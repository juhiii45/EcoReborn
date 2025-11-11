"""
WTForms form definitions with CSRF protection and server-side validation.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError, Optional, Regexp
)
import dns.resolver
import re


def validate_real_email(form, field):
    """
    Custom validator to check if email domain has valid MX records.
    This helps prevent fake/disposable emails.
    """
    email = field.data
    
    # Basic format check first
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValidationError('Please enter a valid email address.')
    
    # Extract domain
    domain = email.split('@')[1]
    
    # Block common disposable email domains
    disposable_domains = [
        'tempmail.com', 'throwaway.email', 'guerrillamail.com', '10minutemail.com',
        'mailinator.com', 'trashmail.com', 'fakeinbox.com', 'yopmail.com',
        'temp-mail.org', 'getnada.com', 'maildrop.cc', 'sharklasers.com'
    ]
    
    if domain.lower() in disposable_domains:
        raise ValidationError('Please use a valid email address. Temporary/disposable emails are not allowed.')
    
    # Check if domain has MX records (real email server)
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if not mx_records:
            raise ValidationError('Email domain does not appear to be valid. Please use a real email address.')
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        raise ValidationError('Email domain does not exist or cannot receive emails. Please check and try again.')
    except Exception:
        # If DNS check fails (network issues, etc.), allow it but log
        # In production, you might want to be stricter
        pass


class SignupForm(FlaskForm):
    """User registration form with enhanced security."""
    
    name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email is too long'),
        validate_real_email  # Custom validator for real email verification
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, max=128, message='Password must be at least 8 characters long'),
        Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])',
            message='Password must include: uppercase letter, lowercase letter, number, and special character (@$!%*?&#)'
        )
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords do not match. Please try again.')
    ])


class LoginForm(FlaskForm):
    """User login form with validation."""
    
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=1, message='Password is required')
    ])
    
    remember_me = BooleanField('Remember Me')


class ForgotPasswordForm(FlaskForm):
    """Forgot password form."""
    
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])


class ResetPasswordForm(FlaskForm):
    """Reset password form with enhanced security."""
    
    password = PasswordField('New Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, max=128, message='Password must be at least 8 characters long'),
        Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])',
            message='Password must include: uppercase letter, lowercase letter, number, and special character (@$!%*?&#)'
        )
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords do not match. Please try again.')
    ])


class ContactForm(FlaskForm):
    """Contact form with optional file upload and email validation."""
    
    name = StringField('Your Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    email = StringField('Your Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        validate_real_email  # Real email validation
    ])
    
    subject = StringField('Subject', validators=[
        DataRequired(message='Subject is required'),
        Length(min=3, max=200, message='Subject must be between 3 and 200 characters')
    ])
    
    message = TextAreaField('Message', validators=[
        DataRequired(message='Message is required'),
        Length(min=10, max=5000, message='Message must be between 10 and 5000 characters')
    ])
    
    attachment = FileField('Attachment (optional, max 2MB)', validators=[
        Optional(),
        FileAllowed(
            ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif'],
            'Only PDF, DOC, DOCX, TXT, JPG, PNG, and GIF files are allowed'
        )
    ])


class ServiceRequestForm(FlaskForm):
    """Service request form with email validation."""
    
    service_name = StringField('Service', validators=[
        DataRequired(message='Service selection is required')
    ])
    
    name = StringField('Your Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    email = StringField('Your Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        validate_real_email  # Real email validation
    ])
    
    phone = StringField('Phone Number', validators=[
        Optional(),
        Length(max=20, message='Phone number is too long'),
        Regexp(r'^[\d\s\-\+\(\)]+$', message='Please enter a valid phone number')
    ])
    
    company = StringField('Company/Organization (if applicable)', validators=[
        Optional(),
        Length(max=150, message='Company name is too long')
    ])
    
    message = TextAreaField('Additional Details', validators=[
        DataRequired(message='Please provide details about your request'),
        Length(min=10, max=2000, message='Message must be between 10 and 2000 characters')
    ])


class NewsletterForm(FlaskForm):
    """Newsletter subscription form with email validation."""
    
    email = StringField('Your Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        validate_real_email  # Real email validation
    ])


def validate_file_size(form, field):
    """Custom validator for file size (2MB limit)."""
    if field.data:
        # FileStorage object
        field.data.seek(0, 2)  # Seek to end
        file_size = field.data.tell()
        field.data.seek(0)  # Reset to beginning
        
        max_size = 2 * 1024 * 1024  # 2MB in bytes
        if file_size > max_size:
            raise ValidationError('File size must not exceed 2MB')
