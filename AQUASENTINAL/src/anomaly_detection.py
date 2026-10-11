import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from config import THRESHOLDS, RANDOM_SEED

def detect_anomalies(df):
    """
    Detect anomalies using a hybrid approach:
    1. Isolation Forest for multivariate anomalies.
    2. Rule-based checks for specific thresholds.
    Returns the dataframe with anomaly flags and reasons.
    """
    if len(df) == 0:
        return df
        
    df = df.copy()
    features = ['pH', 'turbidity', 'tds', 'temperature', 'free_chlorine', 'dissolved_oxygen']
    
    # 1. Isolation Forest
    # Handle NaNs before feeding to model
    X = df[features].fillna(df[features].mean())
    if len(X) > 10:
        model = IsolationForest(contamination=0.05, random_state=RANDOM_SEED)
        df['is_anomaly_iso'] = model.fit_predict(X) == -1
    else:
        df['is_anomaly_iso'] = False
        
    # 2. Rule-based checks
    def check_rules(row):
        alerts = []
        if row['pH'] < THRESHOLDS['pH']['min'] or row['pH'] > THRESHOLDS['pH']['max']:
            alerts.append(f"pH out of range ({row['pH']})")
        if row['turbidity'] > THRESHOLDS['turbidity']['max_caution']:
            alerts.append(f"High Turbidity ({row['turbidity']} {THRESHOLDS['turbidity']['unit']})")
        if row['tds'] > THRESHOLDS['tds']['max_caution']:
            alerts.append(f"High TDS ({row['tds']} {THRESHOLDS['tds']['unit']})")
        if row['free_chlorine'] < THRESHOLDS['free_chlorine']['min_safe']:
            alerts.append(f"Low Chlorine ({row['free_chlorine']} {THRESHOLDS['free_chlorine']['unit']})")
        
        # Determine severity based on thresholds
        severity = "Low"
        if len(alerts) > 0:
            severity = "Medium"
            if row.get('turbidity', 0) > 10 or row.get('tds', 0) > THRESHOLDS['tds']['max_danger'] or row.get('pH', 7) < 5 or row.get('pH', 7) > 10:
                severity = "Critical"
            elif row.get('is_anomaly_iso', False):
                severity = "High"
                alerts.append("Unusual multi-parameter pattern detected")
                
        return pd.Series([len(alerts) > 0, "; ".join(alerts), severity])

    rule_results = df.apply(check_rules, axis=1)
    df[['is_alert', 'alert_reason', 'alert_severity']] = rule_results
    
    return df
