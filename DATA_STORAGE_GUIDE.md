# 📦 Data Storage Locations - Ecoreborn Website

## 🗄️ Data Storage Overview

Your Ecoreborn website stores data in **TWO main locations**:

---

## 1. 🌐 MongoDB Atlas (Cloud Database) - PRIMARY STORAGE

**Location:** Cloud (MongoDB Atlas)
**Connection:** `mongodb+srv://db_user:db_pass@ecoreborn.dkjdd4s.mongodb.net/ecoreborn`

### What's Stored in MongoDB:

#### ✅ **users** Collection
**What:** User account information
**Contains:**
- User's full name
- Email address
- Password (hashed with bcrypt, NOT plaintext)
- Account creation date
- Last login timestamp

**Example Document:**
```json
{
  "_id": ObjectId("..."),
  "name": "John Doe",
  "email": "john@example.com",
  "password_hash": "$2b$12$encrypted_hash_here...",
  "created_at": "2025-11-11T10:00:00Z",
  "last_login": "2025-11-11T15:30:00Z"
}
```

**Access:** MongoDB Atlas Dashboard → Database → Browse Collections → users

---

#### ✅ **contact_messages** Collection
**What:** All contact form submissions
**Contains:**
- Sender's name
- Sender's email
- Subject line
- Message content
- Attached filename (if uploaded)
- Submission date
- Status (new/read/replied/archived)

**Example Document:**
```json
{
  "_id": ObjectId("..."),
  "name": "Jane Smith",
  "email": "jane@example.com",
  "subject": "General Inquiry",
  "message": "I'm interested in your services...",
  "filename": "proposal_20251111_153045.pdf",
  "created_at": "2025-11-11T15:30:00Z",
  "status": "new"
}
```

**Access:** MongoDB Atlas Dashboard → Database → Browse Collections → contact_messages

---

#### ✅ **service_requests** Collection
**What:** All service request form submissions
**Contains:**
- Service name (which service they requested)
- Customer's name
- Customer's email
- Phone number (optional)
- Company name (optional)
- Message/requirements
- Submission date
- Status (pending/in_progress/completed/cancelled)

**Example Document:**
```json
{
  "_id": ObjectId("..."),
  "service_name": "Custom Re-spun Fabric Orders",
  "name": "Business Owner",
  "email": "owner@business.com",
  "phone": "+91 98765 43210",
  "company": "Fashion Brand Ltd",
  "message": "Need 500 meters of recycled cotton fabric",
  "created_at": "2025-11-11T14:20:00Z",
  "status": "pending"
}
```

**Access:** MongoDB Atlas Dashboard → Database → Browse Collections → service_requests

---

#### ✅ **newsletter_subscribers** Collection
**What:** Newsletter email subscriptions
**Contains:**
- Email address
- Subscription date
- Active status (subscribed/unsubscribed)

**Example Document:**
```json
{
  "_id": ObjectId("..."),
  "email": "subscriber@example.com",
  "subscribed_at": "2025-11-11T10:00:00Z",
  "active": true
}
```

**Access:** MongoDB Atlas Dashboard → Database → Browse Collections → newsletter_subscribers

---

#### ✅ **password_reset_tokens** Collection
**What:** Temporary password reset tokens
**Contains:**
- User's email
- Reset token (32-byte random hex)
- Creation date
- Expiration date (1 hour after creation)
- Used status

**Example Document:**
```json
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6",
  "created_at": "2025-11-11T15:00:00Z",
  "expires_at": "2025-11-11T16:00:00Z",
  "used": false
}
```

**Note:** Tokens auto-delete after 1 hour (TTL index)

**Access:** MongoDB Atlas Dashboard → Database → Browse Collections → password_reset_tokens

---

#### ✅ **login_attempts** Collection
**What:** Login attempt tracking (for rate limiting)
**Contains:**
- Email address attempted
- IP address
- Attempt timestamp
- Success status

**Example Document:**
```json
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "ip_address": "192.168.1.100",
  "attempted_at": "2025-11-11T15:30:00Z",
  "successful": false
}
```

**Note:** Auto-deletes after 15 minutes (TTL index)

**Access:** MongoDB Atlas Dashboard → Database → Browse Collections → login_attempts

---

### 🔍 How to View Your MongoDB Data:

1. **Go to:** https://cloud.mongodb.com
2. **Login** with your MongoDB Atlas account
3. **Select** your cluster: `ecoreborn.dkjdd4s`
4. **Click** "Browse Collections"
5. **Select** database: `ecoreborn`
6. **Click** any collection to view data

**You'll see all your real data stored there!**

---

## 2. 💾 Local Files (Your Computer) - TEMPORARY/LOGS

