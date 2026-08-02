# Installation Guide

Follow these steps to set up the Pasumai Predict application locally.

## Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- Git

## Step-by-Step Setup

### 1. Database Configuration
1. Open your MySQL terminal or client (like MySQL Workbench).
2. Ensure you have a user account or use `root`.
3. Open the `config.py` file in the project root directory and update your MySQL credentials:
   ```python
   DB_HOST = "localhost"
   DB_USER = "root"
   DB_PASSWORD = "your_mysql_password_here"
   DB_NAME = "crop_yield_db"
   ```

### 2. Environment Setup
1. Open your terminal in the project directory.
2. Create and activate a Python virtual environment:
   ```bash
   # On Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Initialize the Database
Run the provided initialization script to create the database schema and insert a default admin user:
```bash
python database/init_db.py
```
*Note: The default admin credentials are `admin` / `admin123`.*

### 4. Generate Dataset & Train Models
1. Generate the synthetic agricultural dataset:
   ```bash
   python dataset/generate_dataset.py
   ```
2. Train the Machine Learning models (Linear Regression, Decision Tree, Random Forest) and select the best one:
   ```bash
   python models/train_model.py
   ```
   *This will save the `.joblib` model files in the `models/` directory.*

### 5. Run the Application
Start the Flask development server:
```bash
python app.py
```

### 6. Access the Application
Open your web browser and navigate to:
[http://localhost:5000](http://localhost:5000)

- Register a new account or log in.
- To access the admin panel, use the login page and select "Administrator" with username: `admin` and password: `admin123`.
