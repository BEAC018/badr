@echo off
title منصة المسابقات الرياضية - Math Competition Platform
color 0A

echo.
echo ========================================
echo    🎯 منصة المسابقات الرياضية
echo    📚 Math Competition Platform  
echo ========================================
echo.

cd /d "c:\Users\Acer\OneDrive\Bureau\math2"

echo 🔍 التحقق من المتطلبات...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Python غير مثبت
    echo يرجى تثبيت Python من: https://python.org
    pause
    exit /b 1
)

echo ✅ Python مثبت بنجاح
echo.

echo 🚀 بدء تشغيل الخادم...
echo.
echo 📍 الروابط المهمة:
echo    🏠 الرئيسية: http://127.0.0.1:8000/
echo    👨‍🎓 الطلاب: http://127.0.0.1:8000/student/login/
echo    👨‍🏫 المعلمين: http://127.0.0.1:8000/accounts/login/
echo.
echo 🔑 رمز دخول الطلاب: ben25
echo.
echo ⚠️ لإيقاف الخادم: اضغط Ctrl+C
echo ========================================
echo.

start http://127.0.0.1:8000/
python manage.py runserver

echo.
echo 🛑 تم إيقاف الخادم
pause
