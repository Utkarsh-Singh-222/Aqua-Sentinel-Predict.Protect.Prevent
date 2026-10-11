import os
import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config import DATA_DIR, SAMPLE_DATA_DIR, RANDOM_SEED, THRESHOLDS, WARD_GEO_DATA

def generate_sensor_data(n_stations=15, days=30):
    np.random.seed(RANDOM_SEED)
    start_date = datetime.now() - timedelta(days=days)
    
    stations = []
    for i in range(1, n_stations + 1):
        ward_name = f"Ward {(i % 10) + 1}"
        geo = WARD_GEO_DATA.get(ward_name, {"city": "India", "lat": 28.6139, "lon": 77.2090})
        stations.append({
            "station_id": f"ST-{i:03d}",
            "station_name": f"Station {i} ({geo['city']})",
            "area": ward_name,
            "latitude": round(geo["lat"] + np.random.uniform(-0.03, 0.03), 4),
            "longitude": round(geo["lon"] + np.random.uniform(-0.03, 0.03), 4),
            "base_wqi": np.random.uniform(60, 95)
        })
        
    records = []
    for station in stations:
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            # Add noise and some daily variations
            base_wqi = station["base_wqi"]
            
            # Add a severe contamination event for ST-004 randomly
            if station["station_id"] == "ST-004" and 10 <= day <= 15:
                ph = np.random.uniform(4.5, 5.5) # acidic
                turb = np.random.uniform(10.0, 50.0)
                tds = np.random.uniform(1000, 2500)
                cl = np.random.uniform(0.0, 0.1)
                do = np.random.uniform(1.0, 3.0)
            else:
                ph = np.clip(np.random.normal(7.2, 0.5), 0, 14)
                turb = np.clip(np.random.exponential(1.5), 0.1, 20.0)
                tds = np.clip(np.random.normal(300, 100), 50, 1500)
                cl = np.clip(np.random.normal(0.3, 0.1), 0, 1.0)
                do = np.clip(np.random.normal(6.5, 1.0), 0, 10)
                
            temp = np.random.normal(25, 3)
                
            records.append({
                "station_id": station["station_id"],
                "station_name": station["station_name"],
                "area": station["area"],
                "timestamp": current_date.strftime("%Y-%m-%d %H:%M:%S"),
                "latitude": station["latitude"],
                "longitude": station["longitude"],
                "pH": round(ph, 2),
                "turbidity": round(turb, 2),
                "tds": round(tds, 2),
                "temperature": round(temp, 2),
                "free_chlorine": round(cl, 2),
                "dissolved_oxygen": round(do, 2)
            })
            
    df = pd.DataFrame(records)
    return df

def generate_area_dataset(n_wards=10, months=12):
    np.random.seed(RANDOM_SEED)
    days = months * 30
    start_date = datetime.now() - timedelta(days=days)
    
    ward_profiles = []
    for w in range(1, n_wards + 1):
        ward_profiles.append({
            "area": f"Ward {w}",
            "sanitation_coverage": np.random.uniform(40, 95), # % households
            "population_density": np.random.uniform(5000, 30000), # per sq km
            "base_risk": np.random.uniform(0.1, 0.5)
        })
        
    records = []
    for ward in ward_profiles:
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Seasonality: Monsoon (Jul-Sep) ~ days 180-270 approx
            month_val = current_date.month
            is_monsoon = 1 if 7 <= month_val <= 9 else 0
            
            rainfall = np.random.exponential(5) if not is_monsoon else np.random.exponential(25)
            if np.random.random() > 0.3 and not is_monsoon:
                rainfall = 0
                
            temperature = np.random.normal(28, 4) if not is_monsoon else np.random.normal(25, 2)
            humidity = np.random.normal(50, 10) if not is_monsoon else np.random.normal(85, 5)
            
            # WQI degrades in monsoon and low sanitation areas
            wqi = 100 - (20 * is_monsoon) - (0.2 * (100 - ward["sanitation_coverage"])) + np.random.normal(0, 5)
            wqi = np.clip(wqi, 20, 100)
            
            # Community reports
            base_reports = 0.5 + (100 - wqi)*0.05 + rainfall*0.02
            reports = np.random.poisson(base_reports)
            
            # Disease cases lag behind rainfall and low WQI
            # (We will simulate lag implicitly by just correlating with recent poor conditions, 
            #  but the feature engineering will calculate explicit rolling lags)
            risk_factor = (100 - wqi)*0.1 + rainfall*0.05 + (100 - ward["sanitation_coverage"])*0.05 + (ward["population_density"]/10000)
            
            # Occasional outbreak spikes
            if is_monsoon and wqi < 50 and np.random.random() < 0.05:
                risk_factor *= 3
                
            cases = np.random.poisson(max(0, risk_factor))
            
            records.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "area": ward["area"],
                "avg_wqi": round(wqi, 2),
                "rainfall_mm": round(rainfall, 2),
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2),
                "sanitation_coverage": round(ward["sanitation_coverage"], 2),
                "population_density": round(ward["population_density"], 2),
                "community_reports": reports,
                "disease_cases": cases
            })
            
    df = pd.DataFrame(records)
    # Sort by date
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by=["date", "area"]).reset_index(drop=True)
    return df

def generate_template_csv():
    cols = ["station_id", "station_name", "area", "timestamp", "latitude", "longitude", 
            "pH", "turbidity", "tds", "temperature", "free_chlorine", "dissolved_oxygen"]
    df = pd.DataFrame(columns=cols)
    return df

def main():
    print("Generating synthetic datasets...")
    
    # 1. Historical Area Dataset for prediction model
    area_df = generate_area_dataset()
    area_df.to_csv(DATA_DIR / "historical_area_data.csv", index=False)
    print(f"Created historical_area_data.csv ({len(area_df)} rows)")
    
    # 2. Sensor Data for live monitoring
    sensor_df = generate_sensor_data(days=1)
    sensor_df.to_csv(SAMPLE_DATA_DIR / "sample_sensor_data.csv", index=False)
    print(f"Created sample_sensor_data.csv ({len(sensor_df)} rows)")
    
    # 3. Empty Template
    template_df = generate_template_csv()
    template_df.to_csv(SAMPLE_DATA_DIR / "sensor_data_template.csv", index=False)
    print("Created sensor_data_template.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.parse_args()
    main()
