import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

st.set_page_config(page_title="Documentation | IsoYield Engine", layout="wide")

# ==========================================
# GSAP DESIGN SYSTEM — SHARED CSS
# Identical token set as app.py
# ==========================================
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
    --accent:       #0ae448;
    --accent-light: #abff84;
    --orangey:      #ff8709;
    --pink:         #fec5fb;
    --lilac:        #9d95ff;
    --blue:         #00bae2;
}

/* ===== LIGHT THEME ===== */
[data-theme="light"] {
    --bg-primary:   #f9f8f4;
    --bg-secondary: #ffffff;
    --text-primary: #1a1a1a;
    --text-muted:   #6b6b6b;
    --border:       #d0d0c8;
    --accent:       #00a832;
    --accent-light: #4ccc70;
    --orangey:      #cc6600;
    --pink:         #cc5fc8;
    --lilac:        #6258cc;
    --blue:         #0088b0;
}

/* ===== FALLBACK (dark) ===== */
:root {
    --bg-primary:   #0e100f;
    --bg-secondary: #191919;
    --text-primary: #fffce1;
    --text-muted:   #7c7c6f;
    --border:       #42433d;
    --accent:       #0ae448;
    --accent-light: #abff84;
    --orangey:      #ff8709;
    --pink:         #fec5fb;
    --lilac:        #9d95ff;
    --blue:         #00bae2;
}

/* ===== BASE APP ===== */
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

/* ===== TYPOGRAPHY ===== */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-family: 'Inter Tight', sans-serif !important;
    letter-spacing: -0.02em;
}

