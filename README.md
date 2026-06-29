# 🌱 FAIR Data Stewardship & Metadata Cataloging Engine

An automated, production-ready framework designed to embed data quality profiling, metadata capture, and FAIR (Findable, Accessible, Interoperable, Reusable) data principles directly into enterprise ingestion pipelines. 

This project simulates a data stewardship workflow for complex business segments (e.g., agronomy, operational trial metrics), profiling inbound data assets, auto-generating a structural data dictionary, enforcing boundary constraints, and isolating data quality anomalies into an auditable remediation log.

## 🏗️ Architecture & Governance Stack

*   **Data Generation Layer (`generate_assets.py`):** Simulates a raw enterprise dataset tracking regional crop trial information, embedded with intentional real-world operational anomalies (null values, boundary violations).
*   **Data Stewardship Engine (`stewardship_pipeline.py`):** The programmatic core. Extracts technical metadata schemas, dynamically profiles constraints, and scores overall data quality.
*   **Relational Metastore (`duckdb`):** An in-memory analytics database serving as the high-performance repository for the data catalog metadata and pristine target schemas.
*   **Stewardship Control Plane (`dashboard.py`):** An interactive Streamlit interface providing cross-functional stakeholders, product managers, and senior stewards an executive telemetry view of data health, schema discovery, and data support log monitoring.

---

## 🛡️ Programmatic Guardrails & Data Quality Matrix

The automated stewardship script evaluates incoming transactional entries against strict business metadata rules before allowing relational warehouse inserts:

1.  **Critical Business Term Verification:** Validates that essential domain categorizations (e.g., `crop_type`) are populated, preventing orphaned schemas.
2.  **Logical Boundary Profiling:** Captures and logs out-of-bounds quantitative data points (e.g., negative crop yield metrics).
3.  **Percentage Constraint Validation:** Ensures ratio metrics fall safely within deterministic boundaries ($0 \le \text{moisture\_percentage} \le 100$).

Anomalous entries failing these rules are gracefully bypassed and sent straight to an external remediation log (`data/stewardship_remediation_log.csv`) to trigger support ticketing workflows without interrupting pipeline uptime.

---

## 🚀 Local Installation & Setup Runbook

### 1. Clone & Set Up Environment
Ensure you are running inside your isolated Python environment:

# Clone the repository (or navigate to your project directory)
cd bayer_governance_engine

# Initialize and activate the virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install pandas duckdb streamlit

2. Execute the Pipeline Sequence
Run the generation script followed by the automated data stewardship governance engine:


# Generate mock operational inputs
python3 generate_assets.py

# Run the ingestion script, profile data quality, and build the metadata tables
python3 stewardship_pipeline.py
3. Launch the Governance Dashboard
Spin up the local Streamlit dashboard to interact with the live data catalog map and remediation logging grid:


streamlit run dashboard.py
📊 Sample Pipeline Audit Log
Upon pipeline execution, the stewardship engine outputs a structured reconciliation audit:

Plaintext
--- GOVERNANCE RECONCILIATION SUMMARY ---
📊 Overall Data Quality Index: 98.80%
🔍 Validated Records Staged: 247
⚠️ Remediation Logs Triggered: 3
-----------------------------------------