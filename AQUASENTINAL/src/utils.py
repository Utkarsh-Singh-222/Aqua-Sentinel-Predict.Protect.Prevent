import pandas as pd
import numpy as np
import os
import joblib
from pathlib import Path
from config import MODEL_DIR

def save_model(model, name="rf_model"):
    path = MODEL_DIR / f"{name}.joblib"
    joblib.dump(model, path)
    return path

def load_model(name="rf_model"):
    path = MODEL_DIR / f"{name}.joblib"
    if path.exists():
        return joblib.load(path)
    return None

def style_df_for_streamlit(df):
    """Placeholder for common dataframe styling operations"""
    return df
