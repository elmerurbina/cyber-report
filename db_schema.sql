-- Drop existing tables if they exist (to avoid conflicts during setup)
DROP TABLE IF EXISTS reports, users CASCADE;

-- Create users table (anonymous reporting, but users might still exist for admin moderation)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create reports table (stores reported phone numbers, emails, URLs, etc.)
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    report_type VARCHAR(50) NOT NULL,  -- "phone", "email", "url", "site", etc.
    value TEXT NOT NULL,  -- The actual phone number, email, or URL
    description TEXT,  -- Additional information about the report
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT REFERENCES users(id) ON DELETE SET NULL
);

-- ===========================
-- ✅ CREATE PROCEDURE (INSERT)
-- ===========================
CREATE OR REPLACE PROCEDURE insert_report(
    p_report_type VARCHAR,
    p_value TEXT,
    p_description TEXT,
    p_user_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO reports (report_type, value, description, user_id)
    VALUES (p_report_type, p_value, p_description, p_user_id);
END;
$$;

-- ===========================
-- ✅ CREATE FUNCTION (READ)
-- ===========================
CREATE OR REPLACE FUNCTION get_reports()
RETURNS TABLE(id INT, report_type VARCHAR, value TEXT, description TEXT, reported_at TIMESTAMP, user_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT * FROM reports;
END;
$$;

-- Get reports by type
CREATE OR REPLACE FUNCTION get_reports_by_type(p_report_type VARCHAR)
RETURNS TABLE(id INT, value TEXT, description TEXT, reported_at TIMESTAMP, user_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT id, value, description, reported_at, user_id FROM reports WHERE report_type = p_report_type;
END;
$$;

-- ===========================
-- ✅ CREATE PROCEDURE (UPDATE)
-- ===========================
CREATE OR REPLACE PROCEDURE update_report(
    p_id INT,
    p_description TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE reports SET description = p_description WHERE id = p_id;
END;
$$;

-- ===========================
-- ✅ CREATE PROCEDURE (DELETE)
-- ===========================
CREATE OR REPLACE PROCEDURE delete_report(p_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM reports WHERE id = p_id;
END;
$$;

-- ===========================
-- ✅ CREATE FUNCTION (SEARCH)
-- ===========================
CREATE OR REPLACE FUNCTION search_reports(p_query TEXT)
RETURNS TABLE(id INT, report_type VARCHAR, value TEXT, description TEXT, reported_at TIMESTAMP, user_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT id, report_type, value, description, reported_at, user_id
    FROM reports
    WHERE value ILIKE '%' || p_query || '%'
       OR description ILIKE '%' || p_query || '%';
END;
$$;