"""
Database initialization script.
Seeds the database with initial data including admin user.
"""

import os
import sys
from datetime import datetime
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import models
from models import User


def init_database():
    """Initialize MongoDB database with collections and indexes."""
    
    mongodb_uri = os.getenv('MONGODB_URI')
    db_name = os.getenv('MONGODB_DB_NAME', 'ecoreborn')
    
    if not mongodb_uri:
        print("ERROR: MONGODB_URI not set in environment variables.")
        print("Please copy .env.example to .env and update with your MongoDB Atlas credentials.")
        sys.exit(1)
    
    print(f"Connecting to MongoDB...")
    
    try:
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        # Test connection
        client.server_info()
        db = client[db_name]
        print(f"✓ Connected to MongoDB database: {db_name}")
    except Exception as e:
        print(f"ERROR: Failed to connect to MongoDB: {e}")
        sys.exit(1)
    
    # Create collections and indexes
    print("\nCreating collections and indexes...")
    
    # Users collection
    if 'users' not in db.list_collection_names():
        db.create_collection('users')
    db.users.create_index([('email', ASCENDING)], unique=True)
    print("✓ Users collection ready")
    
    # Password reset tokens
    if 'password_reset_tokens' not in db.list_collection_names():
        db.create_collection('password_reset_tokens')
    db.password_reset_tokens.create_index([('token', ASCENDING)], unique=True)
    db.password_reset_tokens.create_index([('expires_at', ASCENDING)], expireAfterSeconds=0)
    print("✓ Password reset tokens collection ready")
    
    # Contact messages
    if 'contact_messages' not in db.list_collection_names():
        db.create_collection('contact_messages')
    db.contact_messages.create_index([('created_at', ASCENDING)])
    print("✓ Contact messages collection ready")
    
    # Service requests
    if 'service_requests' not in db.list_collection_names():
        db.create_collection('service_requests')
    db.service_requests.create_index([('email', ASCENDING)])
    db.service_requests.create_index([('created_at', ASCENDING)])
    print("✓ Service requests collection ready")
    
    # Newsletter subscribers
    if 'newsletter_subscribers' not in db.list_collection_names():
        db.create_collection('newsletter_subscribers')
    db.newsletter_subscribers.create_index([('email', ASCENDING)], unique=True)
    print("✓ Newsletter subscribers collection ready")
    
    # Login attempts
    if 'login_attempts' not in db.list_collection_names():
        db.create_collection('login_attempts')
    db.login_attempts.create_index([('email', ASCENDING)])
    db.login_attempts.create_index([('timestamp', ASCENDING)])
    print("✓ Login attempts collection ready")
    
    # Seed admin user
    print("\nSeeding initial data...")
    
    admin_email = 'admin@ecoreborn.example'
    admin_password = 'Ec0r3b0rn!'
    admin_name = 'Admin User'
    
    existing_admin = User.find_by_email(db, admin_email)
    
    if not existing_admin:
        user_id = User.create(db, admin_email, admin_password, admin_name)
        if user_id:
            print(f"✓ Admin user created:")
            print(f"  Email: {admin_email}")
            print(f"  Password: {admin_password}")
            print(f"  ⚠️  CHANGE THIS PASSWORD IN PRODUCTION!")
        else:
            print("✗ Failed to create admin user")
    else:
        print(f"✓ Admin user already exists: {admin_email}")
    
    # Create sample newsletter subscriber
    from models import NewsletterSubscriber
    if not db.newsletter_subscribers.find_one({'email': 'newsletter@example.com'}):
        NewsletterSubscriber.subscribe(db, 'newsletter@example.com')
        print("✓ Sample newsletter subscriber added")
    
    print("\n" + "="*60)
    print("Database initialization complete!")
    print("="*60)
    print("\nYou can now run the application:")
    print("  python app.py")
    print("\nOr use Flask CLI:")
    print("  flask run")
    print("\nDefault admin credentials:")
    print(f"  Email: {admin_email}")
    print(f"  Password: {admin_password}")
    print("\n⚠️  Remember to change the admin password after first login!")
    print("="*60)


if __name__ == '__main__':
    init_database()