**Location:** `c:\Users\siddh\Desktop\EcoReborn\`

### What's Stored Locally:

#### 📧 **Email Logs** (Development Only)
**File:** `logs/email.log`
**What:** All "sent" emails are logged here for development/testing
**Contains:**
- Password reset emails with links
- Contact form confirmations
- Service request confirmations
- Admin notifications
- Newsletter confirmations

**Purpose:** Since SMTP is not configured, emails are logged to file instead of being sent

**View:** Open `c:\Users\siddh\Desktop\EcoReborn\logs\email.log` in any text editor

**Example:**
```
================================================================================
Timestamp: 2025-11-11 15:30:45 UTC
To: user@example.com
Subject: Password Reset Request - Ecoreborn
--------------------------------------------------------------------------------
Hello User,

Click the link below to reset your password:
http://localhost:5000/reset-password/abc123token

This link will expire in 1 hour.
...
================================================================================
```

---

#### 📁 **Uploaded Files**
**Folder:** `uploads/`
**What:** Files uploaded via contact form
**Contains:**
- PDF documents
- DOC/DOCX files
- Images (JPG, PNG, GIF)
- Text files

**Naming:** `original-filename_YYYYMMDD_HHMMSS.ext`

**Example:**
```
uploads/
  └── proposal_20251111_153045.pdf
  └── requirements_20251111_140520.docx
  └── design_20251111_120815.jpg
```

**View:** Open `c:\Users\siddh\Desktop\EcoReborn\uploads\` folder

**Note:** Currently empty (.gitkeep placeholder only) - files appear here when uploaded

---

#### 📝 **Application Logs**
**File:** `logs/app.log`
**What:** Server activity logs, errors, warnings
**Contains:**
- Server startup messages
- Database connections
- Error messages
- Warning messages
- Request logs

**Purpose:** Debugging and monitoring

**View:** Open `c:\Users\siddh\Desktop\EcoReborn\logs\app.log`

---

## 📊 Complete Data Flow Diagram

```
USER SUBMITS FORM
       ↓
[Flask Application]
       ↓
       ├─→ [Validation] → If invalid: Show error
       ↓
       ├─→ [MongoDB Atlas] → Store data permanently ✅
       ↓
       ├─→ [File Upload] → Save to uploads/ folder (if attached)
       ↓
       ├─→ [Email System] → Log to logs/email.log (development)
       ↓                     Send via SMTP (production)
       ↓
[Success Message]
```

---

## 🔍 How to Access YOUR Data

### Option 1: MongoDB Atlas Dashboard (Recommended)

**Step-by-step:**

1. **Open:** https://cloud.mongodb.com/
2. **Login:** Use your MongoDB Atlas credentials
3. **Dashboard:** You'll see your cluster
4. **Browse Collections:** Click the button on your cluster
5. **Select Database:** `ecoreborn`
6. **View Collections:**
   - Click `users` to see all registered users
   - Click `contact_messages` to see all contact submissions
   - Click `service_requests` to see all service requests
   - Click `newsletter_subscribers` to see all newsletter emails
   - And so on...

**You can:**
- ✅ View all documents
- ✅ Search and filter
- ✅ Edit documents
- ✅ Delete documents
- ✅ Export data (JSON/CSV)

---

### Option 2: Using Python Script

**Create:** `view_data.py` in your project folder

```python
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB_NAME')]

# View all users
print("=== USERS ===")
for user in db.users.find():
    print(f"Name: {user['name']}, Email: {user['email']}")

# View all contact messages
print("\n=== CONTACT MESSAGES ===")
for msg in db.contact_messages.find():
    print(f"From: {msg['name']} ({msg['email']})")
    print(f"Subject: {msg['subject']}")
    print(f"Message: {msg['message'][:50]}...")

# View all service requests
print("\n=== SERVICE REQUESTS ===")
for req in db.service_requests.find():
    print(f"Service: {req['service_name']}")
    print(f"From: {req['name']} ({req['email']})")
    print(f"Status: {req['status']}")
```

**Run:**
```bash
python view_data.py
```

---

### Option 3: Through the Website Dashboard

**For Users:**
1. Login to the website: http://127.0.0.1:5000/login
2. Go to Dashboard: http://127.0.0.1:5000/dashboard
3. View your service requests

**Note:** Currently only shows user's own data. Admin panel could be added to view all data.

---

## 📧 Email Storage Details

### Development Mode (CURRENT):
**Where:** `logs/email.log` (local file)
**When:** Every time an email should be sent
**Contains:**
- ✉️ Password reset links
- ✉️ Contact form confirmations (to user)
- ✉️ Contact notifications (to admin)
- ✉️ Service request confirmations (to user)
- ✉️ Service request notifications (to admin)
- ✉️ Newsletter confirmations

**Check for new emails:**
```bash
# View last 20 lines
type logs\email.log | Select-Object -Last 20

