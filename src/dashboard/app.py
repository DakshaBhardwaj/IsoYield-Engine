import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ==========================================
# 1. PAGE CONFIGURATION & UI SETUP
# ==========================================
st.set_page_config(page_title="App", layout="wide")

# Inject theme-aware Design System CSS
gsap_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;600&display=swap');

/* ===== DARK THEME ===== */
[data-theme="dark"] {
    --bg-primary:   #0e100f;
    --bg-secondary: #191919;
    --text-primary: #fffce1;
    --text-muted:   #7c7c6f;
    --border:       #42433d;
}

/* ===== LIGHT THEME ===== */
[data-theme="light"] {
    --bg-primary:   #f9f8f4;
    --bg-secondary: #ffffff;
    --text-primary: #1a1a1a;
    --text-muted:   #6b6b6b;
    --border:       #d0d0c8;
}

/* Fallback for when data-theme is not yet set */
:root {
    --bg-primary:   #0e100f;
    --bg-secondary: #191919;
    --text-primary: #fffce1;
    --text-muted:   #7c7c6f;
    --border:       #42433d;
}

/* Base App */
[data-testid="stAppViewContainer"], .stApp {
    background-color: var(--bg-primary) !important;
    font-family: 'Inter Tight', sans-serif !important;
}

[data-testid="stHeader"] {
    background-color: var(--bg-primary) !important;
}

[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-family: 'Inter Tight', sans-serif !important;
}

p, span, label, li {
    color: var(--text-primary) !important;
    font-family: 'Inter Tight', sans-serif !important;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: var(--text-primary) !important;
}

/* Menus / Popovers */
[data-baseweb="menu"],
[data-baseweb="popover"] > div,
[data-baseweb="popover"] ul,
div[role="menu"],
div[role="listbox"],
div[role="dialog"] {
    background-color: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
}

[data-baseweb="menu"] li,
[data-baseweb="menu"] span,
[data-baseweb="popover"] span {
    color: var(--text-primary) !important;
}

/* Protect Streamlit Icons from global font override */
.material-symbols-rounded, .material-icons,
[class*="icon"], [data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
}

/* Custom Hero Typography */
.gsap-hero {
    font-size: 89px !important;
    font-weight: 600 !important;
    line-height: 0.9 !important;
    letter-spacing: -0.02em !important;
    color: var(--text-primary) !important;
    margin-bottom: 24px;
}
.gsap-eyebrow {
    font-size: 19px !important;
    font-weight: 400 !important;
    color: var(--text-primary) !important;
    margin-bottom: 8px;
}
.gsap-hairline {
    border-top: 1px solid var(--border) !important;
    margin: 40px 0 !important;
}

/* Button Styling (Ghost Pills) */
.stButton > button {
    background-color: transparent !important;
    border: 1px solid var(--text-primary) !important;
    border-radius: 100px !important;
    color: var(--text-primary) !important;
    padding: 15px 24px !important;
    font-weight: 600 !important;
}

