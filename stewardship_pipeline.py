import pandas as pd
import duckdb
import json
from datetime import datetime

def run_stewardship_pipeline():
    print("⏳ Initiating FAIR Data Stewardship Ingestion Engine...")
    
    # 1. Profile and Ingest Raw Asset
    df = pd.read_csv('data/raw_crop_trials.csv')
    total_records = len(df)
    
    # 2. Automated Metadata Discovery & Schema Mapping (Data Catalog Design)
    metadata_catalog = []
    clean_records = []
    quarantined_records = []
    
    # Technical Metadata Structural Scan
    for column in df.columns:
        metadata_entry = {
            'column_name': column,
            'data_type': str(df[column].dtype),
            'null_count': int(df[column].isnull().sum()),
            'is_nullable': "Yes" if df[column].isnull().sum() > 0 else "No",
            'fair_status': "Findable/Interoperable"
        }
        metadata_catalog.append(metadata_entry)
        
    # 3. Dynamic Automated Monitoring, Profiling & Remediation Rules
    for idx, row in df.iterrows():
        failures = []
        
        # Rule 1: Missing Critical Domain Identifiers
        if pd.isna(row['crop_type']):
            failures.append("Missing Critical Business Term: crop_type")
            
        # Rule 2: Logical Boundary Validation
        if row['yield_metric_bu_acre'] <= 0:
            failures.append("Yield Boundary Violation (Negative/Zero)")
            
        # Rule 3: Percentage Constraints Checked
        if not (0 <= row['moisture_percentage'] <= 100):
            failures.append("Moisture Percentage Out of Bounds (>100%)")
            
        row_dict = row.to_dict()
        if failures:
            row_dict['remediation_reasons'] = "; ".join(failures)
            quarantined_records.append(row_dict)
        else:
            clean_records.append(row_dict)
            
    # Process Logs to DataFrames
    clean_df = pd.DataFrame(clean_records)
    quarantine_df = pd.DataFrame(quarantined_records)
    catalog_df = pd.DataFrame(metadata_catalog)
    
    # Save the remediation/isolation logs
    quarantine_df.to_csv('data/stewardship_remediation_log.csv', index=False)
    
    # 4. Populate Local Relational Data Warehouse
    conn = duckdb.connect('bayer_governance.db')
    
    conn.execute("CREATE OR REPLACE TABLE data_catalog_metadata AS SELECT * FROM catalog_df")
    conn.execute("CREATE OR REPLACE TABLE validated_crop_trials AS SELECT * FROM clean_df")
    
    # Executive Metadata Metrics Summary Table
    dq_score = (len(clean_df) / total_records) * 100
    metrics_summary = pd.DataFrame([{
        'execution_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_profileed_records': total_records,
        'clean_assets_loaded': len(clean_df),
        'quarantined_assets_isolated': len(quarantine_df),
        'data_quality_index': round(dq_score, 2),
        'fair_principles_aligned': 'Findable, Accessible, Interoperable, Reusable'
    }])
    conn.execute("CREATE OR REPLACE TABLE stewardship_metrics AS SELECT * FROM metrics_summary")
    
    print("\n--- GOVERNANCE RECONCILIATION SUMMARY ---")
    print(f"📊 Overall Data Quality Index: {dq_score:.2f}%")
    print(f"🔍 Validated Records Staged: {len(clean_df)}")
    print(f"⚠️ Remediation Logs Triggered: {len(quarantine_df)}")
    print("-----------------------------------------\n")
    conn.close()

if __name__ == "__main__":
    run_stewardship_pipeline()