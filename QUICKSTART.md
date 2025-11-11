# Quick Start Guide

## For First-Time Setup

### Windows:
1. Double-click `setup.bat`
2. Edit `.env` with your MongoDB credentials
3. Run: `python init_db.py`
4. Run: `run.bat` or `python app.py`

### Linux/Mac:
```bash
chmod +x setup.sh
./setup.sh
# Edit .env with your MongoDB credentials
python init_db.py
python app.py
```

## MongoDB Atlas Setup

1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account and cluster
3. Create database user (remember username/password)
4. Get connection string (looks like: `mongodb+srv://...`)
5. Update `.env` file with your credentials

Replace in the connection string:
- `db_user` with your database username
- `db_pass` with your database password

Example:
```
MONGODB_URI=mongodb+srv://myuser:mypassword@ecoreborn.dkjdd4s.mongodb.net/ecoreborn?retryWrites=true&w=majority
```

## Default Admin Login

After running `init_db.py`, use these credentials:
- **Email:** admin@ecoreborn.example
- **Password:** Ec0r3b0rn!

⚠️ **Change this password immediately in production!**

## Accessing the Website

Open your browser and go to:
```
http://localhost:5000
```

## Common Issues

### "MongoDB connection failed"
- Check your internet connection
- Verify MongoDB Atlas cluster is running
- Check connection string in `.env`
- Whitelist your IP in MongoDB Atlas (or use 0.0.0.0/0)

### "Port 5000 already in use"
- Another app is using port 5000
- Change port in app.py: `app.run(port=5001)`
- Or stop the other application

### "Module not found"
- Virtual environment not activated
- Run setup script again
- Or manually: `pip install -r requirements.txt`

## Testing

Run tests with:
```bash
pytest
```

## Need Help?

Check the full README.md for detailed instructions.
