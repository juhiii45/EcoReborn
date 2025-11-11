@echo off
REM Push project to GitHub (Windows batch)
REM Run this from the project folder: double-click or run in cmd

REM Optional: If Git is installed in a non-PATH location, set this to the full path
SET GIT_EXE=C:\Program Files\Git\cmd\git.exe
IF NOT EXIST "%GIT_EXE%" (
    REM fallback to git on PATH
    SET GIT_EXE=git
)

REM Quick check that git is callable
"%GIT_EXE%" --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
  echo Git not found in PATH and not at "%GIT_EXE%". Please install Git from https://git-scm.com/downloads and re-run this script.
  pause
  exit /b 1
)

SET REPO_URL=https://github.com/juhiii45/EcoReborn.git

REM Change to script directory (project root)
cd /d "%~dp0"

REM Initialize git if needed
if not exist .git (
  echo Initializing new git repository...
  "%GIT_EXE%" init
) else (
  echo Existing git repository detected.
)

REM Ensure origin remote points to the target repo
"%GIT_EXE%" remote | findstr /R /C:"^origin$" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  echo Updating origin remote to %REPO_URL%...
  "%GIT_EXE%" remote set-url origin %REPO_URL%
) else (
  echo Adding origin remote %REPO_URL%...
  "%GIT_EXE%" remote add origin %REPO_URL%
)

REM Stage all changes
echo Staging files...
"%GIT_EXE%" add -A

REM Commit
echo.
set /p COMMIT_MSG=Enter commit message (press Enter for default: "Initial project push"): 
if "%COMMIT_MSG%"=="" (
  set COMMIT_MSG=Initial project push
)

"%GIT_EXE%" commit -m "%COMMIT_MSG%" 2>nul
if %ERRORLEVEL% NEQ 0 (
  echo No changes to commit or commit failed. Continuing to push existing commits.
) else (
  echo Commit created successfully.
)

REM Ensure branch is main
for /f "delims=" %%b in ('"%GIT_EXE%" branch --show-current 2^>nul') do set CURR_BRANCH=%%b

if "%CURR_BRANCH%"=="" (
  echo No current branch detected, setting to main...
  "%GIT_EXE%" branch -M main
) else (
  echo Current branch is %CURR_BRANCH%. Renaming to main...
  "%GIT_EXE%" branch -M main
)

REM Push to origin main
echo Pushing to remote origin main. You may be prompted for GitHub credentials (username and PAT).
"%GIT_EXE%" push -u origin main
if %ERRORLEVEL% NEQ 0 (
  echo Push failed. If using HTTPS you may need to provide a Personal Access Token (PAT) as password.
  echo See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
  pause
  exit /b 1
) else (
  echo Push succeeded.
)

echo All done. Verify your GitHub repo at: %REPO_URL%
pause
