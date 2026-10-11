import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR / "src"))

from components import render_kpi_card, render_alert_card
from config import DATA_DIR, WARD_GEO_DATA, INDIA_CENTER, INDIA_DEFAULT_ZOOM
from predict import predict_risk

def build_folium_map(df, focus_ward=None, theme_mode="Dark"):
    """Constructs an interactive Folium map centered on India with risk markers."""
    if focus_ward and focus_ward in WARD_GEO_DATA:
        center_lat = WARD_GEO_DATA[focus_ward]['lat']
        center_lon = WARD_GEO_DATA[focus_ward]['lon']
        zoom = 9
    else:
        center_lat = INDIA_CENTER['lat']
        center_lon = INDIA_CENTER['lon']
        zoom = 5

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    for _, row in df.iterrows():
        area = row['area']
        lat = row['latitude']
        lon = row['longitude']
        city = row.get('city', area)
        state = row.get('state', '')
        desc = row.get('region_desc', '')
        risk_score = row.get('risk_score', 0)
        risk_level = row.get('risk_level', 'Low')
        wqi = row.get('avg_wqi', 0)
        pop_density = row.get('population_density', 0)
        reports = row.get('community_reports', 0)
        cases = row.get('disease_cases', 0)

        # Visual styling by risk level
        if risk_level == 'High':
            color = "#FF3366"
            fill_color = "#FF3366"
            radius = 16
        elif risk_level == 'Medium':
            color = "#F59E0B"
            fill_color = "#F59E0B"
            radius = 13
        else:
            color = "#10B981"
            fill_color = "#10B981"
            radius = 11

        is_focused = (focus_ward == area)
        if is_focused:
            radius += 6
            weight = 4
        else:
            weight = 2

        popup_html = f"""
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; min-width: 230px; padding: 4px; color: #0f172a;">
            <div style="font-size: 15px; font-weight: 800; color: #0f172a; border-bottom: 2px solid {color}; padding-bottom: 4px; margin-bottom: 6px;">
                {area} &bull; {city}
            </div>
            <div style="font-size: 11px; color: #64748b; margin-bottom: 8px;">{state} &bull; {desc}</div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 12px;">
                <span style="font-weight: 600;">Outbreak Risk:</span>
                <span style="font-weight: 700; color: {color};">{risk_score:.1f}% ({risk_level})</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 12px;">
                <span style="font-weight: 600;">Water Quality (WQI):</span>
                <span style="font-weight: 700; color: {'#16a34a' if wqi > 75 else '#ea580c' if wqi > 50 else '#dc2626'};">{wqi:.1f} / 100</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 12px;">
                <span style="font-weight: 600;">Population Density:</span>
                <span>{pop_density:,.0f} / km²</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 12px;">
                <span style="font-weight: 600;">Citizen Reports:</span>
                <span style="font-weight: 700;">{reports} active</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 12px;">
                <span style="font-weight: 600;">Disease Cases (7d):</span>
                <span style="font-weight: 700;">{cases} reported</span>
            </div>
            <div style="background: {'#fee2e2' if risk_level=='High' else '#fef3c7' if risk_level=='Medium' else '#dcfce7'}; padding: 6px 8px; border-radius: 6px; font-size: 11px; font-weight: 600;">
                {'⚠️ Critical: Immediate boil water advisory & hyper-chlorination' if risk_level=='High' else '⚡ Caution: Enhanced sampling & pipeline integrity check' if risk_level=='Medium' else '✅ Safe: Potable parameters meet BIS IS 10500 standards'}
            </div>
        </div>
        """

        tooltip_text = f"{area} ({city}) — Risk: {risk_score:.1f}% [{risk_level}] | WQI: {wqi:.1f}"

        # Outer highlight ring for High risk or focused ward
        if risk_level == 'High' or is_focused:
            folium.CircleMarker(
                location=[lat, lon],
                radius=radius + 8,
                color=color,
                weight=1,
                fill=True,
                fill_color=color,
                fill_opacity=0.2,
            ).add_to(m)

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color=color,
            weight=weight,
            fill=True,
            fill_color=fill_color,
            fill_opacity=0.88,
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=tooltip_text,
        ).add_to(m)

    return m

