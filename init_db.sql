-- init.sql

-- Connect to the dev_db database
\c dev_db

-- Create schema
CREATE SCHEMA IF NOT EXISTS app_schema AUTHORIZATION root_user;

-- Quit the database
\q
