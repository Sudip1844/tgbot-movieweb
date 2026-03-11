# 🎯 INTEGRATION PROJECT PLAN (UPDATED: SINGLE SERVER, UNIFIED DATA ENTRY)

## ✅ COMPLETED

- [x] Deleted all duplicate MD files (kept only README.md)
- [x] Identified Supabase schema (7 tables)
- [x] Found Admin credentials: `sbiswas1844` / `save@184455`

---

## 🔄 UPDATED REQUIREMENTS BASED ON YOUR INPUT:

### **Workflow Changes:**

**BEFORE:**
```
1. Create movie in Movieweb (short links) → 2. Add movie in Tgbot (metadata) → 3. Auto-post to Telegram
```

**AFTER:**
```
1. Create movie in IntegratedServer website (name + links + metadata + thumbnail) → 2. Goes to review queue → 3. Owner reviews via bot → 4. Approve/Reject/Edit → 5. Post to Telegram
```

### **Command Removal from Bot:**
- ❌ Remove `add movie` command (movie creation moves to website)
- ❌ Remove `add admin`/`remove admin` commands (admin management moves to website)

### **New Commands in Bot:**
- ✅ `review movie` - Owner sees pending movies, can approve/reject/edit
- ✅ `edit movie` - For thumbnail updates if not uploaded via website

### **Website Routes:**
- `/sudip` - Owner panel (hardcoded login: `sbiswas1844` / `save@184455`)
- `/admin` - Admin login panel (admins created by owner)
- `/redirect` - Ad intermediate page (10-second timer)

### **New Database Tables:**

1. **`movie_reviews`** - Pending movies for review (status: pending/approved/rejected)
2. **`admin_accounts`** - Manually created admin accounts by owner

### **Requirement 1**: Tgbot + Movieweb separate, but IntegratedServer combines both

```
INPUT (Unchanged):
├── Tgbot/          (runs independently)
└── Movieweb/       (runs independently)

OUTPUT (IntegratedServer):
└── IntegratedServer/
    ├── main.py                   (Runs bot + Flask + Frontend together)
    └── config.py                 (Unified credentials)
```

### **Single Server Architecture:**

```
❌ OLD SEPARATE SERVERS:
  Terminal 1: Tgbot ─────────────► JSON files (local)
  Terminal 2: Movieweb ──────────► Supabase (direct)

✅ NEW SINGLE SERVER:
  Terminal 1: IntegratedServer ──► Supabase (single connection)
               ├── Bot Module
               ├── API Server  
               └── Frontend (Fixed & Working)
```

### **Requirement 4**: Merge both codebases into IntegratedServer

```
Tgbot/handlers/*.py        ──► IntegratedServer/bot/
Tgbot/database.py          ──► IntegratedServer/database/repository.py
Movieweb/server/routes.ts  ──► IntegratedServer/server/routes/

Both SHARE:
├── Same Database (Supabase)
├── Same Config (credentials, settings)
├── Same Admin System
└── Same API endpoints
```

---

## 🏗️ ARCHITECTURE AFTER INTEGRATION:

```
┌─────────────────────────────────────────────────────┐
│        IntegratedServer (Python Flask)              │
│         Running: python main.py                     │
│         Ports: Bot (Telegram API), 5000 (Flask)    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │  BOT MODULE (from Tgbot)                      │ │
│  │  ├── handlers/start_handler.py                │ │
│  │  ├── handlers/movie_handlers.py               │ │
│  │  ├── handlers/callback_handler.py             │ │
│  │  └── bot_main.py                              │ │
│  └───────────────────────────────────────────────┘ │
│                   ↓                                 │
│  ┌───────────────────────────────────────────────┐ │
│  │  UNIFIED DATABASE LAYER                       │ │
│  │  ├── models.py (Supabase tables)              │ │
│  │  ├── supabase_client.py (connection)          │ │
│  │  └── repository.py (CRUD)                     │ │
│  └───────────────────────────────────────────────┘ │
│                   ↓                                 │
│  ┌───────────────────────────────────────────────┐ │
│  │  API SERVER MODULE (from Movieweb)            │ │
│  │  ├── server/routes/movies.py                  │ │
│  │  ├── server/routes/links.py                   │ │
│  │  ├── server/routes/admin.py                   │ │
│  │  └── server/app.py                            │ │
│  └───────────────────────────────────────────────┘ │
│                   ↓                                 │
│  ┌───────────────────────────────────────────────┐ │
│  │  SUPABASE (Cloud Database)                    │ │
│  │  ├── movie_links                              │ │
│  │  ├── quality_movie_links                      │ │
│  │  ├── quality_episodes                         │ │
│  │  ├── quality_zips                             │ │
│  │  ├── api_tokens                               │ │
│  │  ├── admin_settings                           │ │
│  │  └── ad_view_sessions                         │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
         ↑                            ↑
         │                            │
    ┌────┴──────────────────────────┬─┘
    │                               │
  INPUTS(Still separate):      FLOWS TO:
  ├── Tgbot/                   - Same API
  ├── Movieweb/                - Same Database
  │                            - Same Config
  └── (Both run independently)
```

