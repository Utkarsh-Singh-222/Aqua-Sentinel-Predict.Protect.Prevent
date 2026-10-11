import streamlit as st
from streamlit_option_menu import option_menu
import sys
from pathlib import Path

# Add src to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "src"))

from components import load_css, render_hero_banner
from config import APP_TITLE, APP_TAGLINE, ASSETS_DIR, WARD_GEO_DATA

# Set page config FIRST
st.set_page_config(
    page_title=f"{APP_TITLE} | {APP_TAGLINE}",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "Dark"

# Load custom CSS and inject theme
load_css(str(ASSETS_DIR / "style.css"), theme_mode=st.session_state["theme_mode"])

# Import page modules from views
from views import overview, monitor, predict, sanitation, community, about

def main():
    # Sidebar
    with st.sidebar:
        # Pinned Logo and Title
        col1, col2 = st.columns([1, 4], vertical_alignment="center")
        with col1:
            try:
                st.image(str(ASSETS_DIR / "logo.svg"), width=42)
            except:
                st.write("🛡️")
        with col2:
            st.markdown(f"<h3 style='margin: 0; padding: 0; font-size: 1.45rem; font-weight: 800; font-family: var(--font-heading);'><span class='gradient-text'>{APP_TITLE}</span></h3>", unsafe_allow_html=True)
            
        st.markdown(f"<div style='color: var(--text-muted); font-size: 0.78rem; font-weight: 600; letter-spacing: 0.04em; margin-top: 2px; margin-bottom: 14px;'>{APP_TAGLINE}</div>", unsafe_allow_html=True)
        
        # 🌗 Light / Dark Mode Toggle
        st.markdown("<div style='font-size: 0.75rem; text-transform: uppercase; font-weight: 700; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 4px;'>Theme Experience</div>", unsafe_allow_html=True)
        theme_choice = st.radio(
            "Select Theme",
            ["🌙 Cyber Dark", "☀️ Glacier Light"],
            index=0 if st.session_state["theme_mode"] == "Dark" else 1,
            horizontal=True,
            label_visibility="collapsed",
            key="theme_radio"
        )
        new_theme = "Light" if "Glacier" in theme_choice else "Dark"
        if new_theme != st.session_state["theme_mode"]:
            st.session_state["theme_mode"] = new_theme
            st.rerun()

        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

        # Navigation Menu
        is_dark = (st.session_state["theme_mode"] == "Dark")
        nav_selected = option_menu(
            menu_title=None,
            options=["Overview", "Live Monitoring", "Outbreak Prediction", "Community Reports", "Sanitation & Action Plan", "About & Methodology"],
            icons=["house", "activity", "graph-up", "chat-dots", "droplet", "info-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent" if is_dark else "#F0F4FB",
                },
                "icon": {
                    "color": "#00F0FF" if is_dark else "#0284C7",
                    "font-size": "17px"
                },
                "nav-link": {
                    "font-size": "13.5px",
                    "text-align": "left",
                    "margin": "2px 0px",
                    "font-family": "var(--font-heading)",
                    "font-weight": "600",
                    "border-radius": "10px",
                    "color": "#8EA5C8" if is_dark else "#3D5470",
                    "background-color": "transparent",
                    "--hover-color": "rgba(0, 240, 255, 0.08)" if is_dark else "rgba(2, 132, 199, 0.10)"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, rgba(0, 240, 255, 0.16), rgba(59, 130, 246, 0.16))" if is_dark else "linear-gradient(135deg, rgba(2, 132, 199, 0.18), rgba(37, 99, 235, 0.12))",
                    "border": "1px solid #00F0FF" if is_dark else "1px solid #0284C7",
                    "color": "#F1F6FD" if is_dark else "#0B1528",
                    "font-weight": "700",
                    "box-shadow": "0 0 15px rgba(0, 240, 255, 0.2)" if is_dark else "0 2px 8px rgba(2, 132, 199, 0.18)"
                },
            }
        )
        
        st.markdown("<hr style='border: none; border-top: 1px solid var(--card-border); margin: 16px 0 12px 0;'>", unsafe_allow_html=True)
        
        # Global Filters
        st.markdown("<div style='font-size: 0.75rem; text-transform: uppercase; font-weight: 700; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 6px;'>Territory Filter</div>", unsafe_allow_html=True)
        area_options = ["All Wards (Pan-India)"] + [f"{w} - {WARD_GEO_DATA[w]['city']}" for w in WARD_GEO_DATA]
        st.selectbox("Select Ward / City", area_options, key="global_area", label_visibility="collapsed")
        
        st.markdown("<hr style='border: none; border-top: 1px solid var(--card-border); margin: 16px 0 12px 0;'>", unsafe_allow_html=True)
        
        # Live System Telemetry HUD in Sidebar
        st.markdown(f"""
        <div style="background: var(--pill-bg); border: 1px solid var(--card-border); border-radius: 12px; padding: 12px; font-size: 0.78rem;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                <span style="font-weight: 600; color: var(--text-main);">Surveillance Radar</span>
                <span class="chip-tag green" style="margin: 0; font-size: 0.68rem;">LIVE</span>
            </div>
            <div style="display: flex; justify-content: space-between; color: var(--text-muted); margin-bottom: 3px;">
                <span>AI Accuracy</span>
                <b class="mono-data" style="color: var(--primary);">94.8%</b>
            </div>
            <div style="display: flex; justify-content: space-between; color: var(--text-muted); margin-bottom: 3px;">
                <span>IoT Nodes</span>
                <b class="mono-data" style="color: var(--safe);">15 / 15 Online</b>
            </div>
            <div style="display: flex; justify-content: space-between; color: var(--text-muted);">
                <span>UN SDG Alignment</span>
                <b style="color: var(--text-main);">Target 6.1 & 6.2</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Main Content Header & Hero
    page_descriptions = {
        "Overview": "National water quality surveillance, predictive outbreak tracking, and municipal emergency dispatch.",
        "Live Monitoring": "Real-time telemetry stream from IoT multi-parameter water sensors with Isolation Forest anomaly detection.",
        "Outbreak Prediction": "Machine Learning early-warning forecasts estimating 7-day disease risk across river basins.",
        "Community Reports": "Crowdsourced citizen grievance portal with geotagged incident reporting and municipal routing.",
        "Sanitation & Action Plan": "Actionable policy interventions, sanitation infrastructure gap analysis, and automated PDF dossier export.",
        "About & Methodology": "Full technical architecture, Machine Learning models, WHO/BIS standards, and United Nations SDG 6 framework.",
    }
    
    render_hero_banner(
        title=nav_selected,
        subtitle=page_descriptions.get(nav_selected, ""),
        badge=f"AquaSentinel AI • {st.session_state['theme_mode']} Mode"
    )

    # Route Page Views
    theme = st.session_state["theme_mode"]
    if nav_selected == "Overview":
        overview.render(theme_mode=theme)
    elif nav_selected == "Live Monitoring":
        monitor.render(theme_mode=theme)
    elif nav_selected == "Outbreak Prediction":
        predict.render(theme_mode=theme)
    elif nav_selected == "Community Reports":
        community.render(theme_mode=theme)
    elif nav_selected == "Sanitation & Action Plan":
        sanitation.render(theme_mode=theme)
    elif nav_selected == "About & Methodology":
        about.render(theme_mode=theme)
        
    # Custom Modern Footer
    st.markdown("""
    <div class="custom-footer">
        🛡️ <b>AquaSentinel</b> &bull; Built for Track 2: Code to Clean Water &bull; SDG 6: Clean Water and Sanitation for All
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
