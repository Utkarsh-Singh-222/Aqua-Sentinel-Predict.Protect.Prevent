import pandas as pd
import numpy as np

def calculate_wqi(row):
    """
    Computes a simplified Water Quality Index (0-100, 100 is best).
    Uses weighted sub-indices based on WHO guidelines.
    """
    # Weights for parameters
    weights = {
        'pH': 0.15,
        'turbidity': 0.20,
        'tds': 0.15,
        'free_chlorine': 0.25,
        'dissolved_oxygen': 0.25
    }
    
    # Sub-indices (0-100 score per parameter)
    # pH: Ideal is 7.2. 6.5-8.5 is safe.
    ph = row.get('pH', 7.2)
    ph_score = 100 - abs(ph - 7.2) * 20
    ph_score = max(0, min(100, ph_score))
    
    # Turbidity: < 1 is 100, > 5 is 0
    turb = row.get('turbidity', 0)
    turb_score = 100 - (turb * 20)
    turb_score = max(0, min(100, turb_score))
    
    # TDS: < 300 is 100, > 2000 is 0
    tds = row.get('tds', 300)
    tds_score = 100 - ((tds - 300) / 1700) * 100
    tds_score = max(0, min(100, tds_score))
    
    # Free Chlorine: 0.2-0.5 is ideal.
    cl = row.get('free_chlorine', 0.2)
    if 0.2 <= cl <= 0.5:
        cl_score = 100
    else:
        dist = min(abs(cl - 0.2), abs(cl - 0.5))
        cl_score = 100 - (dist * 200)
    cl_score = max(0, min(100, cl_score))
    
    # Dissolved Oxygen: > 5 is ideal
    do = row.get('dissolved_oxygen', 6.0)
    do_score = (do / 8.0) * 100 if do < 8 else 100
    do_score = max(0, min(100, do_score))
    
    wqi = (
        weights['pH'] * ph_score +
        weights['turbidity'] * turb_score +
        weights['tds'] * tds_score +
        weights['free_chlorine'] * cl_score +
        weights['dissolved_oxygen'] * do_score
    )
    
    return round(wqi, 2)

def classify_wqi(wqi):
    if wqi >= 80:
        return "Safe"
    elif wqi >= 50:
        return "Caution"
    else:
        return "Unsafe"

def validate_sensor_data(df):
    """
    Validates uploaded CSV data structure and values.
    Returns (is_valid, message, cleaned_df)
    """
    required_cols = ["station_id", "station_name", "area", "timestamp", "latitude", "longitude", 
                     "pH", "turbidity", "tds", "temperature", "free_chlorine", "dissolved_oxygen"]
    
    # Check columns
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        return False, f"Missing required columns: {', '.join(missing)}", None
        
    # Drop rows where all sensor values are NaN
    sensor_cols = ["pH", "turbidity", "tds", "temperature", "free_chlorine", "dissolved_oxygen"]
    df = df.dropna(subset=sensor_cols, how='all')
    if len(df) == 0:
        return False, "File contains no valid sensor readings.", None
        
    # Forward fill missing individual readings
    df[sensor_cols] = df[sensor_cols].ffill().bfill()
    
    # Validate ranges loosely
    if (df['pH'] < 0).any() or (df['pH'] > 14).any():
        return False, "Invalid pH values detected (must be 0-14).", None
        
    # Calculate WQI and Status
    df['wqi'] = df.apply(calculate_wqi, axis=1)
    df['status'] = df['wqi'].apply(classify_wqi)
    
    # Ensure timestamp is datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    
    return True, "Data validated successfully.", df
