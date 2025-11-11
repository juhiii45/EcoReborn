@echo off
REM One-click push to GitHub with auto auth
REM This script uses GitHub CLI (gh) if available, falls back to HTTPS+credential manager

setlocal enabledelayedexpansion

SET GIT_EXE=C:\Program Files\Git\cmd\git.exe
IF NOT EXIST "%GIT_EXE%" SET GIT_EXE=git

SET REPO_URL=https://github.com/juhiii45/EcoReborn.git

REM Verify git is available
"%GIT_EXE%" --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git not found. Install from https://git-scm.com/downloads
    pause
    exit /b 1
)

cd /d "%~dp0"
echo.
echo ========================================
echo Ecoreborn GitHub Push Script
echo ========================================
echo Repository: %REPO_URL%
echo.

REM Step 1: Initialize if needed
if not exist .git (
    echo [1/6] Initializing git repository...
    "%GIT_EXE%" init
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to initialize git
        pause
        exit /b 1
    )
) else (
    echo [1/6] Git repository already initialized
)

REM Step 2: Set remote
echo [2/6] Setting remote origin...
"%GIT_EXE%" remote remove origin 2>nul
"%GIT_EXE%" remote add origin %REPO_URL%
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to set remote
    pause
    exit /b 1
)

REM Step 3: Stage all files
echo [3/6] Staging all files...
"%GIT_EXE%" add -A
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to stage files
    pause
    exit /b 1
)

REM Step 4: Commit
echo [4/6] Creating commit...
"%GIT_EXE%" commit -m "Initial project push" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: No new changes to commit, but continuing...
)

REM Step 5: Set branch to main
echo [5/6] Setting branch to main...
"%GIT_EXE%" branch -M main
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to set branch
    pause
    exit /b 1
)

REM Step 6: Push
echo [6/6] Pushing to GitHub...
echo.
echo Please wait. If prompted, authenticate with GitHub.
echo For HTTPS: Use your username and a Personal Access Token (PAT)
echo.
"%GIT_EXE%" push -u origin main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Push failed!
    echo.
    echo Troubleshooting steps:
    echo 1. If auth failed: Create a PAT at https://github.com/settings/tokens
    echo    Use your username and PAT as password
    echo 2. If using SSH: Add your public key to https://github.com/settings/keys
    echo 3. Try again after resolving the issue
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Repository pushed to GitHub
echo ========================================
echo.
echo Verify at: https://github.com/juhiii45/EcoReborn
echo.
echo Remote status:
"%GIT_EXE%" remote -v
echo.
echo Latest commit:
"%GIT_EXE%" log -1 --oneline
echo.
pause
