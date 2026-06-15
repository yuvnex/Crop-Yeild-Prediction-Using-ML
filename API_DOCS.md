# API Documentation

The Crop Yield Prediction application uses Flask Blueprints for its internal API structure.

## Authentication Routes

### `POST /auth/login`
- **Description:** Authenticates a user or admin and creates a session.
- **Parameters (Form Data):**
  - `email`: User email or admin username
  - `password`: Account password
  - `role`: 'user' or 'admin'

### `POST /auth/register`
- **Description:** Registers a new farmer/user.
- **Parameters (Form Data):**
  - `name`: Full name
  - `email`: Email address
  - `password`: Account password

---

## Prediction Routes

### `POST /predict/`
- **Description:** Receives agricultural parameters and returns the predicted crop yield using the trained ML model.
- **Requires Auth:** Yes (User Session)
- **Parameters (Form Data):**
  - `crop_name` (String): e.g., 'Rice', 'Wheat'
  - `soil_type` (String): e.g., 'Clay', 'Sandy'
  - `temperature` (Float): Temperature in °C
  - `rainfall` (Float): Rainfall in mm
  - `humidity` (Float): Humidity percentage
  - `fertilizer` (Float): Fertilizer used in kg
  - `irrigation` (Float): Irrigation duration in days
  - `area` (Float): Land area in Hectares
- **Returns:** Rendered HTML template with prediction results and AI Confidence.

### `GET /predict/history`
- **Description:** Fetches all past predictions made by the logged-in user.
- **Requires Auth:** Yes
- **Returns:** Rendered HTML table with prediction history.

### `POST /predict/delete/<id>`
- **Description:** Deletes a specific prediction record belonging to the user.
- **Requires Auth:** Yes
