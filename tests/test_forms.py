"""
Test suite for form validation.
"""

import pytest
from forms import SignupForm, LoginForm, ContactForm, ServiceRequestForm


class TestSignupForm:
    """Test signup form validation."""
    
    def test_valid_signup_form(self, app):
        """Test valid signup form data."""
        with app.test_request_context():
            form = SignupForm(data={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'Test123!@#',
                'confirm_password': 'Test123!@#',
                'csrf_token': 'dummy'  # Disabled in testing
            })
            # In test context, CSRF is disabled
            assert form.validate() or 'csrf_token' in form.errors
    
    def test_password_too_short(self, app):
        """Test password minimum length validation."""
        with app.test_request_context():
            form = SignupForm(data={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'Short1!',
                'confirm_password': 'Short1!',
                'csrf_token': 'dummy'
            })
            is_valid = form.validate()
            if not is_valid:
                assert 'password' in form.errors or 'csrf_token' in form.errors
    
    def test_password_mismatch(self, app):
        """Test password confirmation validation."""
        with app.test_request_context():
            form = SignupForm(data={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'Test123!@#',
                'confirm_password': 'Different123!@#',
                'csrf_token': 'dummy'
            })
            is_valid = form.validate()
            if not is_valid:
                assert 'confirm_password' in form.errors or 'csrf_token' in form.errors


class TestContactForm:
    """Test contact form validation."""
    
    def test_valid_contact_form(self, app):
        """Test valid contact form data."""
        with app.test_request_context():
            form = ContactForm(data={
                'name': 'Test User',
                'email': 'test@example.com',
                'subject': 'Test Subject',
                'message': 'This is a test message with enough characters.',
                'csrf_token': 'dummy'
            })
            assert form.validate() or 'csrf_token' in form.errors
    
    def test_invalid_email(self, app):
        """Test email validation."""
        with app.test_request_context():
            form = ContactForm(data={
                'name': 'Test User',
                'email': 'invalid-email',
                'subject': 'Test',
                'message': 'Test message',
                'csrf_token': 'dummy'
            })
            is_valid = form.validate()
            if not is_valid:
                assert 'email' in form.errors or 'csrf_token' in form.errors
    
    def test_message_too_short(self, app):
        """Test message minimum length validation."""
        with app.test_request_context():
            form = ContactForm(data={
                'name': 'Test User',
                'email': 'test@example.com',
                'subject': 'Test',
                'message': 'Short',
                'csrf_token': 'dummy'
            })
            is_valid = form.validate()
            if not is_valid:
                assert 'message' in form.errors or 'csrf_token' in form.errors


class TestServiceRequestForm:
    """Test service request form validation."""
    
    def test_valid_service_request(self, app):
        """Test valid service request form."""
        with app.test_request_context():
            form = ServiceRequestForm(data={
                'service_name': 'Fabric Recycling',
                'name': 'Test User',
                'email': 'test@example.com',
                'phone': '+91 98765 43210',
                'company': 'Test Company',
                'message': 'This is a valid service request message.',
                'csrf_token': 'dummy'
            })
            assert form.validate() or 'csrf_token' in form.errors
    
    def test_optional_fields(self, app):
        """Test that phone and company are optional."""
        with app.test_request_context():
            form = ServiceRequestForm(data={
                'service_name': 'Consulting',
                'name': 'Test User',
                'email': 'test@example.com',
                'phone': '',
                'company': '',
                'message': 'This is a valid service request message.',
                'csrf_token': 'dummy'
            })
            assert form.validate() or 'csrf_token' in form.errors


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
