import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR / "src"))

from config import DATA_DIR, WARD_GEO_DATA
from predict import predict_risk
from recommendations import generate_area_recommendations
from report_generator import generate_pdf_report
from components import render_kpi_card

def render(theme_mode="Dark"):
    is_dark = (theme_mode == "Dark")
    plotly_template = "plotly_dark" if is_dark else "plotly_white"

    try:
        area_df = pd.read_csv(DATA_DIR / "historical_area_data.csv")
        risk_df = predict_risk(area_df)
        recs = generate_area_recommendations(risk_df)
    except Exception as e:
        st.error(f"Error loading sanitation datasets: {e}")
        return

    merged = pd.merge(risk_df, recs, on='area')
    merged['City'] = merged['area'].map(lambda x: WARD_GEO_DATA.get(x, {}).get("city", x))
    merged['City_Label'] = merged['area'] + " (" + merged['City'] + ")"

    # Top KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    avg_sanitation = merged['sanitation_coverage'].mean()
    critical_interventions = len(merged[merged['risk_level'] == 'High'])
    with c1:
        render_kpi_card("National Sanitation Index", f"{avg_sanitation:.1f}%", delta="+3.2", delta_desc="expanded", icon="🚽", subtitle="Households connected to sewer grid")
    with c2:
        render_kpi_card("Immediate Interventions", f"{critical_interventions}", delta="+1", delta_desc="urgent wards", icon="⚡", subtitle="Targeted for mobile chlorination")
    with c3:
        render_kpi_card("Clean Water Coverage", "84.6%", delta="+1.8", delta_desc="access rate", icon="💧", subtitle="Piped water supply network")
    with c4:
        render_kpi_card("Policy Dossiers", "Active", delta="Ready", delta_desc="PDF Export", icon="📄", subtitle="Automated municipal reports")

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # Priority Action Matrix
    st.markdown("### 🎯 Strategic Priority Matrix: Sanitation Deficit vs Outbreak Risk")
    st.markdown("<p style='color: var(--text-muted); font-size: 0.85rem; margin-top: -6px;'>High Outbreak Risk + Low Sanitation Coverage = Highest Priority for Municipal Funding.</p>", unsafe_allow_html=True)

    fig = px.scatter(
        merged,
        x="sanitation_coverage",
        y="risk_score",
        size="population_density",
        color="risk_level",
        hover_name="City_Label",
        text="City",
        color_discrete_map={"High": "#FF3366", "Medium": "#F59E0B", "Low": "#10B981"},
        template=plotly_template,
        labels={'sanitation_coverage': 'Sanitation Coverage (% Households)', 'risk_score': '7-Day Outbreak Risk (%)', 'risk_level': 'Priority Tier'}
    )
    fig.update_traces(textposition='top center', marker=dict(opacity=0.85, line=dict(width=1.5, color='white' if is_dark else '#0F172A')))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=20, b=10),
        height=380
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # Action Directives Cards
    st.markdown("### 📋 Municipal Tactical Directives")
    
    col_act1, col_act2 = st.columns(2)
    rows = list(merged.sort_values("risk_score", ascending=False).iterrows())
    
    for i, (_, row) in enumerate(rows):
        if row['risk_level'] == 'Low': continue
        
        target_col = col_act1 if i % 2 == 0 else col_act2
        color = "var(--danger)" if row['risk_level'] == "High" else "var(--caution)"
        badge_type = "red" if row['risk_level'] == "High" else "amber"
        
        with target_col:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid {color}; padding: 14px 18px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <div style="font-size: 1.05rem; font-weight: 700; color: var(--text-main); font-family: var(--font-heading);">{row['area']} &bull; {row['City']}</div>
                    <span class="chip-tag {badge_type}">{row['risk_level'].upper()} TIER</span>
                </div>
                <div style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.4; margin-bottom: 8px;">
                    {row['primary_action']}
                </div>
                <div style="display: flex; gap: 14px; font-size: 0.76rem; color: var(--text-faint);">
                    <span>🚽 Sanitation: <b>{row['sanitation_coverage']:.1f}%</b></span>
                    <span>💧 WQI: <b>{row['avg_wqi']:.1f}</b></span>
                    <span>📈 Risk: <b style="color: {color};">{row['risk_score']:.1f}%</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # Official PDF Dossier Card
    st.markdown("### 📑 Official Policy Dossier & Incident Audit")
    
    pdf_box_col1, pdf_box_col2 = st.columns([2, 1])
    with pdf_box_col1:
        st.markdown("""
        <div class="glass-card" style="padding: 16px 20px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 2.2rem;">📑</span>
                <div>
                    <h4 style="margin: 0; font-family: var(--font-heading); color: var(--text-main);">AquaSentinel Comprehensive Municipal Water Security Brief</h4>
                    <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: var(--text-muted);">
                        Auto-generated executive dossier compiling Isolation Forest anomalies, Random Forest 7-day risk forecasts, and WHO/BIS compliance tables.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with pdf_box_col2:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Compile Official PDF Brief", use_container_width=True):
            with st.spinner("Compiling ReportLab PDF dossier..."):
                pdf_path = generate_pdf_report(merged)
                st.success("Dossier Compiled Successfully!")
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📥 Download AquaSentinel_Report.pdf",
                        f,
                        file_name="AquaSentinel_Official_Brief.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
