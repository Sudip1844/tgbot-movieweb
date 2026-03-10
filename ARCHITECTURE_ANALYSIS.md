# একীভূত প্রজেক্ট - স্থাপত্য বিশ্লেষণ

## বর্তমান স্ট্রাকচার

### 1. Tgbot (Telegram Bot) - Python

```
├── main.py                 # প্রধান বট লজিক
├── config.py              # কনফিগারেশন (TOKEN, OWNER_ID, CATEGORIES)
├── database.py            # ডাটাবেস হ্যান্ডলিং
├── utils.py               # সাহায্যকারী ফাংশন
├── handlers/              # বিভিন্ন হ্যান্ডলার মডিউল
│   ├── start_handler.py
│   ├── movie_handlers.py
│   ├── callback_handler.py
│   ├── conversation_handlers.py
│   └── owner_handlers.py
├── data/                  # JSON ডাটা ফাইল
│   ├── users.json
│   ├── movies.json
│   ├── admins.json
│   └── ...
└── ad_page/               # HTML/JS বিজ্ঞাপন পেজ
```

**প্রযুক্তি**: Python, python-telegram-bot, JSON storage

---

### 2. Movieweb (Web সার্ভার + Frontend) - Node.js/TypeScript

```
├── server/                # Express সার্ভার
│   ├── index.ts           # প্রধান সার্ভার এন্ট্রি
│   ├── routes.ts          # API রুট (978 লাইন - বিশাল!)
│   ├── storage.ts         # স্টোরেজ লেয়ার
│   ├── supabase-client.ts # Supabase ডাটাবেস
│   └── db.ts              # ডাটাবেস স্কিমা
├── client/                # React + Vite Frontend
│   ├── src/
│   │   ├── components/    # React কম্পোনেন্ট
│   │   └── ...
│   └── dist/              # বিল্ডেড আউটপুট
├── package.json
└── vite.config.ts
```

**প্রযুক্তি**: Node.js, Express, TypeScript, React, Vite, Supabase, Drizzle ORM

---

## কী কী করে

### Tgbot

1. **Telegram Bot Operations**:
   - ইউজাররা `/start` দিয়ে বটকে অ্যাক্টিভ করে
   - ইউজাররা মুভি লিংক পাঠায়
   - মালিক মুভি যোগ/এডিট করতে পারে
   - বট Telegram চ্যানেলে পোস্ট করে

2. **ডাটাবেস**: JSON ফাইল ব্যবহার করে
   - users.json
   - movies.json
   - admins.json
   - tokens.json
   - etc.

---

### Movieweb

1. **API এন্ডপয়েন্ট** (Express):
   - `/api/health` - স্বাস্থ্য চেক
   - `/api/admin-config` - অ্যাডমিন সেটিংস
   - মুভি লিংক ম্যানেজমেন্ট
   - শর্ট লিংক তৈরি ও পরিচালনা
   - রিডাইরেক্ট/বিজ্ঞাপন পেজ পরিচালনা

2. **সার্ভার ফিচার**:
   - CORS সাপোর্ট
   - Authentication (API tokens)
   - বিজ্ঞাপন পেজ serve করা (HTML/CSS/JS)
   - রিডাইরেক্ট লজিক

3. **ফ্রন্টএন্ড**: React + Admin Panel

4. **ডাটাবেস**: Supabase (PostgreSQL)

---

## লক্ষ্য: একীভূত Python সার্ভার

### নতুন আর্কিটেকচার

```
INTEGRATED-SERVER/
├── bot/                   # Telegram Bot Module
│   ├── main.py
│   ├── handlers/
│   └── commands/
├── server/                # Web Server Module
│   ├── app.py            # Flask/FastAPI প্রধান
│   ├── routes/
│   │   ├── movies.py
│   │   ├── shorts.py
│   │   ├── redirect.py
│   │   ├── admin.py
│   │   └── health.py
│   └── middleware.py
├── database/              # Unified Database
│   ├── models.py         # ORM models
│   ├── connection.py
│   └── migrations/
├── config.py             # Centralized Configuration
├── utils.py              # Shared Utilities
├── requirements.txt      # Python dependencies
└── main.py               # Entry point (bot + server চালায়)
```

---

## কী রূপান্তর করতে হবে

### 1. Express → Flask/FastAPI (Python)

- ✅ routes.ts (978 লাইন) → routes/\*.py
- ❌ TypeScript → Python
- ✅ CORS → Flask-CORS
- ✅ Express middleware → Flask decorators/blueprints

### 2. Supabase (PostgreSQL) → বিকল্প

**বিকল্প**:

- Option A: Supabase রাখুন (Supabase Python client ব্যবহার)
- Option B: SQLite → Local DB
- Option C: SQLAlchemy + PostgreSQL

### 3. Frontend (React)

- **রাখুন** React/TypeScript frontend - Python backend থেকে separate
- Vite build করুন static files হিসেবে
- Python সার্ভার থেকে serve করুন

---

## পর্যায়ক্রম বাস্তবায়ন

### Phase 1: প্রস্তুতি

- [ ] ডায়রেক্টরি স্ট্রাকচার তৈরি করি
- [ ] requirements.txt তৈরি করি
- [ ] Flask/FastAPI সেটআপ করি

### Phase 2: API রুট রূপান্তর

- [ ] routes.ts বিশ্লেষণ করি
- [ ] Python-এ রূপান্তর করি
- [ ] ডাটাবেস লেয়ার তৈরি করি

### Phase 3: Integration

- [ ] Telegram Bot integrate করি
- [ ] ডাটা মাইগ্রেশন করি
- [ ] Testing করি

---

## প্রশ্ন

1. **ডাটাবেস**: Supabase রাখবো নাকি SQLite/Local?
2. **এখনকার ডাটা**: মুভি ডাটা যা JSON-এ আছে, SQL-এ মাইগ্রেট করব?
3. **React Frontend**: কি একই URL-এ থাকবে (`/` root থেকে)?
4. **পোর্ট**: কি একটি একক পোর্টে (e.g., 5000) চালাব?
