"""
Authentication routes: login, signup, logout, password reset.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from bson import ObjectId

from models import User, PasswordResetToken, LoginAttempt
from forms import SignupForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from utils import (
    send_email, generate_reset_token, get_client_ip,
    create_password_reset_email
)


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration page with enhanced validation."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = SignupForm()
    
    if form.validate_on_submit():
        db = current_app.db
        
        # Check if user already exists
        existing_user = User.find_by_email(db, form.email.data.lower())
        if existing_user:
            flash('⚠️ An account with this email already exists. Please <a href="{}">login here</a> or use a different email.'.format(url_for('auth.login')), 'error')
            return render_template('signup.html', form=form, title='Sign Up')
        
        # Create new user (email stored in lowercase for consistency)
        user_id = User.create(
            db,
            email=form.email.data.lower(),
            password=form.password.data,
            name=form.name.data
        )
        
        if user_id:
            flash('✅ Account created successfully! You can now login with your credentials.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('❌ An error occurred while creating your account. Please try again or contact support.', 'error')
    elif form.errors:
        # Display form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'❌ {error}', 'error')
    
    return render_template('signup.html', form=form, title='Sign Up')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page with enhanced error messages."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        db = current_app.db
        email = form.email.data.lower()  # Normalize email to lowercase
        password = form.password.data
        
        # Check for too many failed attempts
        failed_attempts = LoginAttempt.get_recent_failed_attempts(db, email, minutes=15)
        if failed_attempts >= 5:
            flash('🔒 Account temporarily locked due to too many failed login attempts. Please wait 15 minutes or <a href="{}">reset your password</a>.'.format(url_for('auth.forgot_password')), 'error')
            return render_template('login.html', form=form, title='Login')
        
        # Find user
        user = User.find_by_email(db, email)
        
        if user:
            # User exists, check password
            if User.verify_password(user['password_hash'], password):
                # Successful login
                LoginAttempt.record_attempt(db, email, True, get_client_ip(request))
                LoginAttempt.clear_attempts(db, email)
                
                # Update last login
                User.update_last_login(db, email)
                
                # Create Flask-Login user object
                from app import UserLogin
                user_obj = UserLogin(str(user['_id']), user['email'], user['name'])
                
                remember = form.remember_me.data
                login_user(user_obj, remember=remember)
                
                flash(f'✅ Welcome back, {user["name"]}!', 'success')
                
                # Redirect to next page or dashboard
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for('main.dashboard'))
            else:
                # Wrong password
                LoginAttempt.record_attempt(db, email, False, get_client_ip(request))
                remaining_attempts = 5 - (failed_attempts + 1)
                if remaining_attempts > 0:
                    flash(f'❌ Incorrect password. You have {remaining_attempts} attempt(s) remaining. <a href="{url_for("auth.forgot_password")}">Forgot password?</a>', 'error')
                else:
                    flash('🔒 Too many failed attempts. Account locked for 15 minutes.', 'error')
        else:
            # User doesn't exist - don't reveal this for security, but record attempt
            LoginAttempt.record_attempt(db, email, False, get_client_ip(request))
            flash('❌ Invalid email or password. Please check your credentials and try again. <a href="{}">Need an account?</a>'.format(url_for('auth.signup')), 'error')
    elif form.errors:
        # Display form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'❌ {error}', 'error')
    
    return render_template('login.html', form=form, title='Login')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.home'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        db = current_app.db
        email = form.email.data
        
        user = User.find_by_email(db, email)
        
        if user:
            # Generate reset token
            token = generate_reset_token()
            expires_at = datetime.utcnow() + timedelta(hours=1)
            
            PasswordResetToken.create(db, user['_id'], token, expires_at)
            
            # Create reset URL
            app_url = current_app.config.get('APP_URL', 'http://localhost:5000')
            reset_url = f"{app_url}{url_for('auth.reset_password', token=token)}"
            
            # Send email
            subject, body, html_body = create_password_reset_email(reset_url, user['name'])
            send_email(email, subject, body, html_body)
            
            current_app.logger.info(f'Password reset requested for {email}')
        
        # Always show success message (security: don't reveal if email exists)
        flash('If an account exists with that email, you will receive password reset instructions.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('forgot_password.html', form=form, title='Forgot Password')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    db = current_app.db
    
    # Verify token
    token_doc = PasswordResetToken.find_valid_token(db, token)
    
    if not token_doc:
        flash('Invalid or expired password reset link.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        # Update password
        User.update_password(db, token_doc['user_id'], form.password.data)
        
        # Mark token as used
        PasswordResetToken.mark_as_used(db, token)
        
        flash('Your password has been reset successfully. Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html', form=form, token=token, title='Reset Password')
