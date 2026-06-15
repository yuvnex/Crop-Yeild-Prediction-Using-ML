CREATE DATABASE IF NOT EXISTS crop_yield_db;
USE crop_yield_db;

CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    crop_name VARCHAR(100),
    soil_type VARCHAR(100),
    temperature FLOAT,
    rainfall FLOAT,
    humidity FLOAT,
    fertilizer FLOAT,
    irrigation FLOAT,
    area FLOAT,
    predicted_yield FLOAT,
    yield_category VARCHAR(50),
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- Insert a default admin user (password: admin123 hashed if using werkzeug.security, but we'll insert a plain/hashed one via python init script or let admin login handle it. Let's just create it via python)
