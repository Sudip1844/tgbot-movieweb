# 🚀 Integrated Project - Implementation Roadmap

## 📋 Final Architecture

```
d:\vs code use\tgbot+movieweb/
├── Tgbot/                    # ✅ Original Telegram Bot (NO EDITS)
│   ├── main.py
│   ├── config.py
│   ├── handlers/
│   ├── data/
│   └── .git (ORIGINAL REPO)
│
├── Movieweb/                 # ✅ Original Website (NO EDITS)
│   ├── server/
│   ├── client/
│   ├── package.json
│   └── .git (ORIGINAL REPO)
│
└── IntegratedServer/         # 🆕 NEW UNIFIED PYTHON SERVER
    ├── .git (NEW REPO - ONLY THIS TO PUSH)
    ├── requirements.txt
    ├── main.py               # Entry point
    ├── config.py             # Unified config
    ├── bot/                  # Bot logic (modified from Tgbot/)
    │   ├── __init__.py
    │   ├── bot_main.py
    │   ├── handlers/
    │   └── ...
    ├── server/               # Web Server (converted from Node to Python)
    │   ├── __init__.py
    │   ├── app.py           # Flask/FastAPI main
    │   ├── routes/
    │   │   ├── movies.py
    │   │   ├── shorts.py
    │   │   ├── redirect.py
    │   │   ├── admin.py
    │   │   └── health.py
    │   ├── middleware.py
    │   └── database.py
    ├── database/
    │   ├── models.py        # SQLAlchemy models
    │   ├── supabase_client.py
    │   └── migrations/
    └── static/              # React build (serve from sever)
        └── dist/            # Built React files
```

## 🔑 Port Configuration

- **Python Server**: `http://localhost:5000`
  - API endpoints: `/api/movies`, `/api/shorts`, `/api/redirect`, etc.
  - Static files (React build): `/` (root)
- **React Development Frontend**: `http://localhost:3000` (during development)
  - After build: served from Python server

- **Telegram Bot**: No port needed (uses Telegram Bot API)

---

## 📦 Database Tables (Supabase)

### Tables Structure

```
✅ movie_links          - Single movie downloads
✅ quality_movie_links  - Multi-quality movies (480p/720p/1080p)
✅ quality_episodes     - Series with episodes (JSON format)
✅ quality_zips         - Episode range downloads
✅ api_tokens           - API authentication tokens
✅ admin_settings       - Admin credentials (sbiswas1844 / save@184455)
✅ ad_view_sessions     - IP-based 5-min timer for ads
```

---

## 🛠️ Supabase Setup Required

###你有的 Information:

```
Admin ID: sbiswas1844
Admin Password: save@184455
```

### Next Steps - You Need to Provide:

1. **New Supabase Project URL**
   - Format: `https://[PROJECT_ID].supabase.co`
   - Example: `https://abcdef123456.supabase.co`

2. **Supabase API Keys**
   - Anon Public Key: `eyJhbG...` (starts with ey)
   - Service Role Key: `eyJhbG...` (starts with ey, secret!)

3. **Supabase Connection String** (optional)
   - Format: `postgresql://user:password@host:port/database`

4. **Database Name** (usually `postgres`)

### How to Get These:

1. Go to Supabase Dashboard: https://app.supabase.com
2. Create new project
3. Settings → API → Copy:
   - `Project URL`
   - `anon public` (for frontend)
   - `service_role` (for backend - KEEP SECRET!)

---

## 📝 Environment Variables

`.env` file you need to create:

```env
# Flask/Server Config
FLASK_ENV=development
FLASK_PORT=5000
DEBUG=True

# Supabase (You'll provide these)
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIs...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIs...
SUPABASE_DB_PASSWORD=your_db_password

# Telegram Bot Config
BOT_TOKEN=7489158288:AAG3r41T8kG4O01BpBeICApd28p9g4DJJ4A
BOT_USERNAME=MoviezoneDownloadbot
OWNER_ID=5379553841
AD_PAGE_URL=https://sudip1844.github.io/moviezone-redirect-page-

# Admin Credentials
ADMIN_ID=sbiswas1844
ADMIN_PASSWORD=save@184455

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5000
```

---

## 🔒 Git Configuration Strategy

### DO NOT PUSH TO:

- `d:\vs code use\tgbot+movieweb\Tgbot\.git`
- `d:\vs code use\tgbot+movieweb\Movieweb\.git`

### DISCONNECTING ORIGINAL REPOS:

```powershell
# Remove .git from original folders
Remove-Item -Path "d:\vs code use\tgbot+movieweb\Tgbot\.git" -Recurse -Force
Remove-Item -Path "d:\vs code use\tgbot+movieweb\Movieweb\.git" -Recurse -Force
```

### NEW REPO - AFTER COMPLETION:

```powershell
cd d:\vs code use\tgbot+movieweb
git init
git add IntegratedServer/
git commit -m "Initial integrated project setup"
git remote add origin https://github.com/YourUsername/MovieZone-Integrated.git
git push -u origin main
```

---

## 📊 Implementation Phases

### Phase 1: Setup ✅

- [x] Extract both repos
- [ ] Create IntegratedServer directory structure
- [ ] Create `requirements.txt` with all dependencies

### Phase 2: Configuration

- [ ] Create `.env` file (awaiting Supabase details)
- [ ] Setup Supabase with SQL schema
- [ ] Configure Flask/FastAPI server

### Phase 3: Backend Conversion (Node → Python)

- [ ] Convert `server/routes.ts` → Python routes
- [ ] Create SQLAlchemy models from Supabase schema
- [ ] Implement API endpoints in Python

### Phase 4: Integration

- [ ] Integrate Telegram Bot with new server
- [ ] Database layer implementation
- [ ] API testing

### Phase 5: Frontend

- [ ] Build React app
- [ ] Serve from Python server on `/`

### Phase 6: Final

- [ ] Testing
- [ ] Create new GitHub repo
- [ ] Push IntegratedServer only

---

## 🎯 What You Need to Do First

Please provide:

1. **Supabase Project Details**:
   - Project URL: `https://...supabase.co`
   - Anon Key: `eyJ...`
   - Service Role Key: `eyJ...`

2. **Any other API keys/configs** needed

Then I'll:

- Create complete IntegratedServer structure
- Setup all Python files
- Create requirements.txt
- Generate .env template
- You run Supabase SQL script once

---

## 📌 Important Notes

- Tgbot and Movieweb ফোল্ডার কখনো edit করব না
- শুধুমাত্র IntegratedServer-এ কাজ করব
- Final push-এ শুধু IntegratedServer যাবে new repo-তে
