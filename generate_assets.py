import pandas as pd
import numpy as np

# 1. Simulate Raw Crop Trial Dataset
np.random.seed(42)
rows = 250

crop_trials = pd.DataFrame({
    'trial_id': [f'TRL-{i:05d}' for i in range(1001, 1001 + rows)],
    'region_hub': np.random.choice(['Midwest-US', 'EMEA-Hub', 'LATAM-South', 'APAC-North'], size=rows),
    'crop_type': np.random.choice(['Corn', 'Soybeans', 'Wheat', 'Sorghum'], size=rows),
    'yield_metric_bu_acre': np.random.uniform(30, 220, size=rows).round(2),
    'moisture_percentage': np.random.uniform(5, 35, size=rows).round(2),
    'gmo_indicator': np.random.choice(['Yes', 'No'], size=rows)
})

# Inject explicit data quality/governance failure points
crop_trials.loc[14, 'yield_metric_bu_acre'] = -99.00   # Out-of-bounds anomaly
crop_trials.loc[42, 'moisture_percentage'] = 105.00     # Broken percentage constraint
crop_trials.loc[87, 'crop_type'] = None                 # Critical missing business descriptor

# Save raw asset
crop_trials.to_csv('data/raw_crop_trials.csv', index=False)
print("✅ Raw trial datasets generated successfully in data/")