p, span, label, li {
    color: var(--text-primary) !important;
    font-family: 'Inter Tight', sans-serif !important;
    font-size: 16px;
    line-height: 1.5;
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

/* Protect Streamlit Icons */
.material-symbols-rounded, .material-icons,
[class*="icon"], [data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
}

/* ===== GSAP CUSTOM TYPOGRAPHY CLASSES ===== */
/* Hero display — matches app.py .gsap-hero */
.gsap-hero {
    font-size: 66px !important;
    font-weight: 600 !important;
    line-height: 1.0 !important;
    letter-spacing: -0.02em !important;
    color: var(--text-primary) !important;
    margin-bottom: 16px;
    font-family: 'Inter Tight', sans-serif !important;
}

/* Section eyebrow — { Curly Bracket } annotations */
.gsap-eyebrow {
    font-size: 16px !important;
    font-weight: 400 !important;
    color: var(--text-muted) !important;
    margin-bottom: 12px;
    margin-top: 40px;
    letter-spacing: -0.01em;
    font-family: 'Inter Tight', sans-serif !important;
}

/* Section subheading — 34px per spec */
.gsap-subheading {
    font-size: 34px !important;
    font-weight: 600 !important;
    line-height: 1.2 !important;
    letter-spacing: -0.34px !important;
    color: var(--text-primary) !important;
    margin-bottom: 16px;
    font-family: 'Inter Tight', sans-serif !important;
}

/* Body large — 19px per spec */
.gsap-body {
    font-size: 19px !important;
    line-height: 1.5 !important;
    color: var(--text-primary) !important;
    font-family: 'Inter Tight', sans-serif !important;
    margin-bottom: 24px;
}

/* Column label headings — discipline-style */
.gsap-label-issue  { font-size: 14px !important; font-weight: 600 !important; color: var(--orangey) !important; letter-spacing: 0.08em; text-transform: uppercase; }
.gsap-label-world  { font-size: 14px !important; font-weight: 600 !important; color: var(--pink) !important;   letter-spacing: 0.08em; text-transform: uppercase; }
.gsap-label-fix    { font-size: 14px !important; font-weight: 600 !important; color: var(--accent) !important; letter-spacing: 0.08em; text-transform: uppercase; }

/* 1px hairline divider */
.gsap-hairline {
    border: none;
    border-top: 1px solid var(--border) !important;
    margin: 48px 0 !important;
}

/* Playground panel header */
.gsap-playground-header {
    font-size: 23px !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.23px;
    margin-bottom: 8px;
    margin-top: 24px;
    font-family: 'Inter Tight', sans-serif !important;
}

/* ===== COMPONENTS ===== */

/* Info / Alert boxes */
[data-testid="stAlert"] {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
[data-testid="stAlert"] p {
    color: var(--text-primary) !important;
    font-size: 16px !important;
}

/* Expanders */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    background-color: var(--bg-secondary) !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary span {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}
[data-testid="stExpander"] p,
[data-testid="stExpander"] li {
    color: var(--text-primary) !important;
    font-size: 16px !important;
}

/* Metrics */
[data-testid="stMetricValue"],
[data-testid="stMetricLabel"],
[data-testid="stMetricDelta"] {
    color: var(--text-primary) !important;
    font-family: 'Inter Tight', sans-serif !important;
}

/* Sliders */
.stSlider div[data-baseweb="slider"] div[role="slider"] {
    background-color: var(--accent) !important;
}

/* Radio buttons */
[data-testid="stRadio"] label span {
    color: var(--text-primary) !important;
}

/* Input fields */
[data-baseweb="input"] input,
[data-baseweb="select"] div {
    background-color: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
}

/* Markdown text inside columns */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
    color: var(--text-primary) !important;
    font-size: 16px !important;
    line-height: 1.5 !important;
}

/* Tab Styling */
[data-baseweb="tab-list"] {
    background-color: transparent !important;
    gap: 24px;
}
[data-baseweb="tab"] {
    background-color: transparent !important;
    color: var(--text-muted) !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding-bottom: 10px !important;
}
[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* Ghost Pill Button — matches app.py */
.stButton > button {
    background-color: transparent !important;
    border: 1px solid var(--text-primary) !important;
    border-radius: 100px !important;
    color: var(--text-primary) !important;
    padding: 15px 24px !important;
    font-weight: 600 !important;
    font-family: 'Inter Tight', sans-serif !important;
}
</style>
"""
st.markdown(gsap_css, unsafe_allow_html=True)


# ==========================================
# CHART THEME HELPER (theme-aware)
# ==========================================
def apply_gsap_theme(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter Tight, sans-serif", color='#fffce1'),
        margin=dict(t=48, b=40, l=40, r=40),
        xaxis=dict(showgrid=False, zerolinecolor='#42433d', color='#7c7c6f'),
        yaxis=dict(gridcolor='#42433d', zerolinecolor='#42433d', color='#7c7c6f')
    )
    return fig


# ==========================================
# PAGE HEADER — matches app.py hero style
# ==========================================
st.markdown('<div class="gsap-eyebrow">{ IsoYield Engine }</div>', unsafe_allow_html=True)
st.markdown('<div class="gsap-hero">Documentation.</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="gsap-body">An enterprise-grade Operations Research engine that mitigates systemic climate risk in subsistence agriculture through convex optimization and downside risk modelling.</p>',
    unsafe_allow_html=True
)
st.markdown('<hr class="gsap-hairline">', unsafe_allow_html=True)


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown('<div class="gsap-eyebrow">{ Index }</div>', unsafe_allow_html=True)
selected_tab = st.sidebar.radio(
    "",
    ["Overview & Architecture", "The Mathematical Engine", "Model Boundaries"],
    label_visibility="collapsed"
)


# ==========================================
# SECTION 1 — OVERVIEW & ARCHITECTURE
# ==========================================
if selected_tab == "Overview & Architecture":

    st.markdown('<div class="gsap-eyebrow">{ Core Problem Statement }</div>', unsafe_allow_html=True)
    st.markdown('<div class="gsap-subheading">Why average yield optimization fails farmers.</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="gsap-body">Traditional agricultural models push farmers toward highly profitable but water-sensitive crops. When a monsoon fails, these portfolios collapse catastrophically. This engine uses <strong>Linear Programming (GLPK)</strong> and <strong>Downside Risk (Semi-MAD)</strong> to generate a portfolio that maximizes revenue while strictly bounding worst-case financial losses.</p>',
        unsafe_allow_html=True
    )

    st.markdown('<hr class="gsap-hairline">', unsafe_allow_html=True)
    st.markdown('<div class="gsap-eyebrow">{ Key Capabilities }</div>', unsafe_allow_html=True)

    cap1, cap2, cap3, cap4 = st.columns(4)
    with cap1:
        st.markdown('<p style="font-size:14px;font-weight:600;color:var(--accent);letter-spacing:0.08em;text-transform:uppercase;">Downside Protection</p>', unsafe_allow_html=True)
        st.markdown("Directly targets and minimizes catastrophic downside risk, not just variance.")
    with cap2:
        st.markdown('<p style="font-size:14px;font-weight:600;color:var(--blue);letter-spacing:0.08em;text-transform:uppercase;">Ultra-Low Latency</p>', unsafe_allow_html=True)
        st.markdown("Solves 10-year systemic LP matrices in under `50ms` via in-memory global instantiation.")
    with cap3:
        st.markdown('<p style="font-size:14px;font-weight:600;color:var(--orangey);letter-spacing:0.08em;text-transform:uppercase;">Covariance Simulation</p>', unsafe_allow_html=True)
        st.markdown("All yield variance is anchored to empirical monsoon rainfall — no synthetic assumptions.")
    with cap4:
        st.markdown('<p style="font-size:14px;font-weight:600;color:var(--lilac);letter-spacing:0.08em;text-transform:uppercase;">Global Optimum</p>', unsafe_allow_html=True)
        st.markdown("GLPK guarantees global optimum convergence without slow branch-and-bound solvers.")

    st.markdown('<hr class="gsap-hairline">', unsafe_allow_html=True)
    st.markdown('<div class="gsap-eyebrow">{ System Architecture }</div>', unsafe_allow_html=True)
    st.markdown('<div class="gsap-subheading">From raw rainfall data to optimal portfolio.</div>', unsafe_allow_html=True)

    mermaid_html = """
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({
        startOnLoad: true,
        theme: 'dark',
        themeVariables: {
          primaryColor: '#191919',
          primaryTextColor: '#fffce1',
          primaryBorderColor: '#42433d',
          lineColor: '#42433d',
          secondaryColor: '#0e100f',
          tertiaryColor: '#191919',
          edgeLabelBackground: '#0e100f',
          clusterBkg: '#191919',
          clusterBorder: '#42433d'
        }
      });
    </script>
    <div class="mermaid" style="background:transparent; padding: 24px 0;">
    flowchart LR
        subgraph DATA [" Data Layer "]
            A[(Rainfall\nRecords)]
            B[(Crop\nYield History)]
        end

        subgraph ENGINE [" Optimization Engine "]
            C[Covariate\nImputation]
            D[Semi-MAD\nDownside Risk]
            E[Demand &\nWater Constraints]
        end

        subgraph APP [" Application Layer "]
            F[FastAPI\nBackend]
            G[Streamlit\nDashboard]
        end

        A --> C
        B --> C
        C --> D
        E --> D
        D --> F
        F <-->|REST API| G
    </div>
    """
    components.html(mermaid_html, height=380)


# ==========================================
# SECTION 2 — THE MATHEMATICAL ENGINE
# ==========================================
elif selected_tab == "The Mathematical Engine":

    st.markdown('<div class="gsap-eyebrow">{ Mathematical Engine }</div>', unsafe_allow_html=True)
    st.markdown('<div class="gsap-subheading">Three pillars of empirical risk modelling.</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="gsap-body">This engine bridges data science with convex optimization. Each pillar below is interactive — adjust the sliders to see the mathematics respond in real time.</p>',
        unsafe_allow_html=True
    )

    # ---- PILLAR 1 ----
    st.markdown('<hr class="gsap-hairline">', unsafe_allow_html=True)
    st.markdown('<div class="gsap-eyebrow">{ 1 of 3 }</div>', unsafe_allow_html=True)
    st.markdown('<div class="gsap-subheading">Covariate Imputation.</div>', unsafe_allow_html=True)
    st.markdown(r"""
    Historical yields $Y_{c,y}$ are estimated using a crop's drought-resistance coefficient $\alpha_c$ scaled against the monsoon rainfall anomaly for that year:

    $$ Y_{c,y} = \mu_c \cdot \left( \alpha_c + (1 - \alpha_c)\frac{R_y}{\bar{R}} \right) + \epsilon $$
    """)

    st.markdown('<div class="gsap-playground-header">Playground — Yield vs. Monsoon Rainfall</div>', unsafe_allow_html=True)
    col_math1, col_math2 = st.columns([1, 2])
    with col_math1:
        st.info("Adjust a crop's genetic resilience. Resistant crops survive droughts; sensitive crops crash.")
        alpha_c = st.slider("Drought Resistance (α)", min_value=0.0, max_value=1.0, value=0.3, step=0.1,
                            help="1.0 = Fully drought-proof. 0.0 = Collapses without rain.")
        mu_c = st.slider("Max Potential Yield (μ) kg/ha", min_value=1000, max_value=5000, value=3000, step=500)

        with st.expander("Real World Interpretation", expanded=True):
            st.markdown(f"""
            Rice planted with **α=0.1, μ=4000** drops from **4,000 kg/ha** in a good year to just **2,200 kg/ha** during a 60% rainfall drought — a **45% loss**.

            Sorghum with **α=0.6, μ=2000** only falls to **1,680 kg/ha** — a **16% loss** under the same drought.

            This is how the optimizer mathematically justifies diversifying into drought-hardy crops even when they yield less in good years.
            """)

    with col_math2:
        rainfall_ratios = np.linspace(0.4, 1.6, 100)
        yields = mu_c * (alpha_c + (1 - alpha_c) * rainfall_ratios)
        df_yield = pd.DataFrame({"Rainfall Ratio (Rᵧ / R̄)": rainfall_ratios, "Estimated Yield (kg/ha)": yields})
        fig_yield = px.line(df_yield, x="Rainfall Ratio (Rᵧ / R̄)", y="Estimated Yield (kg/ha)",
                            title="Crop Yield Curve vs Monsoon Rainfall")
        fig_yield.update_traces(line_color='#0ae448', line_width=4)
        fig_yield.add_vline(x=1.0, line_dash="dash", line_color="#fffce1",
                            annotation_text="Normal Year (100% Rain)", annotation_position="top left")
        fig_yield.add_vline(x=0.6, line_dash="dot", line_color="#ff8709",
                            annotation_text="Severe Drought (60%)", annotation_position="top left")
        fig_yield.update_layout(yaxis=dict(range=[0, 5500]))
        apply_gsap_theme(fig_yield)
        st.plotly_chart(fig_yield, use_container_width=True)

    # ---- PILLAR 2 ----
    st.markdown('<hr class="gsap-hairline">', unsafe_allow_html=True)
    st.markdown('<div class="gsap-eyebrow">{ 2 of 3 }</div>', unsafe_allow_html=True)
    st.markdown('<div class="gsap-subheading">Downside Risk (Semi-MAD).</div>', unsafe_allow_html=True)
    st.markdown(r"""
    Instead of penalizing all volatility symmetrically, the objective function only penalizes results that fall *below* the expected mean — the true danger zone. A risk-aversion penalty $\lambda$ scales how aggressively the solver hunts down these shortfalls:

    $$ \max \left( E[M] - \text{Water Penalty} - \lambda \cdot E[\delta^-] \right) $$
    """)

    st.markdown('<div class="gsap-playground-header">Playground — Downside Risk Distribution</div>', unsafe_allow_html=True)
    col_math3, col_math4 = st.columns([1, 2])
    with col_math3:
        st.info("The algorithm simulates thousands of weather scenarios and penalizes only the orange 'ruin' region.")
        lambda_penalty = st.slider("Risk Aversion Penalty (λ)", min_value=0.0, max_value=5.0, value=2.0, step=0.5,
                                   help="Higher = solver aggressively avoids crop combos with high shortfall risk.")

        np.random.seed(42)
        profits = np.random.normal(loc=50000, scale=15000, size=1000)
        mean_profit = np.mean(profits)
        shortfalls = [mean_profit - p for p in profits if p < mean_profit]
        avg_shortfall = np.mean(shortfalls)
        total_penalty = lambda_penalty * avg_shortfall

        st.metric("Expected Mean Profit", f"₹ {mean_profit:,.0f}")
        st.metric("Avg Shortfall (Risk Area)", f"₹ {avg_shortfall:,.0f}")
        st.metric("Applied Math Penalty", f"₹ {total_penalty:,.0f}", delta=f"λ = {lambda_penalty}x", delta_color="inverse")

        with st.expander("Real World Interpretation", expanded=True):
            st.markdown("""
            **Why not just maximize the average?**

            Portfolio A and Portfolio B both average **₹50,000**.
            - **A:** ₹100,000 in a good year, **₹0 in a drought** — ruin.
            - **B:** ₹60,000 good, **₹40,000 drought** — survival.

            A standard model picks A. This engine sees through the average and rejects A, because the **λ penalty** makes the ₹0 scenario mathematically unbearable.
            """)

    with col_math4:
        fig_risk = go.Figure()
        hist, bin_edges = np.histogram(profits, bins=40)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        colors = ['#ff8709' if x < mean_profit else '#0ae448' for x in bin_centers]
        fig_risk.add_trace(go.Bar(x=bin_centers, y=hist, marker_color=colors, name="Profit Distribution"))
        fig_risk.add_vline(x=mean_profit, line_dash="dash", line_color="#fffce1", annotation_text="Expected Mean Profit")
        fig_risk.add_annotation(
            x=mean_profit - 22000, y=max(hist) * 0.78,
            text="The Dangerous Left Tail<br>(Penalized Area)",
            showarrow=False, font=dict(color="#ff8709", size=13)
        )
        fig_risk.update_layout(
            title="Simulated Portfolio Profit Distribution",
            showlegend=False,
            xaxis_title="Net Profit (₹)",
            yaxis_title="Scenario Frequency",
            xaxis=dict(range=[0, 100000])
        )
        apply_gsap_theme(fig_risk)
        st.plotly_chart(fig_risk, use_container_width=True)

    # ---- PILLAR 3 ----
    st.markdown('<hr class="gsap-hairline">', unsafe_allow_html=True)
    st.markdown('<div class="gsap-eyebrow">{ 3 of 3 }</div>', unsafe_allow_html=True)
    st.markdown('<div class="gsap-subheading">Piecewise Concave Constraints.</div>', unsafe_allow_html=True)
    st.markdown(r"""
    To model market elasticity within LP, revenue is split into two concave price tiers. The solver **must exhaust Tier 1** before accessing Tier 2, preventing infinite mono-cropping:

    $$R(q) = \begin{cases} P_1 \cdot q & \text{if } q \leq Q_1 \\ P_1 \cdot Q_1 + P_2 \cdot (q - Q_1) & \text{if } q > Q_1 \end{cases}$$
    """)

    st.markdown('<div class="gsap-playground-header">Playground — Market Saturation & Revenue</div>', unsafe_allow_html=True)
    col_pw1, col_pw2 = st.columns([1, 2])
    with col_pw1:
        st.info("Set the market absorption ceiling and price drop. Watch how revenue growth flattens once the market is flooded.")
        tier1_price = st.slider("Tier 1 Price (₹/kg)", min_value=10, max_value=100, value=60, step=5,
                                help="Base market price within normal supply limits.")
        tier2_price = st.slider("Tier 2 Price (₹/kg)", min_value=5, max_value=80, value=30, step=5,
                                help="Discounted price when the market is oversupplied.")
        tier1_cap = st.slider("Market Absorption Cap (kg)", min_value=500, max_value=3000, value=1500, step=100,
                              help="Quantity ceiling before the market saturates and prices fall.")

        with st.expander("Real World Interpretation", expanded=True):
            st.markdown(f"""
            If every UP farmer simultaneously plants Wheat:

            The market absorbs **{tier1_cap:,} kg at ₹{tier1_price}/kg** → Revenue: **₹{tier1_cap * tier1_price:,.0f}**.

            Beyond that, supply floods the market. Price collapses to **₹{tier2_price}/kg**. The next {tier1_cap:,} kg earns only **₹{tier1_cap * tier2_price:,.0f}** — half the revenue for the same effort.

            The piecewise constraint makes the solver see this cliff and diversify automatically.
            """)

    with col_pw2:
        qty = np.linspace(0, tier1_cap * 2.5, 300)
        revenue = np.where(qty <= tier1_cap,
                           tier1_price * qty,
                           tier1_price * tier1_cap + tier2_price * (qty - tier1_cap))
        naive_revenue = tier1_price * qty

        fig_pw = go.Figure()
        fig_pw.add_trace(go.Scatter(x=qty, y=naive_revenue, mode='lines',
                                    name='Naive (No Market Limit)',
                                    line=dict(color='#42433d', width=2, dash='dot')))
        mask1 = qty <= tier1_cap
        fig_pw.add_trace(go.Scatter(x=qty[mask1], y=revenue[mask1], mode='lines',
                                    name=f'Tier 1 (₹{tier1_price}/kg)',
                                    line=dict(color='#0ae448', width=4)))
        mask2 = qty >= tier1_cap
        fig_pw.add_trace(go.Scatter(x=qty[mask2], y=revenue[mask2], mode='lines',
                                    name=f'Tier 2 (₹{tier2_price}/kg)',
                                    line=dict(color='#ff8709', width=4)))
        fig_pw.add_vline(x=tier1_cap, line_dash='dash', line_color='#fffce1',
                         annotation_text=f'Saturation at {tier1_cap:,} kg',
                         annotation_position='top left')
        fig_pw.add_annotation(x=tier1_cap * 1.6, y=tier1_price * tier1_cap * 0.55,
                               text='Slope flattens — every<br>extra kg earns less',
                               showarrow=True, arrowhead=2,
                               arrowcolor='#ff8709', font=dict(color='#ff8709', size=13))
        fig_pw.update_layout(
            title='Piecewise Concave Revenue Curve',
            xaxis_title='Total Quantity Produced (kg)',
            yaxis_title='Total Revenue (₹)',
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#fffce1')),
            yaxis=dict(range=[0, tier1_price * tier1_cap * 2.6])
        )
        apply_gsap_theme(fig_pw)
        st.plotly_chart(fig_pw, use_container_width=True)


# ==========================================
# SECTION 3 — MODEL BOUNDARIES
# ==========================================
elif selected_tab == "Model Boundaries":

    st.markdown('<div class="gsap-eyebrow">{ Model Boundaries }</div>', unsafe_allow_html=True)
    st.markdown('<div class="gsap-subheading">Every model is a simplification of reality.</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="gsap-body">Below are the three known boundaries of this engine — what they mean on the ground, and how each could be resolved in a future version.</p>',
        unsafe_allow_html=True
    )

    # ---- LIMITATION 1 ----
    st.markdown('<hr class="gsap-hairline">', unsafe_allow_html=True)
    st.markdown('<div class="gsap-eyebrow">{ 1 of 3 }</div>', unsafe_allow_html=True)
    st.markdown('<div class="gsap-subheading">The Linearity Fallacy.</div>', unsafe_allow_html=True)

    col_l1a, col_l1b, col_l1c = st.columns(3)
    with col_l1a:
        st.markdown('<p class="gsap-label-issue">Technical Issue</p>', unsafe_allow_html=True)
        st.markdown(r"""
        The yield formula is a straight line — it believes more rain always means more yield, with no upper bound.

        $$Y_{c,y} = \mu_c \cdot \left(\alpha_c + (1-\alpha_c)\frac{R_y}{\bar{R}}\right)$$

        A 200% monsoon year is predicted as twice as profitable as a 100% year.
        """)
    with col_l1b:
        st.markdown('<p class="gsap-label-world">Real World Consequence</p>', unsafe_allow_html=True)
        st.markdown("""
        In Bihar and coastal Andhra Pradesh, excessive monsoons routinely wash away entire rice paddy fields. A farmer who planted Rice because the model said "high rainfall = high yield" would face total crop failure in a flood year — exactly the catastrophic outcome the model was built to prevent.

        **The model is completely blind to flood-side risk.**
        """)
    with col_l1c:
        st.markdown('<p class="gsap-label-fix">The Solution</p>', unsafe_allow_html=True)
        st.markdown(r"""
        Replace the linear formula with a **Gaussian bell-curve yield response**:

        $$Y_{c,y} = \mu_c \cdot \exp\!\left(-\frac{(R_y - R^*)^2}{2\sigma^2}\right)$$

        Where $R^*$ is the crop's optimal rainfall. Yield peaks at the ideal level and falls symmetrically on both sides — capturing both drought *and* flood risk in one function.
        """)

    # ---- LIMITATION 2 ----
    st.markdown('<hr class="gsap-hairline">', unsafe_allow_html=True)
    st.markdown('<div class="gsap-eyebrow">{ 2 of 3 }</div>', unsafe_allow_html=True)
    st.markdown('<div class="gsap-subheading">Static Price Elasticity.</div>', unsafe_allow_html=True)

    col_l2a, col_l2b, col_l2c = st.columns(3)
    with col_l2a:
        st.markdown('<p class="gsap-label-issue">Technical Issue</p>', unsafe_allow_html=True)
        st.markdown("""
        Commodity prices (e.g., Wheat = ₹25/kg) are baked in as constants across all 10 simulated years. They do not respond to how much or how little was produced.

        **Supply and demand does not exist inside this model.**
        """)
    with col_l2b:
        st.markdown('<p class="gsap-label-world">Real World Consequence</p>', unsafe_allow_html=True)
        st.markdown("""
        Consider the **2006 Pulse Crisis**. A drought devastated lentil production across Maharashtra. Supply crashed — but the model would predict *lower revenue* because it only sees reduced yield at fixed prices.

        In reality, lentil prices **nearly tripled** that year. Farmers with even modest harvests earned far more per kilogram than in bumper years. The model completely misses this — the single most important dynamic in Indian agricultural markets.
        """)
    with col_l2c:
        st.markdown('<p class="gsap-label-fix">The Solution</p>', unsafe_allow_html=True)
        st.markdown(r"""
        Integrate a **stochastic inverse demand curve** coupled to yield scenarios:

        $$P_{c,y} = P^{\text{base}}_c \cdot \left(\frac{\bar{Q}_c}{Q_{c,y}}\right)^{\epsilon}$$

        Where $\epsilon$ is each crop's price elasticity. Prices spike dynamically during drought years and compress during surplus years — reflecting real commodity market behaviour.
        """)

    # ---- LIMITATION 3 ----
    st.markdown('<hr class="gsap-hairline">', unsafe_allow_html=True)
    st.markdown('<div class="gsap-eyebrow">{ 3 of 3 }</div>', unsafe_allow_html=True)
    st.markdown('<div class="gsap-subheading">Spatial Homogeneity.</div>', unsafe_allow_html=True)

    col_l3a, col_l3b, col_l3c = st.columns(3)
    with col_l3a:
        st.markdown('<p class="gsap-label-issue">Technical Issue</p>', unsafe_allow_html=True)
        st.markdown("""
        All farmland is treated as a single undifferentiated block. The land constraint is one number: total available hectares.

        Every hectare is assumed to have identical soil quality, water access, distance to market, and storage infrastructure.
        """)
    with col_l3b:
        st.markdown('<p class="gsap-label-world">Real World Consequence</p>', unsafe_allow_html=True)
        st.markdown("""
        In Uttar Pradesh, the fertile **Gangetic alluvial plains** (ideal for sugarcane, wheat) are worlds apart from the rain-fed **Bundelkhand plateau** (where only drought-resistant Bajra millets survive).

        A recommendation to "plant 40% sugarcane" works for Lucknow. It's catastrophic for Jhansi. The model gives both farms the exact same portfolio.
        """)
    with col_l3c:
        st.markdown('<p class="gsap-label-fix">The Solution</p>', unsafe_allow_html=True)
        st.markdown(r"""
        Decompose the single land constraint into a **multi-zone spatial LP**. Partition the region into $k$ zones, each carrying:
        - Soil suitability matrix $S_{c,k}$
        - Local water availability $W_k$
        - Transport cost $T_k$ to the nearest mandi

        The optimizer solves across all zones simultaneously, producing **zone-specific portfolios** instead of one-size-fits-all recommendations.
        """)

    st.markdown('<hr class="gsap-hairline">', unsafe_allow_html=True)
