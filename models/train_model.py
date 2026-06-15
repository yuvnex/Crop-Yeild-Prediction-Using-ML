import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def train_and_evaluate():
    print("Loading dataset...")
    df = pd.read_csv('dataset/crop_data.csv')
    
    # Preprocessing
    print("Preprocessing data...")
    # Label Encoding for categorical variables
    le_crop = LabelEncoder()
    le_soil = LabelEncoder()
    
    df['Crop_Name_Encoded'] = le_crop.fit_transform(df['Crop_Name'])
    df['Soil_Type_Encoded'] = le_soil.fit_transform(df['Soil_Type'])
    
    # Save encoders
    os.makedirs('models', exist_ok=True)
    joblib.dump(le_crop, 'models/le_crop.joblib')
    joblib.dump(le_soil, 'models/le_soil.joblib')
    
    # Features and Target
    X = df[['Crop_Name_Encoded', 'Soil_Type_Encoded', 'Temperature', 'Rainfall', 'Humidity', 'Fertilizer', 'Irrigation']]
    y = df['Yield']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Feature scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    joblib.dump(scaler, 'models/scaler.joblib')
    
    # Models
    models = {
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    results = []
    best_model = None
    best_r2 = -float('inf')
    best_model_name = ""
    
    print("Training models...")
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results.append({
            'Model': name,
            'RMSE': rmse,
            'MAE': mae,
            'R2 Score': r2
        })
        
        if r2 > best_r2:
            best_r2 = r2
            best_model = model
            best_model_name = name
            
    # Display results
    results_df = pd.DataFrame(results)
    print("\nModel Comparison:")
    print(results_df.to_string(index=False))
    
    print(f"\nBest Model selected: {best_model_name} with R2 Score: {best_r2:.4f}")
    
    # Save best model
    joblib.dump(best_model, 'models/best_model.joblib')
    print("Best model saved to models/best_model.joblib")

if __name__ == "__main__":
    train_and_evaluate()
