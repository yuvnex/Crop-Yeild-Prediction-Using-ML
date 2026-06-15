from flask import Blueprint, render_template, redirect, url_for, session
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

admin_bp = Blueprint('admin', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@admin_bp.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('auth.login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) as total_users FROM Users")
    total_users = cursor.fetchone()['total_users']
    
    cursor.execute("SELECT COUNT(*) as total_predictions FROM Predictions")
    total_predictions = cursor.fetchone()['total_predictions']
    
    cursor.execute("SELECT crop_name, COUNT(*) as count FROM Predictions GROUP BY crop_name ORDER BY count DESC LIMIT 5")
    top_crops = cursor.fetchall()
    
    # Get recent predictions
    cursor.execute("SELECT p.*, u.name as user_name FROM Predictions p JOIN Users u ON p.user_id = u.id ORDER BY p.created_at DESC LIMIT 10")
    recent_predictions = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('admin_dashboard.html', 
                           total_users=total_users, 
                           total_predictions=total_predictions,
                           top_crops=top_crops,
                           recent_predictions=recent_predictions)