def build_plotly_map(df, focus_ward=None, theme_mode="Dark"):
    """Constructs a Plotly open-street-map view with explicit India centering."""
    if focus_ward and focus_ward in WARD_GEO_DATA:
        center = {"lat": WARD_GEO_DATA[focus_ward]['lat'], "lon": WARD_GEO_DATA[focus_ward]['lon']}
        zoom = 8.5
    else:
        center = {"lat": INDIA_CENTER['lat'], "lon": INDIA_CENTER['lon']}
        zoom = 4.3

    template = "plotly_dark" if theme_mode == "Dark" else "plotly_white"

    fig = px.scatter_map(
        df,
        lat="latitude",
        lon="longitude",
        color="risk_score",
        size="population_density",
        hover_name="city_label",
        hover_data={
            "risk_score": ":.1f",
            "risk_level": True,
            "avg_wqi": ":.1f",
            "community_reports": True,
            "latitude": False,
            "longitude": False,
        },
        color_continuous_scale="RdYlGn_r",
        size_max=24,
        zoom=zoom,
        center=center,
        map_style="open-street-map",
        template=template,
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(
            title="Outbreak Risk %",
            tickvals=[20, 50, 80],
            ticktext=["Low (<40%)", "Caution (40-70%)", "High (>70%)"],
            len=0.75,
        ),
    )
    return fig

