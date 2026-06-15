import pandas as pd
import numpy as np
import random
import os

def generate_dataset(num_records=2500):
    np.random.seed(42)
    
    crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Soybean', 'Barley', 'Potato']
    soil_types = ['Clay', 'Sandy', 'Loamy', 'Silt', 'Peaty', 'Saline']
    
    data = []
    
    for _ in range(num_records):
        crop = random.choice(crops)
        soil = random.choice(soil_types)
        
        # Base realistic values depending on crop
        if crop == 'Rice':
            temp = np.random.uniform(20, 35)
            rain = np.random.uniform(150, 300)
            hum = np.random.uniform(60, 90)
            fert = np.random.uniform(50, 150)
            irrigation = np.random.uniform(10, 20)
            # Yield calculation (base logic + random noise)
            base_yield = (temp * 0.5) + (rain * 2) + (fert * 1.5) + (irrigation * 5)
        elif crop == 'Wheat':
            temp = np.random.uniform(10, 25)
            rain = np.random.uniform(50, 100)
            hum = np.random.uniform(40, 70)
            fert = np.random.uniform(40, 120)
            irrigation = np.random.uniform(5, 15)
            base_yield = (temp * 1.2) + (rain * 1.5) + (fert * 1.8) + (irrigation * 4)
        elif crop == 'Sugarcane':
            temp = np.random.uniform(25, 35)
            rain = np.random.uniform(100, 250)
            hum = np.random.uniform(70, 95)
            fert = np.random.uniform(100, 250)
            irrigation = np.random.uniform(15, 30)
            base_yield = (temp * 0.8) + (rain * 3) + (fert * 2) + (irrigation * 8)
        else:
            temp = np.random.uniform(15, 35)
            rain = np.random.uniform(50, 200)
            hum = np.random.uniform(30, 80)
            fert = np.random.uniform(30, 150)
            irrigation = np.random.uniform(5, 25)
            base_yield = (temp * 1) + (rain * 1.5) + (fert * 1.5) + (irrigation * 4)
            
        # Add some noise
        noise = np.random.normal(0, base_yield * 0.1)
        final_yield = max(50, base_yield + noise) # Ensure positive minimum yield
        
        data.append([crop, soil, temp, rain, hum, fert, irrigation, final_yield])
        
    df = pd.DataFrame(data, columns=['Crop_Name', 'Soil_Type', 'Temperature', 'Rainfall', 'Humidity', 'Fertilizer', 'Irrigation', 'Yield'])
    
    # Save to CSV
    os.makedirs('dataset', exist_ok=True)
    csv_path = 'dataset/crop_data.csv'
    df.to_csv(csv_path, index=False)
    print(f"Dataset generated successfully with {num_records} records at {csv_path}")

if __name__ == "__main__":
    generate_dataset(10000)
