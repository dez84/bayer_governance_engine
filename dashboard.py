import streamlit as st
import duckdb
import pandas as pd

conn = duckdb.connect('bayer_governance.db')

st.set_page_config(page_title="Bayer IT Data Stewardship Portal", layout="wide")
st.title("🌱 Bayer Crop Science Data Stewardship & Cataloging Platform")
st.markdown("### Automated Data Quality Monitoring, Catalog Mapping, & FAIR Alignment")

st.markdown("---")

# 1. Stewardship High-Level Metrics
st.subheader("📊 Governance Performance Metrics")
col1, col2, col3, col4 = st.columns(4)

metrics = conn.execute("SELECT * FROM stewardship_metrics").df().iloc[0]

col1.metric("Total Records Profiled", f"{metrics['total_profileed_records']:,}")
col2.metric("Pristine Relational Inserts", f"{metrics['clean_assets_loaded']:,}")
col3.metric("Isolated Remediation Tickets", f"{metrics['quarantined_assets_isolated']:,}")
col4.metric("Data Quality Index Score", f"{metrics['data_quality_index']}%")

st.markdown("---")

# 2. Interactive Data Catalog and Metadata Explorer
st.subheader("🗂️ Metadata Repository & Object Relations (FAIR Data Map)")
left_col, right_col = st.columns([1, 2])

with left_col:
    st.markdown("**Data Dictionary Schema Discovery**")
    catalog_data = conn.execute("SELECT * FROM data_catalog_metadata").df()
    st.dataframe(catalog_data, use_container_width=True, hide_index=True)

with right_col:
    st.markdown("**Regional Inbound Summary Aggregations**")
    regional_summary = conn.execute("""
        SELECT region_hub, COUNT(*) as record_count, ROUND(AVG(yield_metric_bu_acre), 2) as average_yield
        FROM validated_crop_trials
        GROUP BY region_hub
        ORDER BY record_count DESC
    """).df()
    st.bar_chart(regional_summary.set_index('region_hub')['average_yield'])

st.markdown("---")

# 3. Active Incident Response Grid
st.subheader("⚠️ Automated Remediation Logs & Ticket Tracking")
remediation_df = pd.read_csv('data/stewardship_remediation_log.csv')
if not remediation_df.empty:
    st.dataframe(remediation_df, use_container_width=True)
else:
    st.success("🎉 Zero quality remediation violations detected in active catalog pipelines.")