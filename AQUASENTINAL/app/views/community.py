import streamlit as st
import pandas as pd
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR / "src"))

from database import init_db, insert_report, get_all_reports
from config import WARD_GEO_DATA
from components import render_kpi_card

def render(theme_mode="Dark"):
    init_db()

    # Grievance Telemetry Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_kpi_card("Total Reports", "128", delta="+12", delta_desc="this week", icon="📝", subtitle="Geo-tagged citizen complaints")
    with m2:
        render_kpi_card("Critical Hazards", "6", delta="-2", delta_desc="resolved today", icon="🚨", subtitle="Immediate vector risk")
    with m3:
        render_kpi_card("Avg Crew Response", "3.8 hrs", delta="+25", delta_desc="faster", icon="⚡", subtitle="Municipal dispatch speed")
    with m4:
        render_kpi_card("Resolution Rate", "94.2%", delta="+4.1", delta_desc="improved", icon="✅", subtitle="Citizen verified resolutions")

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    col_form, col_feed = st.columns([1, 1.4])

    with col_form:
        st.markdown("### 📝 Lodge Water & Sanitation Grievance")
        st.markdown("<p style='color: var(--text-muted); font-size: 0.85rem; margin-top: -6px;'>Crowdsourced reports directly feed into the Outbreak Prediction Model.</p>", unsafe_allow_html=True)

        with st.form("community_report_form", clear_on_submit=True):
            area_opts = list(WARD_GEO_DATA.keys())
            area = st.selectbox(
                "Municipal Ward / Location",
                area_opts,
                format_func=lambda x: f"{x} - {WARD_GEO_DATA[x]['city']} ({WARD_GEO_DATA[x]['state']})"
            )
            
            category = st.selectbox(
                "Incident Classification",
                [
                    "💧 Turbid / Discolored Drinking Water",
                    "☣️ Sewage Overflow in Residential Area",
                    "🔧 Broken Distribution Main / Major Leak",
                    "🚽 Public Toilet Water Supply Deficit",
                    "⚠️ Chemical Odor / Industrial Discharge",
                    "🦟 Stagnant Vector Breeding Water"
                ]
            )
            
            severity = st.select_slider(
                "Perceived Hazard Severity",
                options=["Low (Minor Inconvenience)", "Medium (Noticeable Disruption)", "High (Direct Health Risk)", "Critical (Severe Contamination)"],
                value="Medium (Noticeable Disruption)"
            )
            
            clean_sev = "Critical" if "Critical" in severity else "High" if "High" in severity else "Medium" if "Medium" in severity else "Low"
            desc = st.text_area("Detailed Observations & Landmarks", placeholder="E.g., Brown water from municipal tap since 8 AM near Sector 4 community center...")

            submitted = st.form_submit_button("🚀 Transmit Grievance to Municipal Control")
            if submitted:
                if desc.strip() == "":
                    st.error("Please enter a brief description before submitting.")
                else:
                    clean_cat = category.split(" ", 1)[-1]
                    insert_report(area, clean_cat, clean_sev, desc)
                    st.toast("Report logged! Assigned Ticket #AQUA-" + str(abs(hash(desc)) % 10000), icon="✅")
                    st.success("Grievance registered. Telemetry dispatched to city water engineering unit.")

    with col_feed:
        st.markdown("### 📋 Live Incident Radar")
        st.markdown("<p style='color: var(--text-muted); font-size: 0.85rem; margin-top: -6px;'>Recent citizen filings with municipal dispatch statuses.</p>", unsafe_allow_html=True)

        try:
            df = get_all_reports()
            if len(df) == 0:
                st.info("No active community incident filings. System clear.")
            else:
                for idx, row in df.head(6).iterrows():
                    sev = str(row['severity']).lower()
                    badge_class = "red" if sev in ["critical", "high"] else "amber" if sev == "medium" else "green"
                    status_text = "DISPATCHED" if idx % 2 == 0 else "UNDER INSPECTION"
                    status_color = "var(--primary)" if idx % 2 == 0 else "var(--caution)"
                    
                    area_name = row['area']
                    city = WARD_GEO_DATA.get(area_name, {}).get("city", area_name)

                    st.markdown(f"""
                    <div class="glass-card" style="padding: 12px 16px; margin-bottom: 10px; border-left: 4px solid var(--{'danger' if sev in ['critical', 'high'] else 'caution' if sev == 'medium' else 'safe'});">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <div>
                                <span class="chip-tag {badge_class}">{row['severity'].upper()}</span>
                                <b style="font-size: 0.95rem; color: var(--text-main); font-family: var(--font-heading);">{row['category']}</b>
                            </div>
                            <span style="font-size: 0.72rem; color: {status_color}; font-weight: 700; border: 1px solid {status_color}; padding: 2px 6px; border-radius: 4px;">{status_text}</span>
                        </div>
                        <p style="margin: 4px 0 6px 0; font-size: 0.88rem; color: var(--text-muted); line-height: 1.35;">{row['description']}</p>
                        <div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: var(--text-faint);">
                            <span>📍 {area_name} ({city})</span>
                            <span>🕒 {row['timestamp']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not load reports database: {e}")
