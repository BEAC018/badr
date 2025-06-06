@echo off
echo 🚀 بدء تشغيل منصة المسابقات الرياضية...
echo Starting Math Competition Platform...
echo.

cd /d "%~dp0"

echo 📋 التحقق من Python...
python --version
if errorlevel 1 (
    echo ❌ Python غير مثبت! يرجى تثبيت Python أولاً
    pause
    exit /b 1
)

echo.
echo 🔧 بدء الخادم المحلي...
echo Starting local server...
echo.
echo 🌐 سيفتح التطبيق على: http://127.0.0.1:8000/
echo Application will be available at: http://127.0.0.1:8000/
echo.
echo 🔑 رمز دخول الطلاب: ben25
echo Student access code: ben25
echo.
echo ⚠️ لإيقاف الخادم اضغط Ctrl+C
echo To stop the server press Ctrl+C
echo.

python manage.py runserver

pause
