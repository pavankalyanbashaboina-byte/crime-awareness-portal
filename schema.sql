<<<<<<< HEAD
-- ============================================================
-- Crime Awareness Portal - Supabase Database Schema
-- Run this in your Supabase SQL Editor
-- ============================================================

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id          BIGSERIAL PRIMARY KEY,
    user_id     TEXT UNIQUE NOT NULL,
    role        TEXT NOT NULL CHECK (role IN ('student', 'faculty', 'admin')),
    password_hash TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Reports table
CREATE TABLE IF NOT EXISTS reports (
    id             BIGSERIAL PRIMARY KEY,
    accused_name   TEXT NOT NULL,
    department     TEXT NOT NULL,
    violation_type TEXT NOT NULL,
    description    TEXT NOT NULL,
    anonymous      BOOLEAN DEFAULT FALSE,
    reported_by    TEXT,
    reporter_role  TEXT,
    status         TEXT NOT NULL DEFAULT 'pending'
                   CHECK (status IN ('pending', 'under_review', 'resolved')),
    created_at     TIMESTAMPTZ DEFAULT NOW()
);

-- ── Seed admin user (password: admin123) ──────────────────────
-- Generate your own hash via Python:
--   import bcrypt; print(bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode())
-- Then replace the hash below and run this INSERT:

-- INSERT INTO users (user_id, role, password_hash) VALUES
-- ('admin001', 'admin', '$2b$12$REPLACE_WITH_YOUR_BCRYPT_HASH');

-- ── Row Level Security (optional but recommended) ─────────────
-- ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
=======
-- ============================================================
-- Crime Awareness Portal - Supabase Database Schema
-- Run this in your Supabase SQL Editor
-- ============================================================

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id          BIGSERIAL PRIMARY KEY,
    user_id     TEXT UNIQUE NOT NULL,
    role        TEXT NOT NULL CHECK (role IN ('student', 'faculty', 'admin')),
    password_hash TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Reports table
CREATE TABLE IF NOT EXISTS reports (
    id             BIGSERIAL PRIMARY KEY,
    accused_name   TEXT NOT NULL,
    department     TEXT NOT NULL,
    violation_type TEXT NOT NULL,
    description    TEXT NOT NULL,
    anonymous      BOOLEAN DEFAULT FALSE,
    reported_by    TEXT,
    reporter_role  TEXT,
    status         TEXT NOT NULL DEFAULT 'pending'
                   CHECK (status IN ('pending', 'under_review', 'resolved')),
    created_at     TIMESTAMPTZ DEFAULT NOW()
);

-- ── Seed admin user (password: admin123) ──────────────────────
-- Generate your own hash via Python:
--   import bcrypt; print(bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode())
-- Then replace the hash below and run this INSERT:

-- INSERT INTO users (user_id, role, password_hash) VALUES
-- ('admin001', 'admin', '$2b$12$REPLACE_WITH_YOUR_BCRYPT_HASH');

-- ── Row Level Security (optional but recommended) ─────────────
-- ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
>>>>>>> 99548e130a923a9864ad0e8fcb481a2110430117
-- ALTER TABLE users   ENABLE ROW LEVEL SECURITY;