/* Primary CTA Button */
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(var(--bg-secondary), var(--bg-secondary)) padding-box,
                linear-gradient(114.41deg, #0ae448 20.74%, #abff84 65.5%) border-box !important;
    border: 2px solid transparent !important;
    border-radius: 100px !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* Sliders */
.stSlider div[data-baseweb="slider"] div[role="slider"] {
    background-color: #0ae448 !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}

/* Info / Alert boxes */
[data-testid="stAlert"] {
    background-color: var(--bg-secondary) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}

/* Expanders */
[data-testid="stExpander"] {
    border-color: var(--border) !important;
    background-color: var(--bg-secondary) !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-primary) !important;
}

/* Input fields */
[data-baseweb="input"] input,
[data-baseweb="select"] div {
    background-color: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
}

/* Selectbox / Dropdown text */
[data-testid="stSelectbox"] div {
    color: var(--text-primary) !important;
}

/* Radio buttons */
[data-testid="stRadio"] label span {
    color: var(--text-primary) !important;
}
</style>
"""
st.markdown(gsap_css, unsafe_allow_html=True)



st.markdown('<div class="gsap-hero">IsoYield<br>Engine.</div>', unsafe_allow_html=True)
st.markdown('<div class="gsap-eyebrow">{ Agricultural Optimization Engine }</div>', unsafe_allow_html=True)

st.markdown("""
<p style="font-size: 19px; max-width: 800px; color: #fffce1; line-height: 1.15;">
This engine utilizes a Linear Programming model with a <strong>Downside Mean Absolute Deviation (Semi-MAD)</strong> penalty to optimize crop portfolios. 
Unlike standard models, it simulates historical scenarios using actual monsoon rainfall to accurately model systemic climate risks like drought.
</p>
""", unsafe_allow_html=True)

st.markdown('<div class="gsap-hairline"></div>', unsafe_allow_html=True)

# --- INTERACTIVE SIDEBAR WITH FORM BATCHING ---
st.sidebar.markdown('<div class="gsap-eyebrow" style="font-size:24px; font-weight:600;">{ Model Parameters }</div>', unsafe_allow_html=True)
st.sidebar.markdown("Configure the objective parameters and resolve the Pyomo matrix.")

with st.sidebar.form(key='optimization_form'):
    user_risk = st.slider(
        "Risk Aversion Penalty (λ)", 
        min_value=0.0, max_value=1.0, value=0.50, step=0.05
    )

    user_water_cost = st.slider(
        "Groundwater Pumping Cost (₹/mm)", 
        min_value=10.0, max_value=50.0, value=25.0, step=1.0
    )
    
    submit_button = st.form_submit_button(label="Run LP Simulation")

st.sidebar.markdown('<div class="gsap-hairline"></div>', unsafe_allow_html=True)
st.sidebar.info("""
{ Backend Architecture }  
The Pyomo LP model is held in memory as a global mutable state in the FastAPI backend.
""")

API_URL = "http://127.0.0.1:8000/optimize"

# ==========================================
# 2. API CONNECTION & DATA FETCHING
# ==========================================
@st.cache_data(ttl=3600)
def fetch_portfolio_state(risk, water):
    """Fetches the optimal portfolio from the Pyomo engine via REST API."""
    payload = {"risk_aversion": risk, "water_cost": water}
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Cannot connect to the backend Optimization Engine. Ensure the FastAPI server is running (`python -m src.api.main`). Error: {e}")
        st.stop()

if submit_button:
    st.cache_data.clear()

with st.spinner("Injecting mutable constraints & solving Pyomo matrix..."):
    state = fetch_portfolio_state(user_risk, user_water_cost)

# ==========================================
# 3. DASHBOARD VISUALIZATIONS
# ==========================================

# Chart Styling Helper
def apply_gsap_theme(fig):
    fig.update_layout(
        plot_bgcolor='#0e100f',
        paper_bgcolor='#0e100f',
        font_color='#fffce1',
        margin=dict(t=40, b=40, l=40, r=40),
        xaxis=dict(showgrid=False, zerolinecolor='#42433d'),
        yaxis=dict(gridcolor='#42433d', zerolinecolor='#42433d')
    )
    return fig

# --- SECTION A: Optimal Allocation & Status Quo Comparison ---
st.markdown('<div class="gsap-eyebrow">{ Portfolio Allocation }</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #7c7c6f;'>Comparing what farmers currently plant (Status Quo) vs. the LP Recommendation.</p>", unsafe_allow_html=True)

# Prepare comparison dataframe
status_quo = state.get('status_quo_portfolio', {})
optimal = state['optimal_portfolio']

comp_data = []
for c in optimal.keys():
    if optimal[c] > 0 or status_quo.get(c, 0) > 0:
        comp_data.append({'Crop': c, 'Hectares': status_quo.get(c, 0) * 1000, 'Scenario': 'Current (Status Quo)'})
        comp_data.append({'Crop': c, 'Hectares': optimal[c] * 1000, 'Scenario': 'LP Optimized'})

df_comp = pd.DataFrame(comp_data)

if df_comp.empty:
    st.warning("The solver returned an empty portfolio. Try adjusting the parameters to be less strict.")
else:
    col_alloc1, col_alloc2 = st.columns([2, 1])
    
    with col_alloc1:
        fig_bar = px.bar(
            df_comp, x='Crop', y='Hectares', color='Scenario', barmode='group',
            color_discrete_map={'Current (Status Quo)': '#7c7c6f', 'LP Optimized': '#0ae448'},
            title="Acreage Comparison"
        )
        fig_bar.update_layout(yaxis_title="Allocated Land (Hectares)", xaxis_title="")
        apply_gsap_theme(fig_bar)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_alloc2:
        df_optimal_only = df_comp[df_comp['Scenario'] == 'LP Optimized']
        fig_tree = px.treemap(
            df_optimal_only, 
            path=[px.Constant("LP Optimized"), 'Crop'], 
            values='Hectares',
            color='Crop',
            color_discrete_sequence=['#0ae448', '#abff84', '#dfffd1', '#fffce1', '#7c7c6f'],
            title="Optimized Composition"
        )
        fig_tree.update_traces(textinfo="label+percent parent")
        apply_gsap_theme(fig_tree)
        fig_tree.update_layout(margin=dict(t=30, b=10, l=10, r=10), height=350)
        st.plotly_chart(fig_tree, use_container_width=True)

st.markdown('<div class="gsap-hairline"></div>', unsafe_allow_html=True)

# --- SECTION B: Historical Back-Test ---
st.markdown('<div class="gsap-eyebrow">{ Stress Test Analysis }</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #7c7c6f;'>A deterministic replay over the last 10 historical years, using true rainfall covariates.</p>", unsafe_allow_html=True)

history_data = [{'Year': str(k), 'Net_Profit': v} for k, v in state['portfolio_history'].items()]
df_history = pd.DataFrame(history_data).sort_values("Year")

mean_profit = df_history['Net_Profit'].mean()
worst_case = df_history['Net_Profit'].min()
best_case = df_history['Net_Profit'].max()
volatility = df_history['Net_Profit'].std()

# KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Expected Mean Margin", f"₹ {mean_profit / 10_000_000:,.2f} Cr")
kpi2.metric("Worst-Case (Downside)", f"₹ {worst_case / 10_000_000:,.2f} Cr")
kpi3.metric("Best-Case (Upside)", f"₹ {best_case / 10_000_000:,.2f} Cr")
kpi4.metric("Systemic Volatility (σ)", f"₹ {volatility / 10_000_000:,.2f} Cr")

col_chart1, col_chart2 = st.columns([2, 1])

with col_chart1:
    df_history['Status'] = df_history['Net_Profit'].apply(lambda value: 'Surplus' if value >= mean_profit else 'Shortfall')
    fig_timeline = px.bar(
        df_history, x='Year', y='Net_Profit', color='Status',
        color_discrete_map={'Surplus': '#0ae448', 'Shortfall': '#ff8709'},
        hover_data={'Status': False, 'Year': True, 'Net_Profit': ':,.0f'}
    )
    fig_timeline.add_hline(y=mean_profit, line_dash="dash", line_color="#fffce1", annotation_text="Expected Mean")
    fig_timeline.update_layout(xaxis_title="Historical Year", yaxis_title="Systemic Portfolio Margin (₹)", showlegend=True, height=450)
    apply_gsap_theme(fig_timeline)
    st.plotly_chart(fig_timeline, use_container_width=True)

with col_chart2:
    fig_box = px.box(
        df_history, 
        y="Net_Profit", 
        points="all", 
        color_discrete_sequence=['#0ae448'],
        hover_data={'Net_Profit': ':,.0f'}
    )
    fig_box.update_layout(yaxis_title="", xaxis_title="Margin Distribution", height=450, margin=dict(l=0))
    apply_gsap_theme(fig_box)
    st.plotly_chart(fig_box, use_container_width=True)
