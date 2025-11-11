# Maintainers Guide

This guide helps developers and maintainers customize and extend the Ecoreborn website.

## Table of Contents

1. [Brand Customization](#brand-customization)
2. [Content Management](#content-management)
3. [Adding New Services](#adding-new-services)
4. [Database Management](#database-management)
5. [Common Tasks](#common-tasks)

---

## Brand Customization

### Changing Brand Colors

Edit `static/css/main.css` and update CSS variables:

```css
:root {
    --color-primary: #2d5016;          /* Main brand color (green) */
    --color-primary-dark: #1f3910;     /* Darker shade */
    --color-primary-light: #4a7a2c;    /* Lighter shade */
    --color-secondary: #8b7355;        /* Secondary color (brown) */
    --color-accent: #c9a66b;           /* Accent color (tan) */
    --color-bg-light: #f8f9f5;         /* Background light */
    --color-bg-white: #ffffff;         /* White background */
    /* ... more colors ... */
}
```

**Tip:** Use a color picker tool to find harmonious color schemes. Update all three variants (primary, primary-dark, primary-light) for consistency.

### Changing Fonts

1. **Update Google Fonts import** in `templates/base.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=YOUR_FONT:wght@300;400;600&display=swap" rel="stylesheet">
```

2. **Update CSS variables** in `static/css/main.css`:

```css
:root {
    --font-primary: 'Your Font', -apple-system, sans-serif;
    --font-display: 'Your Display Font', Georgia, serif;
}
```

**Note:** Always include fallback fonts for accessibility.

### Changing Logo

Replace the inline SVG in `templates/base.html` (lines 80-88) with your logo:

```html
<div class="logo">
    <a href="{{ url_for('main.home') }}">
        <img src="{{ url_for('static', filename='images/logo.png') }}" 
             alt="Ecoreborn" 
             width="40" 
             height="40">
        <span class="logo-text">Ecoreborn</span>
    </a>
</div>
```

Or keep the SVG and customize it.

---

## Content Management

### Homepage Copy

Edit `templates/home.html`:

- **Tagline:** Line 5
- **Subtitle:** Line 6
- **Mission statement:** Line 7
- **Process steps:** Lines 80-150

### Services Page

Edit `routes.py` in the `services()` function (lines 30-60):

```python
services_list = [
    {
        'id': 'unique-id',
        'name': 'Service Name',
        'description': 'Detailed description...',
        'pricing': 'Pricing information'
    },
    # Add more services...
]
```

### Contact Information

Update in multiple locations:

1. **Footer** (`templates/base.html`, lines 150-180):
   - Address
   - Email
   - Social media links

2. **Contact page** (`templates/contact.html`, lines 70-110):
   - Address
   - Business hours
   - Map location

3. **Environment variables** (`.env`):
   - `ADMIN_EMAIL`

### FAQ Section

Edit `templates/services.html` (lines 90-130):

```html
<details class="faq-item">
    <summary>Your Question?</summary>
    <p>Your answer...</p>
</details>
```

---

## Adding New Services

### 1. Add Service to List

Edit `routes.py` in the `services()` function:

```python
services_list = [
    # Existing services...
    {
        'id': 'new-service-slug',
        'name': 'New Service Name',
        'description': 'Full description of the service.',
        'pricing': 'Pricing details or "Contact for quote"'
    }
]
```

### 2. No Template Changes Needed

The service will automatically appear on the services page with a request form.

### 3. Optional: Add Service Icon

Add an SVG icon in `templates/services.html` by creating a new service card template with custom styling.

---

## Database Management

### Accessing MongoDB Atlas

1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Login with your credentials
3. Select your cluster
4. Click "Collections" to view data

### Database Structure

Collections:

- **users:** User accounts
- **contact_messages:** Contact form submissions
- **service_requests:** Service request submissions
- **newsletter_subscribers:** Newsletter emails
- **password_reset_tokens:** Password reset tokens (auto-expire)
- **login_attempts:** Failed login tracking

### Querying Data

Use MongoDB Compass or Python scripts:

```python
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB_NAME', 'ecoreborn')]

# Get all contact messages
messages = db.contact_messages.find().sort('created_at', -1)
for msg in messages:
    print(f"{msg['name']} - {msg['subject']}")
```

### Backup and Restore

**Backup:**

MongoDB Atlas provides automatic backups. To manually export:

1. Install MongoDB Database Tools
2. Run:

```bash
mongodump --uri="your-mongodb-uri" --out=./backup
```

**Restore:**

```bash
mongorestore --uri="your-mongodb-uri" ./backup
```

### Adding Indexes for Performance

Edit `init_db.py` and add indexes:

```python
# Example: Index for faster email lookups
db.users.create_index([('email', ASCENDING)], unique=True)
db.contact_messages.create_index([('created_at', DESCENDING)])
```

Run `python init_db.py` to apply (won't duplicate existing indexes).

---

## Common Tasks

### Adding a New Page

1. **Create route** in `routes.py`:

```python
@main_bp.route('/about')
def about():
    return render_template('about.html', title='About Us')
```

2. **Create template** `templates/about.html`:

```html
{% extends "base.html" %}

{% block content %}
<section class="page-header">
    <div class="container">
        <h1>About Ecoreborn</h1>
    </div>
</section>

<section class="content-section">
    <div class="container">
        <p>Your content here...</p>
    </div>
</section>
{% endblock %}
```

3. **Add to navigation** in `templates/base.html`:

```html
<li><a href="{{ url_for('main.about') }}">About</a></li>
```

### Adding Form Validation

1. **Define form** in `forms.py`:

```python
class NewForm(FlaskForm):
    field = StringField('Label', validators=[
        DataRequired(),
        Length(min=3, max=100)
    ])
```

2. **Use in route** in `routes.py`:

```python
from forms import NewForm

@main_bp.route('/page', methods=['GET', 'POST'])
def page():
    form = NewForm()
    if form.validate_on_submit():
        # Process form
        pass
    return render_template('page.html', form=form)
```

### Changing Email Templates

Edit `utils.py` functions:

- `create_password_reset_email()` - Password reset email
- `create_contact_confirmation_email()` - Contact form confirmation
- `create_service_request_confirmation_email()` - Service request confirmation

### Adding Admin Functionality

Create admin blueprint:

1. **Create** `admin.py`:

```python
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.email != 'admin@ecoreborn.example':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')
```

2. **Register blueprint** in `app.py`:

```python
from admin import admin_bp
app.register_blueprint(admin_bp)
```

### Updating Dependencies

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Update packages
pip install --upgrade -r requirements.txt

# Or update specific package
pip install --upgrade flask

# Update requirements.txt
pip freeze > requirements.txt
```

### Running Tests

```bash
pytest                    # Run all tests
pytest tests/test_auth.py # Run specific test file
pytest --cov=.            # Run with coverage
```

### Viewing Logs

**Development:**
- Console output
- `logs/app.log`
- `logs/email.log`

**Production (VPS):**
```bash
sudo journalctl -u ecoreborn -f
```

**Production (Render/Railway/Heroku):**
Check platform dashboard logs.

---

## Code Structure Reference

```
ecoreborn-website/
├── app.py              # Main Flask application
├── models.py           # Database models
├── forms.py            # WTForms definitions
├── auth.py             # Authentication routes
├── routes.py           # Main application routes
├── utils.py            # Helper functions
├── init_db.py          # Database initialization
├── templates/          # Jinja2 templates
│   ├── base.html       # Base template
│   ├── home.html       # Homepage
│   ├── services.html   # Services page
│   ├── contact.html    # Contact page
│   ├── login.html      # Login page
│   ├── signup.html     # Signup page
│   ├── dashboard.html  # User dashboard
│   └── errors/         # Error pages
├── static/
│   ├── css/
│   │   ├── main.css    # Main stylesheet
│   │   └── print.css   # Print stylesheet
│   └── images/         # Image assets
└── logs/               # Application logs
```

---

## Best Practices

1. **Always test locally** before deploying
2. **Use version control** (Git) for all changes
3. **Keep secrets in .env**, never commit them
4. **Document your changes** in CHANGELOG.md
5. **Follow existing code style** and conventions
6. **Test on mobile devices** after CSS changes
7. **Validate HTML** and check accessibility
8. **Backup database** before major changes

---

## Getting Help

- Review existing code and comments
- Check Flask documentation: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- MongoDB docs: [docs.mongodb.com](https://docs.mongodb.com)
- Create an issue in version control

---

**Happy maintaining! 🛠️**
