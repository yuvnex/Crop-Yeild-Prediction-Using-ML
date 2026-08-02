import os

# Database Configuration
# These read from environment variables first (useful for Render deployment),
# and fall back to your local MySQL setup if the variables aren't set.
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "Yuvanesh26#") 
DB_NAME = os.environ.get("DB_NAME", "crop_yield_db")
