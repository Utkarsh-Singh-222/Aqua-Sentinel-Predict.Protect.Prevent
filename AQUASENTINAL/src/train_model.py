import os
import argparse
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import json

from config import DATA_DIR, MODEL_DIR, RANDOM_SEED
from features import engineer_features

def train_and_evaluate(df_path=None):
    if df_path is None:
        df_path = DATA_DIR / "historical_area_data.csv"
        
    if not df_path.exists():
        print(f"Dataset not found at {df_path}")
        return
        
    print("Loading data and engineering features...")
    df = pd.read_csv(df_path)
    df = engineer_features(df)
    
    # Drop rows where target is effectively missing (the last 7 days)
    # Since we shifted -7, the last 7 dates per area don't have true future targets.
    max_date = df['date'].max() - pd.Timedelta(days=7)
    train_df = df[df['date'] <= max_date].copy()
    
    features = [
        'wqi_rolling_7d', 'rainfall_rolling_7d', 'temperature', 'humidity',
        'sanitation_coverage', 'population_density', 'community_reports', 
        'cases_lag_7d', 'risk_interaction'
    ]
    target = 'target_risk_class'
    
    X = train_df[features]
    y = train_df[target]
    
    # Time-based split to avoid leakage
    split_date = train_df['date'].quantile(0.8)
    X_train = train_df[train_df['date'] <= split_date][features]
    y_train = train_df[train_df['date'] <= split_date][target]
    X_test = train_df[train_df['date'] > split_date][features]
    y_test = train_df[train_df['date'] > split_date][target]
    
    print(f"Training shapes: X_train {X_train.shape}, X_test {X_test.shape}")
    
    # Train Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=RANDOM_SEED, class_weight='balanced')
    rf.fit(X_train, y_train)
    
    # Train Gradient Boosting
    gb = GradientBoostingClassifier(n_estimators=100, random_state=RANDOM_SEED)
    gb.fit(X_train, y_train)
    
    rf_preds = rf.predict(X_test)
    gb_preds = gb.predict(X_test)
    
    rf_acc = accuracy_score(y_test, rf_preds)
    gb_acc = accuracy_score(y_test, gb_preds)
    
    print(f"Random Forest Accuracy: {rf_acc:.4f}")
    print(f"Gradient Boosting Accuracy: {gb_acc:.4f}")
    
    best_model = rf if rf_acc >= gb_acc else gb
    best_name = "RandomForest" if rf_acc >= gb_acc else "GradientBoosting"
    best_acc = max(rf_acc, gb_acc)
    
    print(f"\nBest Model: {best_name}")
    print(classification_report(y_test, best_model.predict(X_test)))
    
    # Save Model
    model_path = MODEL_DIR / "risk_model.joblib"
    joblib.dump(best_model, model_path)
    print(f"Saved best model to {model_path}")
    
    # Save feature importance
    if best_name == "RandomForest":
        importances = best_model.feature_importances_
    else:
        importances = best_model.feature_importances_
        
    feat_imp = dict(zip(features, importances))
    with open(MODEL_DIR / "feature_importance.json", "w") as f:
        json.dump(feat_imp, f)
        
    metrics = {
        "accuracy": best_acc,
        "model_type": best_name
    }
    with open(MODEL_DIR / "metrics.json", "w") as f:
        json.dump(metrics, f)
        
    return best_model

if __name__ == "__main__":
    train_and_evaluate()
