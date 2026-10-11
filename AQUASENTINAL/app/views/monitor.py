import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR / "src"))

from config import SAMPLE_DATA_DIR, THRESHOLDS, WARD_GEO_DATA
from anomaly_detection import detect_anomalies
from preprocess import calculate_wqi

def render(theme_mode="Dark"):
    is_dark = (theme_mode == "Dark")
    plotly_template = "plotly_dark" if is_dark else "plotly_white"
    text_color = "#F1F6FD" if is_dark else "#0F172A"

    # Top Control Bar
    ctrl_col1, ctrl_col2 = st.columns([1, 2])
    with ctrl_col1:
        data_source = st.radio("Telemetry Mode", ["Simulated Live IoT Stream", "Upload Sensor CSV Feed"], horizontal=True)

    df = None
    if data_source == "Upload Sensor CSV Feed":
        uploaded_file = st.file_uploader("Upload Sensor Log (CSV)", type=['csv'])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.toast("Sensor telemetry batch loaded successfully!", icon="✅")
        else:
            with open(SAMPLE_DATA_DIR / "sensor_data_template.csv", "rb") as f:
                st.download_button("📥 Download Official Telemetry Template CSV", f, file_name="telemetry_template.csv")
            return
    else:
        df = pd.read_csv(SAMPLE_DATA_DIR / "sample_sensor_data.csv")

    if df is not None:
        with st.spinner("Executing Isolation Forest anomaly model on telemetry frames..."):
            df['wqi'] = df.apply(calculate_wqi, axis=1)
            df = detect_anomalies(df)

        # Station Selector with City tags
        stations = df['station_id'].unique()
        station_labels = {}
        for s in stations:
            sub = df[df['station_id'] == s]
            area = sub['area'].iloc[0] if 'area' in sub.columns else "Unknown"
            city = WARD_GEO_DATA.get(area, {}).get("city", area)
            has_alert = sub['is_alert'].any()
            alert_icon = "🚨 ALERT" if has_alert else "🟢 NORMAL"
            station_labels[s] = f"{s} &bull; {city} ({area}) &mdash; [{alert_icon}]"

        sel_col, status_badge_col = st.columns([3, 1])
        with sel_col:
            station = st.selectbox(
                "Select IoT Telemetry Node",
                stations,
                format_func=lambda x: station_labels.get(x, x),
                key="telemetry_station"
            )
        st_df = df[df['station_id'] == station].copy()
        latest = st_df.iloc[-1]

        with status_badge_col:
            is_alert = latest.get('is_alert', False)
            verdict_text = "ANOMALY FLAGGED" if is_alert else "POTABLE & SECURE"
            verdict_color = "red" if is_alert else "green"
            st.markdown(f"""
            <div style="margin-top: 24px; text-align: center;">
                <span class="chip-tag {verdict_color}" style="font-size: 0.85rem; padding: 6px 14px;">{verdict_text}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)

        # Futuristic Dials Section
        st.markdown("### 🎛️ Real-Time Water Quality Dials")
        g_col1, g_col2, g_col3 = st.columns(3)

        def make_cyber_gauge(val, title, min_val, max_val, safe_range, unit="", color="#00F0FF"):
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(val, 2),
                number={'suffix': f" {unit}", 'font': {'size': 26, 'family': 'Space Grotesk', 'color': text_color}},
                title={'text': f"<b>{title}</b>", 'font': {'size': 14, 'family': 'Outfit', 'color': text_color}},
                gauge={
                    'axis': {'range': [min_val, max_val], 'tickcolor': text_color, 'tickfont': {'size': 10}},
                    'bar': {'color': color, 'thickness': 0.35},
                    'bgcolor': "rgba(255,255,255,0.06)" if is_dark else "rgba(0,0,0,0.06)",
                    'borderwidth': 1,
                    'bordercolor': "rgba(0, 240, 255, 0.2)" if is_dark else "rgba(2, 132, 199, 0.2)",
                    'steps': [
                        {'range': [min_val, safe_range[0]], 'color': 'rgba(255, 51, 102, 0.15)'},
                        {'range': [safe_range[0], safe_range[1]], 'color': 'rgba(16, 185, 129, 0.15)'},
                        {'range': [safe_range[1], max_val], 'color': 'rgba(245, 158, 11, 0.15)'}
                    ],
                }
            ))
            fig.update_layout(
                height=190,
                margin=dict(l=15, r=15, t=35, b=15),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            return fig

        with g_col1:
            wqi_val = latest['wqi']
            wqi_color = "#10B981" if wqi_val >= 75 else "#F59E0B" if wqi_val >= 50 else "#FF3366"
            st.plotly_chart(make_cyber_gauge(wqi_val, "Water Quality Index", 0, 100, [50, 80], "", wqi_color), use_container_width=True)

        with g_col2:
            turb_val = latest['turbidity']
            turb_color = "#FF3366" if turb_val > THRESHOLDS['turbidity']['max_caution'] else "#10B981"
            st.plotly_chart(make_cyber_gauge(turb_val, "Turbidity (NTU)", 0, 25, [0, 5], "NTU", turb_color), use_container_width=True)

        with g_col3:
            cl_val = latest['free_chlorine']
            cl_color = "#FF3366" if cl_val < THRESHOLDS['free_chlorine']['min_safe'] else "#10B981"
            st.plotly_chart(make_cyber_gauge(cl_val, "Free Chlorine Residual", 0, 1.5, [0.2, 0.5], "mg/L", cl_color), use_container_width=True)

        # Auxiliary Parameters Mini-Bar
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.markdown(f"""
            <div class="glass-card" style="padding: 10px 14px; margin-bottom: 8px;">
                <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">pH Level</div>
                <div class="kpi-value" style="font-size: 1.5rem; margin: 2px 0;">{latest['pH']:.2f}</div>
                <div style="font-size: 0.74rem; color: var(--safe);">BIS Safe (6.5 – 8.5)</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"""
            <div class="glass-card" style="padding: 10px 14px; margin-bottom: 8px;">
                <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">TDS (Dissolved Solids)</div>
                <div class="kpi-value" style="font-size: 1.5rem; margin: 2px 0;">{latest['tds']:.0f} <span style="font-size: 0.8rem;">ppm</span></div>
                <div style="font-size: 0.74rem; color: {'var(--danger)' if latest['tds'] > 500 else 'var(--safe)'};">Permissible: &lt; 500 ppm</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"""
            <div class="glass-card" style="padding: 10px 14px; margin-bottom: 8px;">
                <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Water Temperature</div>
                <div class="kpi-value" style="font-size: 1.5rem; margin: 2px 0;">{latest['temperature']:.1f} <span style="font-size: 0.8rem;">°C</span></div>
                <div style="font-size: 0.74rem; color: var(--text-muted);">Ambient thermal range</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col4:
            st.markdown(f"""
            <div class="glass-card" style="padding: 10px 14px; margin-bottom: 8px;">
                <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Dissolved Oxygen (DO)</div>
                <div class="kpi-value" style="font-size: 1.5rem; margin: 2px 0;">{latest['dissolved_oxygen']:.2f} <span style="font-size: 0.8rem;">mg/L</span></div>
                <div style="font-size: 0.74rem; color: {'var(--safe)' if latest['dissolved_oxygen'] >= 5.0 else 'var(--danger)'};">Healthy: &gt; 5.0 mg/L</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 18px;'></div>", unsafe_allow_html=True)

        # Historical Stream Chart
        st.markdown("### 📈 Multi-Stream Sensor Telemetry (30-Day Trend)")
        fig_trend = px.line(
            st_df,
            x='timestamp',
            y=['wqi', 'turbidity', 'pH'],
            template=plotly_template,
            labels={'value': 'Telemetry Value', 'timestamp': 'Date / Time', 'variable': 'Sensor Stream'}
        )
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # Mark detected anomalies
        anomalies = st_df[st_df['is_alert'] == True]
        if len(anomalies) > 0:
            fig_trend.add_trace(go.Scatter(
                x=anomalies['timestamp'],
                y=anomalies['wqi'],
                mode='markers',
                marker=dict(color='#FF3366', size=12, symbol='cross', line=dict(width=2, color='white')),
                name='🚨 Isolation Forest Anomaly'
            ))

        st.plotly_chart(fig_trend, use_container_width=True)

        # Live Feed Table
        st.markdown("### 🧾 Sensor Telemetry Log")
        styled_df = st_df[['timestamp', 'pH', 'turbidity', 'tds', 'free_chlorine', 'dissolved_oxygen', 'wqi', 'alert_severity', 'alert_reason']].tail(12).copy()
        styled_df.columns = ['Timestamp', 'pH', 'Turbidity (NTU)', 'TDS (ppm)', 'Free Cl (mg/L)', 'DO (mg/L)', 'WQI', 'Severity', 'Anomaly Root Cause']
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
