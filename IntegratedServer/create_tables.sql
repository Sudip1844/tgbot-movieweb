-- ====================================
-- MovieZone Unified Tables
-- Run this in Supabase SQL Editor
-- ====================================

-- DROP OLD TABLES
DROP TABLE IF EXISTS ad_view_sessions CASCADE;
DROP TABLE IF EXISTS api_tokens CASCADE;
DROP TABLE IF EXISTS admin_settings CASCADE;
DROP TABLE IF EXISTS quality_zips CASCADE;
DROP TABLE IF EXISTS quality_episodes CASCADE;
DROP TABLE IF EXISTS quality_movie_links CASCADE;
DROP TABLE IF EXISTS movie_links CASCADE;
DROP TABLE IF EXISTS movie_reviews CASCADE;
DROP TABLE IF EXISTS movies CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS admin_accounts CASCADE;
DROP TABLE IF EXISTS channels CASCADE;
DROP TABLE IF EXISTS movie_requests CASCADE;
DROP TABLE IF EXISTS monthly_stats CASCADE;

-- ====================================
-- MOVIES - Unified movie data
-- ====================================
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    categories TEXT[] DEFAULT '{}',
    languages TEXT[] DEFAULT '{}',
    release_year TEXT DEFAULT 'N/A',
    runtime TEXT DEFAULT 'N/A',
    imdb_rating TEXT DEFAULT 'N/A',
    thumbnail_file_id TEXT,
    download_type TEXT NOT NULL DEFAULT 'single',
    original_link TEXT,
    quality_480p TEXT,
    quality_720p TEXT,
    quality_1080p TEXT,
    episodes JSONB,
    start_from_episode INTEGER DEFAULT 1,
    from_episode INTEGER,
    to_episode INTEGER,
    short_id TEXT UNIQUE,
    status TEXT DEFAULT 'pending',
    views INTEGER DEFAULT 0,
    downloads INTEGER DEFAULT 0,
    ads_enabled BOOLEAN DEFAULT TRUE,
    added_by TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ====================================
-- USERS - Telegram bot users
-- ====================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    first_name TEXT,
    username TEXT,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ====================================
-- ADMIN_ACCOUNTS - Website admin logins
-- ====================================
CREATE TABLE admin_accounts (
    id SERIAL PRIMARY KEY,
    admin_id TEXT UNIQUE NOT NULL,
    admin_password TEXT NOT NULL,
    display_name TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_by TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ====================================
-- CHANNELS - Managed Telegram channels
-- ====================================
CREATE TABLE channels (
    id SERIAL PRIMARY KEY,
    channel_id TEXT UNIQUE NOT NULL,
    channel_name TEXT NOT NULL,
    short_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ====================================
-- MOVIE_REQUESTS - User movie requests
-- ====================================
CREATE TABLE movie_requests (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    movie_name TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ====================================
-- AD_VIEW_SESSIONS - Ad tracking
-- ====================================
CREATE TABLE ad_view_sessions (
    id SERIAL PRIMARY KEY,
    ip_address TEXT NOT NULL,
    short_id TEXT NOT NULL,
    link_type TEXT DEFAULT 'single',
    viewed_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(ip_address, short_id, link_type)
);

-- ====================================
-- MONTHLY_STATS - Statistics
-- ====================================
CREATE TABLE monthly_stats (
    id SERIAL PRIMARY KEY,
    month_year TEXT UNIQUE NOT NULL,
    movies_added INTEGER DEFAULT 0,
    total_downloads INTEGER DEFAULT 0,
    total_views INTEGER DEFAULT 0,
    top_movies JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ====================================
-- Insert default owner
-- ====================================
INSERT INTO admin_accounts (admin_id, admin_password, display_name, is_active, created_by)
VALUES ('sbiswas1844', 'save@184455', 'Owner', TRUE, 'system')
ON CONFLICT (admin_id) DO NOTHING;

INSERT INTO users (user_id, first_name, role)
VALUES (5379553841, 'Owner', 'owner')
ON CONFLICT (user_id) DO NOTHING;

-- Enable Row Level Security (recommended)
ALTER TABLE movies ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE channels ENABLE ROW LEVEL SECURITY;
ALTER TABLE movie_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE ad_view_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE monthly_stats ENABLE ROW LEVEL SECURITY;

-- Allow service role full access
CREATE POLICY "service_role_all" ON movies FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON users FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON admin_accounts FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON channels FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON movie_requests FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON ad_view_sessions FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON monthly_stats FOR ALL USING (true) WITH CHECK (true);