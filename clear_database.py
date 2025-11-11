"""
Clear all data from MongoDB database.
This script removes all documents from all collections.
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

def clear_database():
    """Clear all data from all collections."""
    try:
        # Get MongoDB configuration
        mongodb_uri = os.getenv('MONGODB_URI')
        database_name = os.getenv('MONGODB_DB_NAME', 'ecoreborn')
        
        # Connect to MongoDB
        client = MongoClient(mongodb_uri)
        db = client[database_name]
        
        print("🗑️  Clearing MongoDB database...")
        print(f"Database: {database_name}")
        print("-" * 50)
        
        # Get all collection names
        collections = db.list_collection_names()
        
        if not collections:
            print("✅ Database is already empty!")
            return
        
        # Clear each collection
        total_deleted = 0
        for collection_name in collections:
            count = db[collection_name].count_documents({})
            if count > 0:
                result = db[collection_name].delete_many({})
                print(f"✅ Cleared '{collection_name}': {result.deleted_count} documents deleted")
                total_deleted += result.deleted_count
            else:
                print(f"⚪ '{collection_name}': already empty")
        
        print("-" * 50)
        print(f"🎉 Total documents deleted: {total_deleted}")
        print("✅ Database is now clean and ready for fresh data!")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Get database name
    database_name = os.getenv('MONGODB_DB_NAME', 'ecoreborn')
    
    # Ask for confirmation
    print("⚠️  WARNING: This will delete ALL data from your MongoDB database!")
    print(f"Database: {database_name}")
    confirm = input("\nAre you sure you want to continue? (yes/no): ")
    
    if confirm.lower() in ['yes', 'y']:
        clear_database()
    else:
        print("❌ Operation cancelled.")