---

## 📝 UPDATED DETAILED STEPS:

### **STEP 1 (PRIORITY): Fix Movieweb Frontend in IntegratedServer**

**Move Movieweb/client/ to IntegratedServer/frontend/:**
- Copy all frontend files (HTML, CSS, JS)
- Update all API calls to use relative URLs (no localhost:5000 needed)
- Remove direct Supabase calls from frontend
- Ensure frontend serves correctly from Flask static routes

**Create: `IntegratedServer/server/routes/frontend.py`**
- Flask routes to serve static files
- Admin dashboard routes
- Movie listing and management pages

### **STEP 2: Create Unified Database Layer**

**Update: `IntegratedServer/database/models.py`**
- Include existing Supabase tables
- Add new unified tables: unified_movies, user_sessions, combined_stats, movie_metadata
- Define data structures for combined bot + web operations

**Update: `IntegratedServer/database/supabase_client.py`**
- Single connection for all operations
- Handle both existing and new tables

**Update: `IntegratedServer/database/repository.py`**
- CRUD operations for all tables
- Unified movie operations (single entry point)
- Combined statistics tracking

### **STEP 3: Merge Tgbot into IntegratedServer**

**Copy Tgbot handlers to `IntegratedServer/bot/`:**
- All handler files
- Update imports to use new repository
- Modify database calls to use Supabase instead of JSON

### **STEP 4: Create Unified Admin Interface**

**Single admin interface in frontend:**
- Add/edit movies (serves both bot and web)
- View combined statistics
- Manage users and sessions
- Single login system

### **STEP 5: Update Main Server**

**Modify: `IntegratedServer/main.py`**
- Run Flask server with frontend routes
- Start Telegram bot in same process
- Single entry point for everything

---

## 🔄 DATA FLOW AFTER INTEGRATION:

### **Adding a Movie (Example):**

```
1. Admin opens Movieweb website
2. Submits form: POST http://localhost:3001/admin
3. Movieweb calls: POST http://localhost:5000/api/movies
4. IntegratedServer receives, validates
5. Stores in Supabase (movie_links table)
6. Returns success to Movieweb
7. Admin bot checks: NEW MOVIE AVAILABLE!
8. Bot posts to Telegram channel with short link
9. User clicks link
10. IntegratedServer serves ad page + redirect
11. User downloads from original source
```

### **Bot Posting (Example):**

```
1. Bot handler checks Supabase for new movies
2. Queries: IntegratedServer/database/repository.get_movies()
3. IntegratedServer queries Supabase
4. Returns movie list
5. Bot formats message with short links
6. Posts to Telegram channel
7. User clicks short link
8. IntegratedServer handling redirect (with ads)
```

---

## ✨ SUPABASE TABLES (No changes needed):

Already have all required tables:

- ✅ movie_links
- ✅ quality_movie_links
- ✅ quality_episodes
- ✅ quality_zips
- ✅ api_tokens
- ✅ admin_settings (`sbiswas1844` / `save@184455`)
- ✅ ad_view_sessions

---

## 🚀 FINAL SETUP: SINGLE TERMINAL ONLY

**Terminal 1: Everything Together**

```bash
cd IntegratedServer
python main.py
# Runs:
# - Flask web server with frontend (port 5000)
# - Telegram bot (polling updates)
# - Unified admin interface
# - All API endpoints
# - Supabase connection for everything
```

**Result:**
- ✅ One terminal runs bot + web + admin
- ✅ One Supabase database for all data
- ✅ Single admin interface for movie management
- ✅ Unified data entry (no duplicates)
- ✅ Frontend properly integrated and working

---

## 📌 KEY POINTS TO REMEMBER:

1. **Tgbot folder stays as-is** - It's reference code
2. **Movieweb folder stays as-is** - It's reference code
3. **ALL CHANGES in IntegratedServer folder ONLY**
4. **No direct Supabase calls** - Go through IntegratedServer API
5. **Shared database** - Both bot and website use same Supabase
6. **Single admin system** - Credentials in Supabase admin_settings

---

## ⚡ NEXT ACTION:

Ready to start **STEP 1: Create Unified Database Layer**?

Confirm: আমি ঠিক পথে আছি কি?
