# TGBot + MovieWeb Integrated Project

An integrated solution combining a Telegram Bot, Movie Web Application, and a unified backend server with Supabase database.

## 📁 Project Structure

```
├── Tgbot/                 # Telegram Bot using python-telegram-bot
├── Movieweb/              # Full-stack web app (React frontend + Express backend)
├── IntegratedServer/      # Flask API server + shared admin panel
└── docs/                  # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 16+
- Supabase Account

### 1. Setup Telegram Bot (Tgbot/)

```bash
cd Tgbot
pip install -r requirements.txt
python main.py
```

### 2. Setup MovieWeb Application (Movieweb/)

```bash
cd Movieweb
npm install
npm run dev
```

The app runs on `http://localhost:3001`

### 3. Setup Integrated Server (IntegratedServer/)

```bash
cd IntegratedServer
pip install -r requirements.txt
python main.py
```

The server runs on `http://localhost:5000`

## 🔐 Admin Access

**Admin Panel:** `http://localhost:5000/admin.html`

**Credentials:**

- ID: `sbiswas1844`
- Password: `save@184455`

## 🗄️ Database

**Supabase URL:** `https://xgkkdfxfyznbzaqicpkp.supabase.co`

Tables:

- `movie_links` - Movie information and links
- `admin_settings` - Admin configuration
- `users` - User data
- And more...

## 📚 Key Files

### Tgbot/

- `main.py` - Bot entry point
- `config.py` - Bot token and configuration
- `handlers/` - Command handlers

### Movieweb/

- `client/` - React frontend
- `server/` - Express backend
- `.env` - Environment variables (localhost URLs)

### IntegratedServer/

- `main.py` - Flask server entry point
- `config.py` - Admin credentials
- `static/admin.html` - Admin panel

## 🔗 API Endpoints

### Frontend → Backend

- Frontend: `http://localhost:3001`
- Backend: `http://localhost:5000`

### Bot Integration

- Bot reads from Supabase
- Bot sends updates to Telegram users

## ⚙️ Environment Variables

### Movieweb/.env

```
FRONTEND_URL=http://localhost:3001
BACKEND_URL=http://localhost:5000
```

### IntegratedServer/.env

```
SUPABASE_URL=https://xgkkdfxfyznbzaqicpkp.supabase.co
SUPABASE_KEY=[your_key]
```

## 🛠️ Development

All three services run simultaneously:

1. Terminal 1: `cd Tgbot && python main.py`
2. Terminal 2: `cd Movieweb && npm run dev`
3. Terminal 3: `cd IntegratedServer && python main.py`

## 📝 License

Private Project

## 👤 Author

Created for Telegram Bot + Movie Website Integration
