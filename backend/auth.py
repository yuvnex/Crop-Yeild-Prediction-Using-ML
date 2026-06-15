from flask import Blueprint, request, render_template, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

auth_bp = Blueprint('auth', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'user')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        if role == 'admin':
            cursor.execute("SELECT * FROM Admin WHERE username = %s", (email,))
            admin = cursor.fetchone()
            if admin and check_password_hash(admin['password'], password):
                session['admin_id'] = admin['id']
                session['admin_username'] = admin['username']
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Invalid admin credentials', 'danger')
        else:
            cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'danger')
                
        cursor.close()
        conn.close()
        
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    hashed_password = generate_password_hash(password)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO Users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        conn.commit()
        flash('Registration successful! Please login.', 'success')
    except mysql.connector.IntegrityError:
        flash('Email already exists!', 'danger')
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
