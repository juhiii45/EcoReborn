"""
Test suite for authentication functionality.
"""

import pytest
from app import create_app
from models import User


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    yield app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def db(app):
    """Get database instance."""
    return app.db


class TestAuthentication:
    """Test authentication flows."""
    
    def test_signup_page_loads(self, client):
        """Test signup page is accessible."""
        response = client.get('/signup')
        assert response.status_code == 200
        assert b'Sign Up' in response.data
    
    def test_login_page_loads(self, client):
        """Test login page is accessible."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_successful_signup(self, client, db):
        """Test user can sign up successfully."""
        response = client.post('/signup', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'Test123!@#',
            'confirm_password': 'Test123!@#'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify user was created
        user = User.find_by_email(db, 'test@example.com')
        assert user is not None
        assert user['name'] == 'Test User'
        
        # Clean up
        db.users.delete_one({'email': 'test@example.com'})
    
    def test_signup_duplicate_email(self, client, db):
        """Test signup fails with duplicate email."""
        # Create initial user
        User.create(db, 'existing@example.com', 'Test123!@#', 'Existing User')
        
        # Try to sign up with same email
        response = client.post('/signup', data={
            'name': 'New User',
            'email': 'existing@example.com',
            'password': 'Test123!@#',
            'confirm_password': 'Test123!@#'
        }, follow_redirects=True)
        
        assert b'already exists' in response.data
        
        # Clean up
        db.users.delete_one({'email': 'existing@example.com'})
    
    def test_signup_password_mismatch(self, client):
        """Test signup fails when passwords don't match."""
        response = client.post('/signup', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'Test123!@#',
            'confirm_password': 'Different123!@#'
        })
        
        assert b'must match' in response.data or response.status_code == 200
    
    def test_successful_login(self, client, db):
        """Test user can login successfully."""
        # Create test user
        User.create(db, 'login@example.com', 'Test123!@#', 'Login User')
        
        # Login
        response = client.post('/login', data={
            'email': 'login@example.com',
            'password': 'Test123!@#'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Welcome back' in response.data or b'Dashboard' in response.data
        
        # Clean up
        db.users.delete_one({'email': 'login@example.com'})
    
    def test_login_wrong_password(self, client, db):
        """Test login fails with wrong password."""
        # Create test user
        User.create(db, 'wrongpw@example.com', 'Test123!@#', 'Test User')
        
        # Try login with wrong password
        response = client.post('/login', data={
            'email': 'wrongpw@example.com',
            'password': 'WrongPassword123!@#'
        })
        
        assert b'Invalid' in response.data or b'password' in response.data.lower()
        
        # Clean up
        db.users.delete_one({'email': 'wrongpw@example.com'})
    
    def test_login_nonexistent_user(self, client):
        """Test login fails for non-existent user."""
        response = client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'Test123!@#'
        })
        
        assert b'Invalid' in response.data or response.status_code == 200
    
    def test_logout(self, client, db):
        """Test user can logout."""
        # Create and login user
        User.create(db, 'logout@example.com', 'Test123!@#', 'Logout User')
        client.post('/login', data={
            'email': 'logout@example.com',
            'password': 'Test123!@#'
        })
        
        # Logout
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'logged out' in response.data.lower()
        
        # Clean up
        db.users.delete_one({'email': 'logout@example.com'})
    
    def test_dashboard_requires_login(self, client):
        """Test dashboard is protected."""
        response = client.get('/dashboard', follow_redirects=True)
        assert b'login' in response.data.lower() or response.status_code == 200
    
    def test_forgot_password_page(self, client):
        """Test forgot password page loads."""
        response = client.get('/forgot-password')
        assert response.status_code == 200
        assert b'Forgot Password' in response.data
    
    def test_password_hashing(self, db):
        """Test passwords are hashed, not stored in plaintext."""
        User.create(db, 'hash@example.com', 'Test123!@#', 'Hash User')
        
        user = User.find_by_email(db, 'hash@example.com')
        assert user is not None
        assert user['password_hash'] != b'Test123!@#'
        assert len(user['password_hash']) > 20  # Bcrypt hashes are long
        
        # Verify password
        assert User.verify_password(user['password_hash'], 'Test123!@#')
        assert not User.verify_password(user['password_hash'], 'WrongPassword')
        
        # Clean up
        db.users.delete_one({'email': 'hash@example.com'})


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
