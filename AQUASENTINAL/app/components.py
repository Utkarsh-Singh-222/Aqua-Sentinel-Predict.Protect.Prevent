import streamlit as st
import os

def load_css(file_name="assets/style.css", theme_mode="Dark"):
    """Loads custom CSS and injects theme variables directly (no JS needed)."""
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            css_content = f.read()

        if theme_mode == "Light":
            theme_override = """
        /* =========================================================
           GLACIER LIGHT THEME - Full Override
           ========================================================= */
        :root {
            --bg-main: #F4F7FC;
            --bg-mesh: radial-gradient(circle at 10% 10%, rgba(2, 132, 199, 0.06) 0%, transparent 40%),
                       radial-gradient(circle at 90% 90%, rgba(14, 165, 233, 0.06) 0%, transparent 40%),
                       linear-gradient(180deg, #F8FAFC 0%, #EDF2F7 100%);
            --bg-sec: #FFFFFF;
            --bg-sidebar: #F0F4FB;
            --card-bg: rgba(255, 255, 255, 0.92);
            --card-bg-hover: #FFFFFF;
            --card-border: rgba(2, 132, 199, 0.2);
            --card-hover-border: rgba(2, 132, 199, 0.55);
            --card-shadow: 0 4px 24px -4px rgba(15, 23, 42, 0.10);
            --card-glow: 0 0 20px rgba(2, 132, 199, 0.12);
            --text-main: #0B1528;
            --text-muted: #3D5470;
            --text-faint: #7A92B0;
            --primary: #0284C7;
            --primary-light: #0EA5E9;
            --primary-glow: rgba(2, 132, 199, 0.25);
            --secondary: #2563EB;
            --secondary-glow: rgba(37, 99, 235, 0.2);
            --safe: #059669;
            --safe-glow: rgba(5, 150, 105, 0.2);
            --caution: #D97706;
            --caution-glow: rgba(217, 119, 6, 0.2);
            --danger: #E11D48;
            --danger-glow: rgba(225, 29, 72, 0.25);
            --pill-bg: rgba(2, 132, 199, 0.08);
            --input-bg: #FFFFFF;
            --input-border: rgba(2, 132, 199, 0.28);
            --scrollbar-thumb: #B0C4DE;
        }

        /* ---- App shell ---- */
        html, body,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        .main .block-container {
            background: var(--bg-mesh) !important;
            color: var(--text-main) !important;
        }

        /* ---- Sidebar ---- */
        .stSidebar,
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] > div {
            background: var(--bg-sidebar) !important;
            color: var(--text-main) !important;
        }

        /* ---- ALL text inside sidebar ---- */
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] li,
        section[data-testid="stSidebar"] a {
            color: var(--text-main) !important;
        }

        /* ---- Radio buttons (theme toggle) ---- */
        .stRadio > div,
        .stRadio label,
        .stRadio span,
        [data-testid="stWidgetLabel"] {
            color: var(--text-main) !important;
        }
        .stRadio [data-baseweb="radio"] div {
            background: transparent !important;
        }

        /* ---- Selectbox / dropdown ---- */
        .stSelectbox div[data-baseweb="select"] > div,
        .stSelectbox [data-baseweb="select"] > div > div,
        [data-baseweb="select"] {
            background-color: #FFFFFF !important;
            color: var(--text-main) !important;
            border-color: var(--input-border) !important;
        }
        [data-baseweb="select"] span,
        [data-baseweb="select"] div {
            color: var(--text-main) !important;
            background-color: transparent !important;
        }
        /* Dropdown popover list */
        [data-baseweb="popover"] *,
        [data-baseweb="menu"] *,
        ul[data-testid="stSelectboxVirtualDropdown"] * {
            background-color: #FFFFFF !important;
            color: var(--text-main) !important;
        }
        [data-baseweb="option"]:hover {
            background-color: rgba(2, 132, 199, 0.1) !important;
        }

        /* ---- Option menu nav container (streamlit_option_menu) ---- */
        nav[class*="nav"],
        ul[class*="nav"],
        .nav-pills,
        .nav-link,
        [class*="nav-item"],
        div[class*="st-emotion-cache"] nav {
            background-color: transparent !important;
        }

        /* ---- Streamlit metric / data widgets ---- */
        [data-testid="metric-container"],
        [data-testid="stMetric"] {
            background: var(--card-bg) !important;
            color: var(--text-main) !important;
        }
        [data-testid="stMetricValue"],
        [data-testid="stMetricLabel"],
        [data-testid="stMetricDelta"] {
            color: var(--text-main) !important;
        }

        /* ---- Tabs ---- */
        .stTabs [data-baseweb="tab-list"] {
            background: transparent !important;
        }
        .stTabs [data-baseweb="tab"] {
            background: rgba(2, 132, 199, 0.07) !important;
            color: var(--text-muted) !important;
            border-color: var(--card-border) !important;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(2, 132, 199, 0.16) !important;
            color: var(--text-main) !important;
            border-color: var(--primary) !important;
        }

        /* ---- Dataframe / table ---- */
        [data-testid="stDataFrame"],
        .dvn-scroller,
        .dataframe {
            background: #FFFFFF !important;
            color: var(--text-main) !important;
        }

        /* ---- Info / warning / error / success boxes ---- */
        [data-testid="stAlert"],
        .stAlert {
            background: rgba(2, 132, 199, 0.07) !important;
            color: var(--text-main) !important;
        }

        /* ---- Plotly chart container ---- */
        .js-plotly-plot .plotly .bg {
            fill: transparent !important;
        }

        /* ---- Any remaining dark backgrounds ---- */
        [data-testid="stVerticalBlock"] > div,
        [data-testid="stHorizontalBlock"] {
            color: var(--text-main) !important;
        }

        /* ---- Markdown / paragraph text ---- */
        .stMarkdown p,
        .stMarkdown span,
        .stMarkdown li,
        .stMarkdown h1,
        .stMarkdown h2,
        .stMarkdown h3 {
            color: var(--text-main) !important;
        }

        /* ---- Button override for light ---- */
        .stButton > button {
            color: #FFFFFF !important;
        }

        /* ---- Text input & textarea ---- */
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input {
            background-color: #FFFFFF !important;
            color: var(--text-main) !important;
            border-color: var(--input-border) !important;
        }

        /* ---- Slider ---- */
        [data-testid="stSlider"] label,
        [data-testid="stSlider"] div {
            color: var(--text-main) !important;
        }

        /* ---- Checkbox / multiselect ---- */
        .stCheckbox label,
        .stMultiSelect label {
            color: var(--text-main) !important;
        }
        [data-baseweb="tag"] {
            background-color: rgba(2, 132, 199, 0.15) !important;
            color: var(--text-main) !important;
        }

        /* ---- Expander ---- */
        [data-testid="stExpander"] > div {
            background: var(--card-bg) !important;
            border-color: var(--card-border) !important;
        }
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] span {
            color: var(--text-main) !important;
        }
        """
        else:
            theme_override = """
        /* CYBER DARK THEME - defaults already defined in CSS */
        """

        injection = "<style>" + css_content + theme_override + "</style>"
        st.markdown(injection, unsafe_allow_html=True)


