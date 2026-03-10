# 🔧 Supabase Configuration Checklist

## ✅ Your Task - Step by Step

### Step 1: Create New Supabase Project

```
1. Go to: https://app.supabase.com
2. Click "New Project"
3. Choose:
   - Organization: Your org
   - Name: "MovieZone-Integrated"
   - Database Password: [Create strong password]
   - Region: [Your closest region]
   - Pricing: Free tier (OK for testing)
4. Wait ~2 minutes for project to initialize
```

### Step 2: Copy Project Details

After project initializes, go to **Settings → API** and copy:

```
┌─────────────────────────────────────────────────────┐
│ PROJECT DETAILS (FROM SUPABASE DASHBOARD)           │
├─────────────────────────────────────────────────────┤
│                                                     │
│ 1. Project URL:                                     │
│    https://[YOUR_PROJECT_ID].supabase.co           │
│    Provide: [___________________________]          │
│                                                     │
│ 2. Anon Public Key (for frontend):                 │
│    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...        │
│    Provide: [___________________________]          │
│                                                     │
│ 3. Service Role Key (for backend - SECRET!):       │
│    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...        │
│    Provide: [___________________________]          │
│                                                     │
│ 4. Database Host (Settings → Database):            │
│    [PROJECT_ID].supabase.co                       │
│    Provide: [___________________________]          │
│                                                     │
│ 5. Database Port:                                   │
│    5432 (default)                                   │
│                                                     │
│ 6. Database Name:                                   │
│    postgres (default)                               │
│                                                     │
│ 7. Database User:                                   │
│    postgres                                         │
│                                                     │
│ 8. Database Password:                               │
│    [Same as created in Step 1]                      │
│    Provide: [___________________________]          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Step 3: Setup Database Schema

After project is active:

1. Go to **SQL Editor**
2. Click **New Query**
3. Copy all content from: `SUPABASE_SQL_SCHEMA.sql`
4. Paste in SQL Editor
5. Click **Run**
6. Wait for success message

**Tables Created:**

- ✅ `movie_links`
- ✅ `quality_movie_links`
- ✅ `quality_episodes`
- ✅ `quality_zips`
- ✅ `api_tokens`
- ✅ `admin_settings` (with default: sbiswas1844 / save@184455)
- ✅ `ad_view_sessions`

### Step 4: Verify Tables

In Supabase dashboard:

1. Go to **Table Editor**
2. Should see all 7 tables in left sidebar
3. Click `admin_settings` → should see 1 row with your credentials

---

## 📋 Supabase Configuration Form

**আমাকে এই তথ্য দিয়ে দিন:**

```
Project URL:
Anon Key:
Service Role Key:
Database Password:
Database Host:
(Other details auto-filled)
```

---

## 🔐 Security Notes

### ⚠️ NEVER Share:

- Service Role Key
- Database Password
- These go ONLY in backend `.env`

### ✅ Frontend can use:

- Anon Public Key (it's public)
- Project URL

---

## 🧪 Quick Test (After Setup)

Once Supabase is ready:

```sql
-- In Supabase SQL Editor, check admin settings:
SELECT * FROM admin_settings;

-- Should return:
-- admin_id: sbiswas1844
-- admin_password: save@184455
```

---

## ⚡ Next Steps After You Provide Keys

1. I'll create `.env` file
2. I'll setup Python connection to Supabase
3. I'll create database models
4. We can test API endpoints

**Ready? Provide the information above!** ⬆️
