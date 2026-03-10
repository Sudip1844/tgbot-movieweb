# 📋 Complete Setup Checklist

## Phase 1: Supabase Configuration ⚙️

### Your Action Items:

- [ ] **Create Supabase Project**
  - Go to: https://app.supabase.com
  - Click "New Project"
  - Fill: Project name, Database password, Region
  - Wait 2-3 minutes

- [ ] **Copy Credentials**
  - Settings → API → Copy these:
    - [ ] Project URL: `https://[PROJECT_ID].supabase.co`
    - [ ] Anon Public Key: `eyJ...`
    - [ ] Service Role Key: `eyJ...` (KEEP SECRET!)

- [ ] **Get Database Info**
  - Settings → Database → Copy:
    - [ ] Host: `[PROJECT_ID].supabase.co`
    - [ ] Port: `5432`
    - [ ] Database: `postgres`
    - [ ] User: `postgres`
    - [ ] Password: [Same as project creation]

- [ ] **Run SQL Schema**
  - Go to: SQL Editor
  - New Query
  - Copy from: `SUPABASE_SQL_SCHEMA.sql`
  - Paste and Run
  - Verify: All 7 tables created

---

## Phase 2: IntegratedServer Setup ✅ (DONE)

### Completed:

- [x] Folder structure created
- [x] requirements.txt prepared
- [x] config.py created
- [x] Database models (SQLAlchemy)
- [x] Flask app setup
- [x] Entry point (main.py)
- [x] .gitignore created
- [x] README.md created

---

## Phase 3: Your Configuration 🔧

### Create `.IntegratedServer/.env` file:

```bash
cd IntegratedServer

# Windows:
copy .env.example .env

# Edit .env with these values (from Supabase):

SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
SUPABASE_DB_HOST=YOUR_PROJECT_ID.supabase.co
SUPABASE_DB_PASSWORD=YOUR_DB_PASSWORD
```

---

## Phase 4: Test Connection 🧪

```bash
cd IntegratedServer

# Activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test database connection
python -c "from database import init_db; init_db()"

# Expected output:
# ✅ Database engine created successfully
# ✅ Database tables initialized
```

---

## Phase 5: Start Server 🚀

```bash
cd IntegratedServer

# Activate venv (if not already)
.\venv\Scripts\activate

# Run server
python main.py

# Expected output:
# ╔═══════════════════════════════════════════════════════════╗
# ║         MovieZone - Integrated Server                     ║
# ║     Telegram Bot + Web Server (Unified Python)            ║
# ╚═══════════════════════════════════════════════════════════╝
#
# 🌐 Flask Server: http://0.0.0.0:5000
# 📊 Access API at: http://localhost:5000/api
```

Test: Open http://localhost:5000 in browser

---

## Phase 6: Test API Endpoints 🌐

```bash
# Health Check
curl http://localhost:5000/api/health

# Expected response:
# {
#   "status": "ok",
#   "message": "Server is running",
#   "timestamp": "2024-03-08T12:00:00.000000"
# }
```

---

## Phase 7: Git Configuration 🔒

### Remove Original Repo Links:

```powershell
# Option 1: Remove .git folders
Remove-Item -Path "d:\vs code use\tgbot+movieweb\Tgbot\.git" -Recurse -Force
Remove-Item -Path "d:\vs code use\tgbot+movieweb\Movieweb\.git" -Recurse -Force
```

### Setup New Repository (AFTER completion):

```bash
cd d:\vs code use\tgbot+movieweb

# Initialize new repo
git init

# Add only IntegratedServer
git add IntegratedServer/

# Create initial commit
git commit -m "Initial: Integrated MovieZone server"

# Add remote (create repo on GitHub first)
git remote add origin https://github.com/YOUR_USERNAME/MovieZone-Integrated.git

# Push to GitHub
git push -u origin main
```

---

## 📦 Next Phases (Coming Soon)

- [ ] **Phase 8**: Telegram Bot Integration
- [ ] **Phase 9**: API Routes Implementation
- [ ] **Phase 10**: React Frontend Build & Serve
- [ ] **Phase 11**: Advanced Features (Auth, Ads, etc)

---

## 🆘 Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'flask'`

**Solution**: Make sure venv is activated and requirements installed

```bash
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: `SUPABASE_URL not configured`

**Solution**: Check `.env` file exists and has correct values

```bash
type .env
```

### Problem: Database connection failed

**Solution**: Verify credentials in `.env`

```bash
# Test manually:
python -c "from config import DATABASE_URL; print(DATABASE_URL)"
```

### Problem: Port 5000 already in use

**Solution**: Change port in `.env`

```
FLASK_PORT=5001
```

---

## 📞 What to Provide Next

When you're ready, provide these from Supabase:

```
1. SUPABASE_URL =
2. SUPABASE_ANON_KEY =
3. SUPABASE_SERVICE_ROLE_KEY =
4. SUPABASE_DB_PASSWORD =
5. SUPABASE_DB_HOST =
```

Then I'll:

- Help you create `.env` file
- Test database connection
- Verify all API endpoints
- Start building API routes

---

**Status**: ✅ Ready for Supabase configuration!
