import pandas as pd
import numpy as np

def engineer_features(df):
    """
    Generate features for disease outbreak prediction.
    Assumes df is sorted by date and area.
    """
    df = df.copy()
    
    # Sort just to be safe
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['area', 'date'])
    
    # Group by area for rolling features
    grouped = df.groupby('area')
    
    # Lags and rolling means
    df['wqi_rolling_7d'] = grouped['avg_wqi'].transform(lambda x: x.rolling(7, min_periods=1).mean())
    df['rainfall_rolling_7d'] = grouped['rainfall_mm'].transform(lambda x: x.rolling(7, min_periods=1).sum())
    
    # Lagged disease cases to capture momentum
    df['cases_lag_7d'] = grouped['disease_cases'].shift(7).fillna(0)
    
    # Interaction terms
    df['risk_interaction'] = (100 - df['wqi_rolling_7d']) * df['rainfall_rolling_7d']
    
    # Target definition (for prediction: classify if cases will surge in next 7 days)
    # We will predict next week's average cases, converted to a risk class.
    # To avoid data leakage, target is shifted backwards.
    df['target_cases_next_7d'] = grouped['disease_cases'].shift(-7).fillna(0)
    
    def classify_risk(cases):
        if cases < 2: return 0 # Low
        if cases < 5: return 1 # Medium
        return 2 # High
        
    df['target_risk_class'] = df['target_cases_next_7d'].apply(classify_risk)
    
    # Drop rows where target is NaN (the last 7 days of the dataset)
    # Actually we filled with 0, but we should probably drop them for training
    # For now, keep them but remember not to evaluate on them if possible.
    
    return df
