import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "src"))

from preprocess import calculate_wqi, classify_wqi, validate_sensor_data
from anomaly_detection import detect_anomalies
from features import engineer_features

def test_wqi_calculation():
    row = {'pH': 7.2, 'turbidity': 0.5, 'tds': 200, 'free_chlorine': 0.3, 'dissolved_oxygen': 6.0}
    wqi = calculate_wqi(row)
    assert wqi > 90 # Should be very safe
    
    row_bad = {'pH': 4.0, 'turbidity': 20, 'tds': 3000, 'free_chlorine': 0.0, 'dissolved_oxygen': 1.0}
    wqi_bad = calculate_wqi(row_bad)
    assert wqi_bad < 50
    
def test_wqi_classification():
    assert classify_wqi(90) == "Safe"
    assert classify_wqi(60) == "Caution"
    assert classify_wqi(30) == "Unsafe"

def test_anomaly_detection():
    data = {
        'pH': [7.2, 7.1, 4.0], # 4.0 is anomaly
        'turbidity': [0.5, 0.6, 20.0],
        'tds': [200, 210, 3000],
        'temperature': [25, 25, 25],
        'free_chlorine': [0.3, 0.3, 0.0],
        'dissolved_oxygen': [6.0, 6.0, 1.0]
    }
    df = pd.DataFrame(data)
    result = detect_anomalies(df)
    
    assert result.iloc[0]['is_alert'] == False
    assert result.iloc[2]['is_alert'] == True
    assert result.iloc[2]['alert_severity'] == "Critical"
