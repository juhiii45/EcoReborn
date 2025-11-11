# Creating the Distribution Archive

## For Windows Users

### Option 1: Using File Explorer
1. Open the `EcoReborn` folder
2. Select all files and folders
3. Right-click → Send to → Compressed (zipped) folder
4. Rename to `ecoreborn-website.zip`

### Option 2: Using PowerShell
```powershell
Compress-Archive -Path .\* -DestinationPath ..\ecoreborn-website.zip
```

### Option 3: Using Command Prompt (if 7-Zip installed)
```cmd
"C:\Program Files\7-Zip\7z.exe" a -tzip ..\ecoreborn-website.zip *
```

## For Linux/Mac Users

```bash
# From parent directory
zip -r ecoreborn-website.zip EcoReborn/ -x "*.pyc" "*.pyo" "*__pycache__*" "*/.venv/*" "*/.git/*"

# Or from inside the EcoReborn directory
cd EcoReborn
zip -r ../ecoreborn-website.zip . -x "*.pyc" "*.pyo" "*__pycache__*" "*/.venv/*" "*/.git/*"
```

## What's Included in the Archive

```
ecoreborn-website/
├── Core Application Files
│   ├── app.py
│   ├── models.py
│   ├── forms.py
│   ├── auth.py
│   ├── routes.py
│   ├── utils.py
│   └── init_db.py
│
├── Configuration
│   ├── .env.example
│   ├── requirements.txt
│   ├── .gitignore
│   └── pytest.ini
│
├── Templates (10 files)
│   └── templates/
│
├── Static Assets
│   ├── static/css/
│   └── static/images/
│
├── Tests (3 files)
│   └── tests/
│
├── Logs & Uploads
│   ├── logs/email.log
│   └── uploads/.gitkeep
│
├── Documentation (8 files)
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── DEPLOYMENT.md
│   ├── MAINTAINERS.md
│   ├── CHANGELOG.md
│   ├── TODO.md
│   ├── PROJECT_SUMMARY.md
│   └── LICENSE
│
├── Scripts
│   ├── setup.bat (Windows)
│   ├── setup.sh (Linux/Mac)
│   └── run.bat (Windows)
│
└── SEO Files
    ├── sitemap.xml
    └── robots.txt
```

## File Exclusions

The following should NOT be in the zip:
- `__pycache__/` directories
- `.pyc` and `.pyo` files
- `.venv/` or `venv/` directories
- `.env` file (only .env.example)
- `.git/` directory
- `*.db` or `*.sqlite` database files
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)

## Verification

After creating the zip, verify it contains:
- ✅ 35+ files total
- ✅ All .py files (8 main files)
- ✅ All templates (10 HTML files)
- ✅ All documentation (8 .md files)
- ✅ CSS files (2 files)
- ✅ Test files (3 files)
- ✅ requirements.txt
- ✅ .env.example (NOT .env)
- ✅ setup scripts

## Archive Size

Expected size: 150-250 KB (compressed)

## Distribution

The `ecoreborn-website.zip` can be:
1. Uploaded to file sharing services
2. Distributed via email
3. Hosted on GitHub releases
4. Deployed directly to hosting platforms

## Extraction Instructions for Recipients

### Windows:
1. Right-click the zip file
2. Extract All...
3. Choose destination folder

### Linux/Mac:
```bash
unzip ecoreborn-website.zip
cd ecoreborn-website
```

Then follow QUICKSTART.md or README.md for setup instructions.

---

**Ready to distribute! 🎉**