def render_kpi_card(title, value, delta=None, delta_desc="", icon="📊", subtitle=""):
    """Renders a next-gen cyber glassmorphic KPI card."""
    delta_html = ""
    if delta is not None and str(delta).strip() != "":
        try:
            d_val = float(str(delta).replace("+", ""))
            delta_class = "up" if d_val >= 0 else "down"
            arrow = "up" if d_val >= 0 else "dn"
            delta_html = f'<div class="kpi-delta-pill {delta_class}">{abs(d_val):.1f}% <span class="kpi-subtext">{delta_desc}</span></div>'
        except (ValueError, TypeError):
            delta_html = f'<div class="kpi-delta-pill up">{delta} <span class="kpi-subtext">{delta_desc}</span></div>'

    sub_html = f'<div style="font-size: 0.76rem; color: var(--text-muted); margin-top: 4px;">{subtitle}</div>' if subtitle else ""

    html = f"""
    <div class="kpi-card-v2">
        <div class="kpi-header">
            <span class="kpi-label">{title}</span>
            <div class="kpi-icon-pill">{icon}</div>
        </div>
        <div class="kpi-value">{value}</div>
        {delta_html}
        {sub_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_alert_card(title, message, severity="Medium", timestamp=None, area=None):
    """Renders high-impact alert cards with severity strip and badges."""
    sev = severity.lower()
    badge_color = "red" if sev in ["critical", "high"] else "amber" if sev == "medium" else "green"

    meta_info = ""
    if area or timestamp:
        area_part = f"<b>{area}</b>" if area else ""
        time_part = f"<span>{timestamp}</span>" if timestamp else ""
        sep = " &bull; " if (area and timestamp) else ""
        meta_info = f"<div style='font-size: 0.75rem; color: var(--text-faint); margin-top: 6px;'>{area_part}{sep}{time_part}</div>"

    html = f"""
    <div class="alert-card-v2 {sev}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px;">
            <div style="font-weight: 700; font-size: 0.95rem; color: var(--text-main); font-family: var(--font-heading);">{title}</div>
            <span class="chip-tag {badge_color}">{severity.upper()}</span>
        </div>
        <div style="font-size: 0.86rem; color: var(--text-muted); line-height: 1.4;">{message}</div>
        {meta_info}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_hero_banner(title, subtitle, badge="AI Water Sentinel Active"):
    """Renders a top hero banner with badge and glow."""
    html = f"""
    <div class="hero-banner">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <div class="status-pill">
                <div class="pulsing-dot"></div>
                {badge}
            </div>
        </div>
        <h1 style="margin: 0; padding: 0;"><span class="gradient-text">{title}</span></h1>
        <p style="margin: 6px 0 0 0; color: var(--text-muted); font-size: 0.98rem; max-width: 800px;">
            {subtitle}
        </p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
