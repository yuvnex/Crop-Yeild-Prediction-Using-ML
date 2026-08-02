import mysql.connector
import os
import sys
from werkzeug.security import generate_password_hash

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

def init_database():
    try:
        # Connect without specific database to create it
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # Read schema
        with open('database/schema.sql', 'r') as f:
            sql_file = f.read()
            
        sql_commands = sql_file.split(';')
        for command in sql_commands:
            if command.strip():
                cursor.execute(command)
                
        conn.commit()
        print("Database 'crop_yield_db' created and tables initialized successfully.")
        
        # Insert default admin
        cursor.execute("USE crop_yield_db")
        cursor.execute("SELECT * FROM Admin WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        if not admin:
            admin_pwd = generate_password_hash("admin123")
            cursor.execute("INSERT INTO Admin (username, password) VALUES (%s, %s)", ('admin', admin_pwd))
            conn.commit()
            print("Default admin created (username: admin, password: admin123)")
            
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    init_database()