def render(theme_mode="Dark"):
    # Load Data
    try:
        area_df = pd.read_csv(DATA_DIR / "historical_area_data.csv")
        risk_df = predict_risk(area_df)
    except Exception as e:
        st.error(f"Could not load data: {e}")
        return

    # Enrich risk_df with Indian geography
    lat_list, lon_list, city_list, state_list, desc_list, label_list = [], [], [], [], [], []

    for _, row in risk_df.iterrows():
        area_key = row['area']
        geo = WARD_GEO_DATA.get(area_key, {"city": "India", "state": "IN", "lat": 20.5937, "lon": 78.9629, "description": "Monitoring Zone"})
        lat_list.append(geo["lat"])
        lon_list.append(geo["lon"])
        city_list.append(geo["city"])
        state_list.append(geo["state"])
        desc_list.append(geo["description"])
        label_list.append(f"{area_key} - {geo['city']} ({geo['state']})")

    risk_df["latitude"] = lat_list
    risk_df["longitude"] = lon_list
    risk_df["city"] = city_list
    risk_df["state"] = state_list
    risk_df["region_desc"] = desc_list
    risk_df["city_label"] = label_list

    # Synchronize with global sidebar filter
    global_sel = st.session_state.get("global_area", "All Wards (Pan-India)")
    focus_ward = None
    for w in WARD_GEO_DATA:
        if w in str(global_sel):
            focus_ward = w
            break

    # Top KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    avg_wqi = risk_df['avg_wqi'].mean()
    high_risk_count = len(risk_df[risk_df['risk_level'] == 'High'])
    med_risk_count = len(risk_df[risk_df['risk_level'] == 'Medium'])
    low_risk_count = len(risk_df[risk_df['risk_level'] == 'Low'])
    total_reports = risk_df['community_reports'].sum()

    with col1:
        render_kpi_card("National WQI Index", f"{avg_wqi:.1f}", delta="-2.1", delta_desc="vs 7d avg", icon="💧", subtitle="Bureau of Indian Standards IS 10500")
    with col2:
        render_kpi_card("High Risk Outbreaks", f"{high_risk_count}", delta="+1.0", delta_desc="new alerts", icon="🚨", subtitle=f"{med_risk_count} wards in cautionary tier")
    with col3:
        render_kpi_card("Active IoT Stations", "15 / 15", delta="+100", delta_desc="uptime", icon="📡", subtitle="Telemetry across 10 metro basins")
    with col4:
        render_kpi_card("Citizen Grievances", f"{total_reports}", delta="-8.5", delta_desc="resolved", icon="📝", subtitle="Geo-verified crowdsourced reports")

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # Interactive Map Section
    header_col, filter_col = st.columns([2, 1])
    with header_col:
        st.markdown("### 🗺️ Live Outbreak & Water Risk Map — Pan-India")
        st.markdown("<p style='color: var(--text-muted); font-size: 0.9rem; margin-top: -6px;'>Multi-layered geospatial surveillance monitoring municipal water basins, lake networks, and coastal zones.</p>", unsafe_allow_html=True)
    with filter_col:
        city_options = ["Pan-India (All Wards)"] + [f"{w} - {WARD_GEO_DATA[w]['city']}" for w in WARD_GEO_DATA]
        current_idx = 0
        if focus_ward:
            for idx, opt in enumerate(city_options):
                if focus_ward in opt:
                    current_idx = idx
                    break
        chosen_view = st.selectbox("🎯 Fly To Metro Basin", city_options, index=current_idx, key="map_city_focus")
        if "Pan-India" not in chosen_view:
            for w in WARD_GEO_DATA:
                if w in chosen_view:
                    focus_ward = w
                    break
        else:
            focus_ward = None

    # Visual Status Chips Row
    legend_cols = st.columns([1, 1, 1, 1])
    with legend_cols[0]:
        st.markdown(
            f"""<div class="glass-card" style="padding: 10px 14px; margin-bottom: 12px; border-left: 4px solid var(--danger);">
                <div style="font-weight: 700; color: var(--danger);">🔴 High Risk ({high_risk_count})</div>
                <div style="font-size: 0.76rem; color: var(--text-muted);">Outbreak Probability &ge; 70%</div>
            </div>""",
            unsafe_allow_html=True
        )
    with legend_cols[1]:
        st.markdown(
            f"""<div class="glass-card" style="padding: 10px 14px; margin-bottom: 12px; border-left: 4px solid var(--caution);">
                <div style="font-weight: 700; color: var(--caution);">🟡 Cautionary ({med_risk_count})</div>
                <div style="font-size: 0.76rem; color: var(--text-muted);">Risk Probability 40% – 69%</div>
            </div>""",
            unsafe_allow_html=True
        )
    with legend_cols[2]:
        st.markdown(
            f"""<div class="glass-card" style="padding: 10px 14px; margin-bottom: 12px; border-left: 4px solid var(--safe);">
                <div style="font-weight: 700; color: var(--safe);">🟢 Safe Basins ({low_risk_count})</div>
                <div style="font-size: 0.76rem; color: var(--text-muted);">Optimal Parameters (&lt; 40%)</div>
            </div>""",
            unsafe_allow_html=True
        )
    with legend_cols[3]:
        st.markdown(
            """<div class="glass-card" style="padding: 10px 14px; margin-bottom: 12px; border-left: 4px solid var(--primary);">
                <div style="font-weight: 700; color: var(--primary);">📍 10 Key Metros</div>
                <div style="font-size: 0.76rem; color: var(--text-muted);">Interactive clickable pins</div>
            </div>""",
            unsafe_allow_html=True
        )

    # Multi-View Map Tabs
    tab_interactive, tab_plotly, tab_table = st.tabs([
        "🇮🇳 Interactive India Map (Folium)",
        "📊 Pan-India Risk Density (Plotly)",
        "📋 Basin Surveillance Dossier"
    ])

    with tab_interactive:
        folium_map = build_folium_map(risk_df, focus_ward=focus_ward, theme_mode=theme_mode)
        st_folium(folium_map, width=None, height=530, returned_objects=[])

    with tab_plotly:
        plotly_fig = build_plotly_map(risk_df, focus_ward=focus_ward, theme_mode=theme_mode)
        st.plotly_chart(plotly_fig, use_container_width=True)

    with tab_table:
        display_cols = ['area', 'city', 'state', 'risk_score', 'risk_level', 'avg_wqi', 'rainfall_mm', 'community_reports', 'region_desc']
        table_df = risk_df[display_cols].copy()
        table_df.columns = ['Ward', 'Metro City', 'State', 'Risk Score (%)', 'Risk Tier', 'Avg WQI', 'Rainfall (mm)', 'Grievances', 'River Basin Catchment']
        table_df = table_df.sort_values(by="Risk Score (%)", ascending=False)
        st.dataframe(table_df, use_container_width=True, hide_index=True)

    st.markdown("<div style='margin-bottom: 28px;'></div>", unsafe_allow_html=True)

    # Recent Alerts Feed
    st.markdown("### ⚠️ Active Tactical Alerts & Basin Warnings")
    colA, colB = st.columns(2)
    with colA:
        render_alert_card(
            title="Critical: Turbidity Surge at Hooghly Inlet",
            message="Station ST-004 reported 45.2 NTU (Permissible threshold: 5.0 NTU). Immediate filtration required.",
            severity="Critical",
            timestamp="12 mins ago",
            area="Ward 4 (Kolkata - Hooghly Basin)"
        )
        render_alert_card(
            title="High: Outbreak Probability Forecast",
            message="Machine Learning predicts 85% probability of acute diarrheal surge within 7 days due to runoff.",
            severity="High",
            timestamp="38 mins ago",
            area="Ward 7 (Ahmedabad - Sabarmati Riverfront)"
        )
    with colB:
        render_alert_card(
            title="Medium: Distribution Pressure Loss",
            message="Pipeline sensor L-22 telemetry indicates 15% pressure drop. High risk of cross-contamination leak.",
            severity="Medium",
            timestamp="2 hours ago",
            area="Ward 1 (Delhi NCR - Yamuna Basin)"
        )
        render_alert_card(
            title="Low: Scheduled Sensor Recalibration",
            message="Station ST-002 optical dissolved oxygen sensor scheduled for preventative calibration.",
            severity="Low",
            timestamp="4 hours ago",
            area="Ward 2 (Mumbai Metropolitan)"
        )