# Or open in editor
notepad logs\email.log
```

---

### Production Mode (When SMTP configured):
**Where:** Sent to actual email addresses via SMTP
**Setup:** Configure in `.env`:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
```

**Then emails will:**
- Be sent to real email addresses
- Still be logged to `logs/email.log` as backup
- Use your SMTP provider (Gmail, SendGrid, etc.)

---

## 📂 File Upload Storage

### Current Location:
```
c:\Users\siddh\Desktop\EcoReborn\uploads\
```

### When files are uploaded:
1. User submits contact form with attachment
2. File is validated (type, size)
3. Filename is sanitized and timestamped
4. File is saved to `uploads/` folder
5. Filename is stored in MongoDB (`contact_messages.filename`)

### View uploaded files:
```bash
# List all uploaded files
dir uploads

# Or open folder in Explorer
explorer uploads
```

---

## 🔒 Security Notes

### What's Secure:
✅ **Passwords:** Hashed with bcrypt (NOT stored as plaintext)
✅ **MongoDB:** Cloud-hosted with authentication
✅ **Files:** Sanitized filenames, size limits
✅ **Emails:** Logged locally (not exposed online)

### What to Protect:
⚠️ **`.env` file:** Contains database credentials - NEVER commit to git
⚠️ **MongoDB URI:** Keep secret - has database access
⚠️ **uploads/ folder:** Contains user files - set proper permissions
⚠️ **logs/ folder:** Contains email content - keep private

---

## 📊 Data Summary

| Data Type | Primary Storage | Backup/Logs | Access Method |
|-----------|----------------|-------------|---------------|
| **User accounts** | MongoDB Atlas | None | MongoDB Dashboard |
| **Passwords** | MongoDB (hashed) | None | Cannot view plaintext |
| **Contact messages** | MongoDB Atlas | None | MongoDB Dashboard |
| **Service requests** | MongoDB Atlas | None | MongoDB Dashboard |
| **Newsletter emails** | MongoDB Atlas | None | MongoDB Dashboard |
| **Password reset tokens** | MongoDB Atlas | None | Auto-expire 1 hour |
| **Login attempts** | MongoDB Atlas | None | Auto-expire 15 min |
| **Sent emails** | logs/email.log | None | View file locally |
| **Uploaded files** | uploads/ folder | Filename in MongoDB | View folder locally |
| **Server logs** | logs/app.log | None | View file locally |

---

## 🎯 Quick Commands to View Data

### View email logs:
```bash
cd c:\Users\siddh\Desktop\EcoReborn
type logs\email.log
```

### View uploaded files:
```bash
cd c:\Users\siddh\Desktop\EcoReborn
dir uploads
```

### View server logs:
```bash
cd c:\Users\siddh\Desktop\EcoReborn
type logs\app.log
```

### Connect to MongoDB and view data:
```python
python
>>> from pymongo import MongoClient
>>> client = MongoClient("your-mongodb-uri")
>>> db = client.ecoreborn
>>> list(db.users.find())
>>> list(db.contact_messages.find())
```

---

## 🔄 Data Lifecycle

### When user signs up:
1. Data stored in MongoDB `users` collection
2. Password hashed and stored
3. User can now login

### When user submits contact form:
1. Data stored in MongoDB `contact_messages` collection
2. File saved to `uploads/` folder (if attached)
3. Confirmation email logged to `logs/email.log`
4. Admin notification logged to `logs/email.log`

### When user requests service:
1. Data stored in MongoDB `service_requests` collection
2. Confirmation email logged to `logs/email.log`
3. Admin notification logged to `logs/email.log`

### When user subscribes to newsletter:
1. Email stored in MongoDB `newsletter_subscribers` collection
2. Confirmation logged to `logs/email.log`

### When user resets password:
1. Token created in MongoDB `password_reset_tokens` collection
2. Reset email logged to `logs/email.log`
3. Token expires after 1 hour (auto-deleted)
4. After reset, token marked as used

---

## 📍 Summary

**PRIMARY DATA STORAGE:**
- 🌐 **MongoDB Atlas (Cloud)** - All user data, messages, requests
- 📍 **Location:** `mongodb+srv://...@ecoreborn.dkjdd4s.mongodb.net/ecoreborn`

**LOCAL STORAGE (Development):**
- 📧 **Email logs:** `c:\Users\siddh\Desktop\EcoReborn\logs\email.log`
- 📁 **Uploaded files:** `c:\Users\siddh\Desktop\EcoReborn\uploads\`
- 📝 **Server logs:** `c:\Users\siddh\Desktop\EcoReborn\logs\app.log`

**To view data:**
1. **MongoDB Atlas Dashboard** (main data)
2. **Open logs/email.log** (emails)
3. **Open uploads/ folder** (files)

---

**Your data is safely stored in MongoDB Atlas and accessible anytime!** ✅
