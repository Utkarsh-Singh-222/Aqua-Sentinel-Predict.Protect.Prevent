import os
from pathlib import Path

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
ASSETS_DIR = BASE_DIR / "assets"
DB_PATH = DATA_DIR / "aquasentinel.db"

# Create directories if they don't exist
for d in [DATA_DIR, MODEL_DIR, SAMPLE_DATA_DIR, ASSETS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Color Palette
COLORS = {
    "primary": "#00E5D1",
    "primary_light": "#22D3EE",
    "secondary": "#3B82F6",
    "safe": "#22C55E",
    "caution": "#F59E0B",
    "danger": "#EF4444",
    "bg_main": "#060B1A",
    "bg_sec": "#0B1630",
    "text_main": "#E6F1FF",
    "text_muted": "#8FA3BF",
}

# Water Quality Thresholds (WHO/BIS guidelines approximations)
# Sources: World Health Organization Guidelines for Drinking-water Quality, 
# Bureau of Indian Standards (IS 10500:2012)
THRESHOLDS = {
    "pH": {"min": 6.5, "max": 8.5, "unit": ""},
    "turbidity": {"max_safe": 1.0, "max_caution": 5.0, "unit": "NTU"}, # Ideal < 1, Permissible < 5
    "tds": {"max_safe": 300, "max_caution": 500, "max_danger": 2000, "unit": "ppm"}, # Ideal < 300, Permissible < 500, Max < 2000
    "temperature": {"max_safe": 30.0, "unit": "°C"},
    "free_chlorine": {"min_safe": 0.2, "max_safe": 0.5, "unit": "mg/L"}, # 0.2-0.5 is ideal for residual
    "dissolved_oxygen": {"min_safe": 5.0, "unit": "mg/L"}, # > 5 is good
}

# Random Seed for reproducibility
RANDOM_SEED = 42

# UI Constants
APP_TITLE = "AquaSentinel"
APP_TAGLINE = "Predict. Protect. Prevent."

# Geographic Mapping for Indian Wards / River Basin Monitoring Zones
WARD_GEO_DATA = {
    "Ward 1": {"city": "Delhi NCR", "state": "Delhi", "lat": 28.6139, "lon": 77.2090, "description": "Yamuna River Catchment & East Delhi"},
    "Ward 2": {"city": "Mumbai", "state": "Maharashtra", "lat": 19.0760, "lon": 72.8777, "description": "Mithi River & Coastal Catchment Zone"},
    "Ward 3": {"city": "Bengaluru", "state": "Karnataka", "lat": 12.9716, "lon": 77.5946, "description": "Bellandur & Varthur Lake Network"},
    "Ward 4": {"city": "Kolkata", "state": "West Bengal", "lat": 22.5726, "lon": 88.3639, "description": "Hooghly River Basin & East Wetlands"},
    "Ward 5": {"city": "Chennai", "state": "Tamil Nadu", "lat": 13.0827, "lon": 80.2707, "description": "Cooum & Adyar River Basin"},
    "Ward 6": {"city": "Hyderabad", "state": "Telangana", "lat": 17.3850, "lon": 78.4867, "description": "Musi River Watershed & Central Zone"},
    "Ward 7": {"city": "Ahmedabad", "state": "Gujarat", "lat": 23.0225, "lon": 72.5714, "description": "Sabarmati Riverfront & Industrial Belt"},
    "Ward 8": {"city": "Varanasi", "state": "Uttar Pradesh", "lat": 25.3176, "lon": 82.9739, "description": "Ganga Basin Central Monitoring Station"},
    "Ward 9": {"city": "Pune", "state": "Maharashtra", "lat": 18.5204, "lon": 73.8567, "description": "Mula-Mutha Confluence & Cantonment"},
    "Ward 10": {"city": "Jaipur", "state": "Rajasthan", "lat": 26.9124, "lon": 75.7873, "description": "Dravyavati River & Northern Municipal Zone"},
}

INDIA_CENTER = {"lat": 21.7679, "lon": 78.8718}
INDIA_DEFAULT_ZOOM = 4.8
