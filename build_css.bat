:: ReviewFlow — Tailwind CSS Local Build Script
:: Run this from the reviewflow_app/ inner directory (where tailwind.config.js lives)
::
:: STEP 1: Open a terminal (PowerShell or CMD)
:: STEP 2: cd to this directory:
::   cd "c:\Users\Dhairyakant\Desktop\WORK\Internship\Graphura\Project_3\reviewflow_app\reviewflow_app"
:: STEP 3: Run:
::   npx -y tailwindcss@3 -c tailwind.config.js -i input.css -o static/css/output.css --minify
:: STEP 4: Confirm static/css/output.css was created (should be ~30-80KB)
:: STEP 5: Restart your Flask server — the CDN tag is already replaced in base.html
@echo off
echo Building Tailwind CSS bundle for ReviewFlow...
npx -y tailwindcss@3 -c tailwind.config.js -i input.css -o static/css/output.css --minify
echo.
if exist "static\css\output.css" (
    echo [OK] static/css/output.css created successfully!
    echo Tailwind CDN is no longer needed. Restart your Flask server.
) else (
    echo [ERROR] output.css not found. Check node/npm is installed.
)
pause
