# 🚀 ONE COMMAND DEPLOYMENT

## সবকিছু এক কমান্ডে!

আমি আপনার Service Role Key ব্যবহার করে সরাসরি SQL execute করবো এবং সার্ভার চালাবো।

### Command:

```powershell
cd "d:\vs code use\tgbot+movieweb\IntegratedServer"
.\auto_deploy.bat
```

### এটি যা করবে:

1. ✅ Python virtual environment তৈরি
2. ✅ সমস্ত dependencies install
3. ✅ **সরাসরি Supabase-এ SQL execute করবে** (manual Dashboard-এ যাওয়ার দরকার নেই!)
4. ✅ Database connection test করবে
5. ✅ Server পোর্ট 5000-এ চালু করবে
6. ✅ Browser-এ http://localhost:5000 খুলুন

### সময়: ~5 মিনিট

---

## বিস্তারিত কী হবে:

```
auto_deploy.bat
    ↓
    ├─ Python venv তৈরি
    ├─ pip install (dependencies)
    ├─ execute_sql.py চালানো
    │   └─→ PostgreSQL সরাসরি সংযোগ করবে
    │   └─→ SQL Schema execute করবে
    │   └─→ 7 টা টেবিল তৈরি করবে
    ├─ test_connection.py চালানো
    │   └─→ সবকিছু সঠিক আছে কিনা যাচাই করবে
    └─ main.py চালানো
        └─→ Server শুরু হয়ে যাবে
```

---

## তৈরি নতুন স্ক্রিপ্টগুলি:

1. **execute_sql.py** - SQL Schema Supabase-এ deploy করবে
   - PostgreSQL direct connection ব্যবহার করবে
   - .env থেকে credentials নেবে
   - 7 টা টেবিল তৈরি করবে
   - Verification করবে

2. **auto_deploy.bat** - সম্পূর্ণ প্রক্রিয়া automated
   - One-click অটোমেশন
   - Step-by-step progress দেখায়
   - সার্ভার চালু করে দেয়

---

## উপলব্ধ অপশন:

### অপশন 1️⃣: সম্পূর্ণ অটোমেশন (সবচেয়ে সহজ)

```powershell
cd IntegratedServer
.\auto_deploy.bat
```

✅ একটি কমান্ড - সবকিছু হয়ে যায়

### অপশন 2️⃣: ধাপে ধাপে

```powershell
cd IntegratedServer
.\setup.bat                # Step 1: Environment setup
python execute_sql.py      # Step 2: Deploy SQL
python test_connection.py  # Step 3: Test
python main.py             # Step 4: Start
```

### অপশন 3️⃣: Manual SQL তারপর সার্ভার

```powershell
cd IntegratedServer
python execute_sql.py      # Deploy SQL only
python main.py             # Start server
```

---

## এক্সপেক্টেড আউটপুট:

```
✅ Python found
✅ Virtual environment created
✅ Dependencies installed

🗄️ Executing SQL schema...
   ✓ Executed 10 statements...
   ✓ Executed 20 statements...
   ✓ Executed 30 statements...
✅ All statements executed!

🧪 Testing connection...
✅ Config loaded successfully
✅ Database connection successful!
✅ Database tables accessible
✅ Flask app created successfully!
🎉 All tests passed!

🚀 STARTING SERVER...
 * Running on http://0.0.0.0:5000

(Server চলছে - ব্রাউজার খুলুন!)
```

---

## যদি কোন সমস্যা হয়:

### "ModuleNotFoundError"

```
→ auto_deploy.bat আবার চালান
→ বড় ফাইলগুলি ডাউনলোড করতে সময় লাগে
```

### "Connection refused Supabase"

```
→ .env file-এ credentials চেক করুন
→ Supabase project active আছে কিনা দেখুন
→ Internet connection যাচাই করুন
```

### "Port 5000 in use"

```
→ IntegratedServer/.env তে FLASK_PORT=5001 বদলান
→ auto_deploy.bat আবার চালান
```

---

## 🎉 Ready?

শুধু এটি চালান:

```powershell
cd "d:\vs code use\tgbot+movieweb\IntegratedServer"
.\auto_deploy.bat
```

**সবকিছু হয়ে যাবে!** ✅

---

**Status**: সব প্রস্তুত! এখন শুধু command চালান।
