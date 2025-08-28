@echo off
echo Fixing PostgreSQL Database Schema...
echo.

REM Try different Python commands
python migrate_database_schema.py
if %errorlevel% equ 0 goto :success

py migrate_database_schema.py
if %errorlevel% equ 0 goto :success

python3 migrate_database_schema.py
if %errorlevel% equ 0 goto :success

echo.
echo Python not found. Please run the following SQL commands manually:
echo.
echo ALTER TABLE "order" ALTER COLUMN order_number TYPE VARCHAR(30);
echo ALTER TABLE "order" ALTER COLUMN phone TYPE VARCHAR(15);
echo.
echo Connect to your PostgreSQL database and run these commands.
pause
exit /b 1

:success
echo.
echo Database migration completed successfully!
pause
