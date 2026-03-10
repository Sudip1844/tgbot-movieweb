# IntegratedServer/config.py
# Centralized Configuration for entire application

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# ============================================
# FLASK CONFIGURATION
# ============================================

# CORS
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')

class Config:
    """Base configuration"""
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Server
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))

# ============================================
# TELEGRAM BOT CONFIGURATION
# ============================================

BOT_TOKEN = os.getenv('BOT_TOKEN', '')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'MoviezoneDownloadbot')
OWNER_ID = int(os.getenv('OWNER_ID', 0))
AD_PAGE_URL = os.getenv('AD_PAGE_URL', 'https://sudip1844.github.io/moviezone-redirect-page-')

# Bot Categories
ADMIN_CATEGORIES = [
    "Bollywood 🇮🇳", "Hollywood 🇺🇸", "South Indian 🎬", "Web Series 🎥",
    "Bengali ✨", "Anime & cartoon 🌀", "Comedy 🤣", "Action 💥",
    "Romance 💑", "Horror 😱", "Thriller 🔍", "Sci-Fi 🛸",
    "K-Drama 🎎", "18+ 🔞", "Hentai 💦"
]

BROWSE_CATEGORIES = [
    "All 🌐", "Bollywood 🇮🇳", "Hollywood 🇺🇸", "South Indian 🎬", "Web Series 🎥",
    "Bengali ✨", "Anime & cartoon 🌀", "Comedy 🤣", "Action 💥",
    "Romance 💑", "Horror 😱", "Thriller 🔍", "Sci-Fi 🛸",
    "K-Drama 🎎", "18+ 🔞", "Hentai 💦"
]

LANGUAGES = [
    "Bengali", "Hindi", "English", "Tamil", "Telugu", "Korean", "Gujarati"
]

CONVERSATION_TIMEOUT = 600  # 10 minutes

# ============================================
# SUPABASE CONFIGURATION
# ============================================

SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY', '')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')
SUPABASE_DB_HOST = os.getenv('SUPABASE_DB_HOST', '')
SUPABASE_DB_NAME = os.getenv('SUPABASE_DB_NAME', 'postgres')
SUPABASE_DB_USER = os.getenv('SUPABASE_DB_USER', 'postgres')
SUPABASE_DB_PASSWORD = os.getenv('SUPABASE_DB_PASSWORD', '')
SUPABASE_DB_PORT = int(os.getenv('SUPABASE_DB_PORT', 5432))

# Database connection string for SQLAlchemy
DATABASE_URL = f"postgresql://{SUPABASE_DB_USER}:{SUPABASE_DB_PASSWORD}@{SUPABASE_DB_HOST}:{SUPABASE_DB_PORT}/{SUPABASE_DB_NAME}"

# ============================================
# ADMIN CONFIGURATION
# ============================================

ADMIN_ID = os.getenv('ADMIN_ID', 'sbiswas1844')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'save@184455')

# ============================================
# API CONFIGURATION
# ============================================

API_PREFIX = '/api'
SHORT_ID_LENGTH = 6

# ============================================
# Logging
# ============================================

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if not BOT_TOKEN:
    logger.warning("⚠️ BOT_TOKEN not configured!")
if not SUPABASE_URL:
    logger.warning("⚠️ SUPABASE_URL not configured!")
