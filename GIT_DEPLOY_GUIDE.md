# 🚀 دليل النشر باستخدام Git

## 📋 الخطوات المطلوبة:

### 1️⃣ تثبيت Git (إذا لم يكن مثبت)
- **Windows**: حمل من https://git-scm.com/download/win
- **أو استخدم GitHub Desktop**: https://desktop.github.com/

### 2️⃣ إعداد Git في مجلد المشروع
افتح Command Prompt أو PowerShell في مجلد المشروع:
```bash
cd "c:\Users\Acer\OneDrive\Bureau\math2"
```

### 3️⃣ تهيئة Git Repository
```bash
git init
git add .
git commit -m "Initial commit - Math Competition Platform"
```

### 4️⃣ ربط GitHub Repository
```bash
git remote add origin https://github.com/BEAC018/math-competition-platform.git
git branch -M main
git push -u origin main
```

### 5️⃣ إذا واجهت مشاكل في الرفع
```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

---

## 🌐 بعد رفع الملفات إلى GitHub:

### انتقل إلى Render:
1. اذهب إلى: https://render.com
2. سجل دخول بـ GitHub
3. اضغط **"New +"** → **"Web Service"**
4. اختر مستودعك: **"math-competition-platform"**

### إعدادات Render:
```
Build Command: pip install Django==5.2.1 gunicorn==21.2.0 whitenoise==6.6.0
Start Command: gunicorn alhassan.wsgi:application --bind 0.0.0.0:$PORT

Environment Variables:
SECRET_KEY=django-insecure-math-competition-platform-secret-key-123456789
DEBUG=False
DJANGO_SETTINGS_MODULE=alhassan.deploy_settings
STUDENT_ACCESS_CODE=ben25
PORT=10000
```

---

## 🔧 إذا لم يعمل Git:

### استخدم GitHub Desktop:
1. حمل GitHub Desktop من: https://desktop.github.com/
2. سجل دخول بحساب GitHub
3. اضغط **"Add an Existing Repository from your Hard Drive"**
4. اختر مجلد: `c:\Users\Acer\OneDrive\Bureau\math2`
5. اضغط **"Publish repository"**

---

## 📞 الدعم:

إذا واجهت أي مشكلة:
1. أخبرني بنص الخطأ
2. أو استخدم GitHub Desktop (أسهل)
3. أو ارفع الملفات يدوياً إلى GitHub

---

## 🎯 الهدف:

**رفع جميع ملفات المشروع إلى GitHub، ثم ربطها بـ Render للنشر التلقائي.**

**أي طريقة تفضل؟ Git Command Line أم GitHub Desktop؟**
