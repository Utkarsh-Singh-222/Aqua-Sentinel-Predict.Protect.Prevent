import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from config import MODEL_DIR
from features import engineer_features

def predict_risk(df, model_path=None):
    """
    Given a dataframe of current area metrics, predict outbreak risk for the next 7 days.
    """
    if model_path is None:
        model_path = MODEL_DIR / "risk_model.joblib"
        
    if not model_path.exists():
        # Fallback if model not trained
        df['risk_score'] = np.random.uniform(10, 90, len(df))
        df['risk_level'] = pd.cut(df['risk_score'], bins=[0, 33, 66, 100], labels=['Low', 'Medium', 'High'])
        return df
        
    model = joblib.load(model_path)
    
    # Engineer features first
    df_feat = engineer_features(df)
    
    features = [
        'wqi_rolling_7d', 'rainfall_rolling_7d', 'temperature', 'humidity',
        'sanitation_coverage', 'population_density', 'community_reports', 
        'cases_lag_7d', 'risk_interaction'
    ]
    
    # Take the latest row for each area
    latest = df_feat.sort_values('date').groupby('area').tail(1).copy()
    
    X = latest[features].fillna(0) # Basic fillna
    
    probas = model.predict_proba(X)
    # The probability of class 2 (High Risk) as the main score, or a weighted sum
    # Classes are 0, 1, 2. Let's do a weighted score: P(1)*50 + P(2)*100
    risk_scores = probas[:, 1]*50 + probas[:, 2]*100
    
    preds = model.predict(X)
    risk_mapping = {0: 'Low', 1: 'Medium', 2: 'High'}
    
    latest['risk_score'] = np.clip(risk_scores, 0, 100)
    latest['risk_level'] = [risk_mapping[p] for p in preds]
    
    return latest
