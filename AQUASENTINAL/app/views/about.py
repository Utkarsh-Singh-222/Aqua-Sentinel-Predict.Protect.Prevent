import streamlit as st
import pandas as pd

def render(theme_mode="Dark"):
    # Architecture Showcase
    st.markdown("### 🏛️ System Architecture & Data Intelligence Pipeline")
    
    arch_cols = st.columns(4)
    with arch_cols[0]:
        st.markdown("""
        <div class="glass-card" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 6px;">📡</div>
            <h4 style="margin: 0; color: var(--primary); font-family: var(--font-heading);">1. IoT Sensor Telemetry</h4>
            <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 6px; line-height: 1.4;">
                Ingests high-frequency optical, potentiometric, and electrochemical readings (pH, Turbidity, TDS, Free Chlorine, DO) from 15 telemetry stations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with arch_cols[1]:
        st.markdown("""
        <div class="glass-card" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 6px;">🛡️</div>
            <h4 style="margin: 0; color: var(--primary); font-family: var(--font-heading);">2. Anomaly Engine</h4>
            <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 6px; line-height: 1.4;">
                Unsupervised Isolation Forest algorithm detects acute multi-dimensional outliers, pipe fractures, and contamination incidents in sub-second latency.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with arch_cols[2]:
        st.markdown("""
        <div class="glass-card" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 6px;">🧠</div>
            <h4 style="margin: 0; color: var(--primary); font-family: var(--font-heading);">3. Predictive ML</h4>
            <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 6px; line-height: 1.4;">
                Random Forest ensemble trained on 7-day rolling lags, meteorological rainfall surges, and sanitation gaps to forecast disease outbreaks a week in advance.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with arch_cols[3]:
        st.markdown("""
        <div class="glass-card" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 6px;">🎯</div>
            <h4 style="margin: 0; color: var(--primary); font-family: var(--font-heading);">4. Tactical Dispatch</h4>
            <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 6px; line-height: 1.4;">
                Auto-generates priority action matrix, boil water public health warnings, mobile chlorination routes, and downloadable PDF dossiers.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # UN SDG 6 Alignment
    st.markdown("### 🌍 United Nations SDG 6: Clean Water & Sanitation Alignment")
    
    sdg_col1, sdg_col2 = st.columns(2)
    with sdg_col1:
        st.markdown("""
        <div class="glass-card" style="border-left: 4px solid #00F0FF;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="chip-tag cyan">SDG 6.1</span>
                <b style="color: var(--text-main); font-size: 1rem;">Universal & Equitable Safe Drinking Water</b>
            </div>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 8px; line-height: 1.45;">
                AquaSentinel enforces Bureau of Indian Standards (BIS IS 10500:2012) and WHO guidelines by continuously computing the Water Quality Index (WQI), safeguarding potability at the point of distribution.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with sdg_col2:
        st.markdown("""
        <div class="glass-card" style="border-left: 4px solid #10B981;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="chip-tag green">SDG 6.2 & 6.3</span>
                <b style="color: var(--text-main); font-size: 1rem;">Sanitation Access & Pollution Abatement</b>
            </div>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 8px; line-height: 1.45;">
                Combines crowdsourced sewage overflow reports with hydrological models to pinpoint infrastructure deficits before sewage mixes into potable distribution channels.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # Water Quality Standards Reference Table
    st.markdown("### 💧 Regulatory Potability Benchmark (BIS IS 10500 & WHO)")
    
    standards_data = {
        "Parameter": ["pH", "Turbidity", "Total Dissolved Solids (TDS)", "Free Residual Chlorine", "Dissolved Oxygen (DO)", "Temperature"],
        "Ideal Potable Target": ["6.5 – 8.5", "< 1.0 NTU", "< 300 ppm", "0.2 – 0.5 mg/L", "> 6.5 mg/L", "20 – 25 °C"],
        "Permissible Ceiling": ["6.5 – 8.5", "5.0 NTU", "500 ppm (Max 2000)", "< 0.2 mg/L (Critical Deficit)", "< 5.0 mg/L (Stagnant)", "30 °C"],
        "Health / Vector Consequence": [
            "Acidic corrodes copper/lead; Alkaline causes scaling",
            "Pathogen vector shelter; interferes with disinfection",
            "Gastrointestinal irritation and mineral hardness",
            "Inadequate pathogen kill in distribution lines",
            "Anaerobic conditions; promotes microbial proliferation",
            "Accelerates biological reaction rates and bacterial growth"
        ]
    }
    st.dataframe(pd.DataFrame(standards_data), use_container_width=True, hide_index=True)
