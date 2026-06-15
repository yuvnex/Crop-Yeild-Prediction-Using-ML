from flask import Flask, render_template, session, redirect, url_for
from backend.auth import auth_bp
from backend.admin import admin_bp
from backend.prediction import prediction_bp
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'super_secret_key_for_crop_yield_prediction'

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(prediction_bp, url_prefix='/predict')

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html', user_name=session.get('user_name'))

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('database', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('dataset', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
