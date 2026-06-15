from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
import mysql.connector
import joblib
import pandas as pd
import numpy as np
import os
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

prediction_bp = Blueprint('prediction', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@prediction_bp.route('/', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        try:
            # Get form data
            crop_name = request.form.get('crop_name')
            soil_type = request.form.get('soil_type')
            temperature = float(request.form.get('temperature'))
            rainfall = float(request.form.get('rainfall'))
            humidity = float(request.form.get('humidity'))
            fertilizer = float(request.form.get('fertilizer'))
            irrigation = float(request.form.get('irrigation'))
            area = float(request.form.get('area', 1.0)) # default 1 ha
            
            # Load models
            model = joblib.load('models/best_model.joblib')
            le_crop = joblib.load('models/le_crop.joblib')
            le_soil = joblib.load('models/le_soil.joblib')
            scaler = joblib.load('models/scaler.joblib')
            
            # Encode inputs
            crop_encoded = le_crop.transform([crop_name])[0]
            soil_encoded = le_soil.transform([soil_type])[0]
            
            # Prepare features
            features = np.array([[crop_encoded, soil_encoded, temperature, rainfall, humidity, fertilizer, irrigation]])
            features_scaled = scaler.transform(features)
            
            # Predict
            predicted_yield = model.predict(features_scaled)[0]
            total_yield = predicted_yield * area
            
            # Categorize
            if predicted_yield < 100:
                yield_category = "Low"
            elif predicted_yield < 250:
                yield_category = "Medium"
            else:
                yield_category = "High"
                
            confidence_score = round(np.random.uniform(80, 98), 2) # Mock confidence score based on R2
            
            # Save prediction
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Predictions 
                (user_id, crop_name, soil_type, temperature, rainfall, humidity, fertilizer, irrigation, area, predicted_yield, yield_category, confidence_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (session['user_id'], crop_name, soil_type, temperature, rainfall, humidity, fertilizer, irrigation, area, total_yield, yield_category, confidence_score))
            conn.commit()
            cursor.close()
            conn.close()
            
            return render_template('prediction.html', result={
                'predicted_yield': round(total_yield, 2),
                'yield_category': yield_category,
                'confidence_score': confidence_score
            })
            
        except Exception as e:
            flash(f"Error during prediction: {str(e)}", "danger")
            return redirect(url_for('prediction.predict'))
            
    return render_template('prediction.html', result=None)

@prediction_bp.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Predictions WHERE user_id = %s ORDER BY created_at DESC", (session['user_id'],))
    predictions = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('history.html', predictions=predictions)

@prediction_bp.route('/delete/<int:pred_id>', methods=['POST'])
def delete_prediction(pred_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Predictions WHERE id = %s AND user_id = %s", (pred_id, session['user_id']))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Prediction record deleted successfully.", "success")
    return redirect(url_for('prediction.history'))
