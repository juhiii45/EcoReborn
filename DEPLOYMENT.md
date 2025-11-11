# Deployment Guide

This guide provides step-by-step instructions for deploying the Ecoreborn website to various hosting platforms.

## Prerequisites

- Python 3.11 or higher
- MongoDB Atlas account with cluster URL
- Git (for version control)
- Production-ready secret key

## Environment Variables

All platforms require the following environment variables:

```env
SECRET_KEY=<your-production-secret-key>
MONGODB_URI=mongodb+srv://db_user:db_pass@ecoreborn.dkjdd4s.mongodb.net/ecoreborn?retryWrites=true&w=majority
MONGODB_DB_NAME=ecoreborn
FLASK_ENV=production
SESSION_COOKIE_SECURE=True
APP_URL=<your-production-url>

# Optional: Email configuration
SMTP_HOST=<smtp-host>
SMTP_PORT=587
SMTP_USER=<smtp-username>
SMTP_PASS=<smtp-password>
SMTP_FROM=noreply@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com
```

**Important:** Generate a secure SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

1. **Create account** at [render.com](https://render.com)

2. **Create new Web Service**
   - Connect your Git repository
   - Or use "Deploy from Git URL"

3. **Configure build settings:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

4. **Add environment variables** in Render dashboard (see list above)

5. **Add to requirements.txt:**
   ```
   gunicorn==21.2.0
   ```

6. **Initialize database:**
   - After first deploy, use Render Shell to run: `python init_db.py`

7. **Access your site** at `https://your-app.onrender.com`

**Note:** Free tier may sleep after inactivity. Upgrade to paid tier for always-on service.

---

### Option 2: Railway

1. **Create account** at [railway.app](https://railway.app)

2. **New Project → Deploy from GitHub**

3. **Add MongoDB Atlas** environment variables

4. **Railway auto-detects Python** and installs dependencies

5. **Add Procfile** to project root:
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
   ```

6. **Initialize database** via Railway CLI or web terminal:
   ```bash
   python init_db.py
   ```

7. **Generate domain** in Railway settings

---

### Option 3: Heroku

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create new app:**
   ```bash
   heroku create ecoreborn-app
   ```

3. **Add Python buildpack:**
   ```bash
   heroku buildpacks:add heroku/python
   ```

4. **Create Procfile:**
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
   ```

5. **Set environment variables:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set MONGODB_URI=your-mongodb-uri
   heroku config:set FLASK_ENV=production
   heroku config:set SESSION_COOKIE_SECURE=True
   ```

6. **Deploy:**
   ```bash
   git push heroku main
   ```

7. **Initialize database:**
   ```bash
   heroku run python init_db.py
   ```

8. **Open app:**
   ```bash
   heroku open
   ```

---

### Option 4: Linux VPS (Ubuntu + Nginx + Gunicorn)

Perfect for full control and scalability.

#### 1. Prepare Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3.11-venv python3-pip nginx -y
```

#### 2. Create Application User

```bash
sudo useradd -m -s /bin/bash ecoreborn
sudo su - ecoreborn
```

#### 3. Deploy Application

```bash
# Clone repository
git clone <your-repo-url> ~/ecoreborn-website
cd ~/ecoreborn-website

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file
nano .env
# (Add production environment variables)

# Initialize database
python init_db.py
```

#### 4. Create Systemd Service

Exit to root/sudo user and create service file:

```bash
sudo nano /etc/systemd/system/ecoreborn.service
```

Add:

```ini
[Unit]
Description=Ecoreborn Flask Application
After=network.target

[Service]
User=ecoreborn
Group=ecoreborn
WorkingDirectory=/home/ecoreborn/ecoreborn-website
Environment="PATH=/home/ecoreborn/ecoreborn-website/.venv/bin"
ExecStart=/home/ecoreborn/ecoreborn-website/.venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ecoreborn
sudo systemctl start ecoreborn
sudo systemctl status ecoreborn
```

#### 5. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/ecoreborn
```

Add:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/ecoreborn/ecoreborn-website/static;
        expires 30d;
    }

    location /uploads {
        alias /home/ecoreborn/ecoreborn-website/uploads;
        expires 7d;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/ecoreborn /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Certbot auto-renews. Test renewal:

```bash
sudo certbot renew --dry-run
```

---

## Post-Deployment Checklist

- [ ] Verify all environment variables are set
- [ ] Initialize database with `python init_db.py`
- [ ] Change default admin password
- [ ] Test all forms (signup, login, contact, service requests)
- [ ] Test password reset flow
- [ ] Verify CSRF protection is working
- [ ] Check file upload functionality
- [ ] Test on mobile devices
- [ ] Run security scan
- [ ] Set up monitoring (Sentry, New Relic, etc.)
- [ ] Configure backups for MongoDB Atlas
- [ ] Set up logging aggregation
- [ ] Add custom domain (if applicable)
- [ ] Configure SSL/TLS certificate
- [ ] Test email functionality (if SMTP configured)
- [ ] Review logs for errors

---

## Troubleshooting

### Application Won't Start

1. Check logs:
   ```bash
   # Render/Railway: Check dashboard logs
   # Heroku: heroku logs --tail
   # VPS: sudo journalctl -u ecoreborn -f
   ```

2. Verify environment variables are set correctly

3. Ensure MongoDB connection string is valid

### Database Connection Errors

1. Verify MongoDB Atlas cluster is running
2. Check IP whitelist in MongoDB Atlas (add 0.0.0.0/0 for testing)
3. Verify connection string includes database name

### Static Files Not Loading

1. **Render/Railway/Heroku:** Ensure `static` folder is committed to git
2. **VPS:** Check nginx configuration for `/static` location

### CSRF Token Errors

1. Ensure `SECRET_KEY` is set and consistent across restarts
2. Check `SESSION_COOKIE_SECURE` is `True` for HTTPS, `False` for HTTP

---

## Scaling and Performance

### Horizontal Scaling

- Increase Gunicorn workers: `-w 8` (2-4x CPU cores)
- Use async workers: `gunicorn -k gevent -w 4`

### Database Optimization

- Create indexes on frequently queried fields
- Use MongoDB Atlas auto-scaling
- Enable connection pooling

### Caching

Add Redis for session storage and caching:

```python
# Install: pip install flask-caching redis
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://...'})
```

### CDN for Static Assets

Upload static files to Cloudflare, AWS S3, or similar CDN.

---

## Monitoring and Maintenance

### Health Checks

Add health check endpoint in `routes.py`:

```python
@main_bp.route('/health')
def health():
    return {'status': 'healthy'}, 200
```

### Backups

1. **MongoDB Atlas:** Enable automatic backups in dashboard
2. **Code:** Keep in version control (Git)
3. **Uploads:** Sync to S3 or object storage

### Log Rotation

On VPS, configure logrotate:

```bash
sudo nano /etc/logrotate.d/ecoreborn
```

```
/home/ecoreborn/ecoreborn-website/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    notifempty
    create 0640 ecoreborn ecoreborn
}
```

---

## Support

For deployment issues:
- Email: admin@ecoreborn.example
- Check logs first
- Review MongoDB Atlas status
- Verify environment variables

---

**Happy Deploying! 🚀**
