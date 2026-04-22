"""
=============================================================================
Intermediate Macroeconomics: Data Analysis Project
Task 3: Rolling Volatility & Business Cycle Decomposition (HP Filter)
=============================================================================
Author   : Member 1 (Team Lead)
Date     : April 2026
Python   : 3.x
Packages : pandas, numpy, statsmodels, plotly
=============================================================================

METHODOLOGY OVERVIEW
---------------------
1. Rolling Volatility
   - Compute the year-over-year real GDP growth rate for China.
   - Apply a 10-year (window=10) rolling standard deviation to measure
     how the dispersion of growth rates changes over time.
   - A shrinking rolling std indicates stabilisation of the business cycle.

2. HP Filter (Hodrick–Prescott, 1997)
   - Decomposes a log-level GDP series y_t into:
         y_t = τ_t + c_t
     where τ_t is the smooth trend and c_t is the cyclical component.
   - The trend minimises:
         Σ(y_t − τ_t)² + λ Σ[(τ_{t+1}−τ_t) − (τ_t−τ_{t−1})]²
   - For annual data, λ = 100 is the standard (Ravn & Uhlig, 2002).
   - We work in log levels (ln GDP) so the cyclical component is
     interpretable as percentage deviation from trend.
   - Synchronisation is measured via Pearson correlation of the two
     cyclical series over the full sample and the pre/post-2000 sub-samples.
=============================================================================
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# =============================================================================
# SECTION 0 – DATA LOADING
# =============================================================================
df = pd.read_csv("macro_data_clean_1978_2024.csv", index_col="Year")
# Required columns: CN_RGDP_usd_2015, US_RGDP_billion_usd, CN_RGDP_growth_pct


# =============================================================================
# SECTION 1 – ROLLING VOLATILITY (10-year rolling std of China GDP growth)
# =============================================================================

df["china_growth"] = df["CN_RGDP_growth_pct"]

# 10-year rolling standard deviation (min_periods=10 ensures we only
# display values once a full window is available)
df["china_roll_std"] = (
    df["china_growth"]
    .rolling(window=10, min_periods=10)
    .std()
)

print("=" * 60)
print("SECTION 1 – Rolling Volatility Summary")
print("=" * 60)
print(df[["china_growth", "china_roll_std"]].dropna().to_string())


# =============================================================================
# SECTION 2 – HP FILTER (λ = 100, annual data)
# =============================================================================

# Work with non-missing GDP observations only
df2 = df[["CN_RGDP_usd_2015", "US_RGDP_billion_usd"]].dropna().copy()

# Work in natural log of real GDP so cycles are % deviations from trend
df2["ln_china_rgdp"] = np.log(df2["CN_RGDP_usd_2015"])
df2["ln_us_rgdp"]    = np.log(df2["US_RGDP_billion_usd"])

# Apply HP filter (statsmodels hp_filter returns (cycle, trend))
china_cycle, china_trend = sm.tsa.filters.hpfilter(df2["ln_china_rgdp"], lamb=100)
us_cycle,    us_trend    = sm.tsa.filters.hpfilter(df2["ln_us_rgdp"],    lamb=100)

df2["china_cycle"] = china_cycle * 100   # convert to percent deviation
df2["china_trend"] = china_trend
df2["us_cycle"]    = us_cycle    * 100
df2["us_trend"]    = us_trend

# --- Synchronisation statistics ---
full_corr = df2["china_cycle"].corr(df2["us_cycle"])
post_corr = df2.loc[2000:, "china_cycle"].corr(df2.loc[2000:, "us_cycle"])
pre_corr  = df2.loc[:1999, "china_cycle"].corr(df2.loc[:1999, "us_cycle"])

print("\n" + "=" * 60)
print("SECTION 2 – HP Filter: Business Cycle Synchronisation")
print("=" * 60)
print(f"  Full sample correlation  (1978–2024): {full_corr:+.4f}")
print(f"  Pre-2000  correlation    (1978–1999): {pre_corr:+.4f}")
print(f"  Post-2000 correlation    (2000–2024): {post_corr:+.4f}")
print()
if post_corr < pre_corr:
    print("  → Cycles became LESS synchronised after 2000 (diverging drivers).")
else:
    print("  → Cycles became MORE synchronised after 2000 (trade integration).")


# =============================================================================
# SECTION 3 – VISUALISATIONS (Plotly, interactive HTML)
# =============================================================================

# ── Figure 1: Rolling Volatility ─────────────────────────────────────────────
fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True,
    subplot_titles=(
        "China Real GDP Growth Rate (Year-on-Year, %)",
        "10-Year Rolling Standard Deviation of China GDP Growth (%)"
    ), vertical_spacing=0.12)

fig1.add_trace(go.Scatter(x=df.index, y=df["china_growth"], mode="lines+markers",
    name="GDP Growth (%)", line=dict(color="#C0392B", width=2), marker=dict(size=4)),
    row=1, col=1)

for s, e, lbl in [(1989,1990,"Tiananmen/Austerity"),(1997,1998,"Asian Fin. Crisis"),
                   (2008,2009,"Global Financial Crisis"),(2020,2020,"COVID-19")]:
    fig1.add_vrect(x0=s-0.5, x1=e+0.5, fillcolor="grey", opacity=0.12, line_width=0,
        annotation_text=lbl, annotation_position="top left",
        annotation_font_size=8, row=1, col=1)

fig1.add_trace(go.Scatter(x=df.index, y=df["china_roll_std"], mode="lines",
    name="10-yr Rolling Std Dev", line=dict(color="#2980B9", width=2.5),
    fill="tozeroy", fillcolor="rgba(41,128,185,0.12)"), row=2, col=1)

fig1.update_layout(title="China Real GDP Growth Volatility: 10-Year Rolling Standard Deviation",
    height=600, legend=dict(orientation="h", y=-0.08),
    plot_bgcolor="white", paper_bgcolor="white", font=dict(family="Arial", size=12))
fig1.update_xaxes(showgrid=True, gridcolor="#E0E0E0")
fig1.update_yaxes(showgrid=True, gridcolor="#E0E0E0")
fig1.add_annotation(text="Sources: NBS, CEIC. Authors' calculations.",
    xref="paper", yref="paper", x=0, y=-0.14, showarrow=False,
    font=dict(size=10, color="grey"))
fig1.write_html("figure1_rolling_volatility.html")
print("\n  → Saved: figure1_rolling_volatility.html")


# ── Figure 2: HP Filter – Trend vs. Actual ───────────────────────────────────
fig2 = make_subplots(rows=1, cols=2,
    subplot_titles=(
        "China: Log Real GDP – Actual vs HP Trend",
        "United States: Log Real GDP – Actual vs HP Trend"),
    horizontal_spacing=0.10)

for ci, (cname, lc, tc, col) in enumerate([
    ("China","ln_china_rgdp","china_trend","#C0392B"),
    ("US","ln_us_rgdp","us_trend","#1A5276")], start=1):
    fig2.add_trace(go.Scatter(x=df2.index, y=df2[lc], mode="lines",
        name=f"{cname} Actual", line=dict(color=col, width=1.5, dash="dot")), row=1, col=ci)
    fig2.add_trace(go.Scatter(x=df2.index, y=df2[tc], mode="lines",
        name=f"{cname} HP Trend", line=dict(color=col, width=2.5)), row=1, col=ci)

fig2.update_layout(title="HP Filter Decomposition: Trend Component (λ = 100)",
    height=450, plot_bgcolor="white", paper_bgcolor="white",
    font=dict(family="Arial", size=12))
fig2.add_annotation(text="Sources: NBS, CEIC, FRED. Authors' calculations.",
    xref="paper", yref="paper", x=0, y=-0.12, showarrow=False,
    font=dict(size=10, color="grey"))
fig2.write_html("figure2_hp_trend.html")
print("  → Saved: figure2_hp_trend.html")


# ── Figure 3: HP Filter – Cyclical Components ────────────────────────────────
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df2.index, y=df2["china_cycle"], mode="lines",
    name="China Cyclical Component", line=dict(color="#C0392B", width=2),
    fill="tozeroy", fillcolor="rgba(192,57,43,0.10)"))
fig3.add_trace(go.Scatter(x=df2.index, y=df2["us_cycle"], mode="lines",
    name="US Cyclical Component", line=dict(color="#1A5276", width=2),
    fill="tozeroy", fillcolor="rgba(26,82,118,0.10)"))
fig3.add_hline(y=0, line_dash="dash", line_color="black", line_width=1)
fig3.add_vrect(x0=2007.5, x1=2009.5, fillcolor="orange", opacity=0.12, line_width=0,
    annotation_text="GFC 2008–09", annotation_position="top left",
    annotation_font_size=10)
fig3.add_annotation(x=0.02, y=0.93, xref="paper", yref="paper",
    text=(f"Full-sample corr: {full_corr:+.3f}<br>"
          f"Pre-2000 corr: {pre_corr:+.3f}<br>"
          f"Post-2000 corr: {post_corr:+.3f}"),
    showarrow=False, bgcolor="rgba(255,255,255,0.85)", bordercolor="grey",
    borderwidth=1, font=dict(size=11), align="left")
fig3.update_layout(
    title="HP Filter Cyclical Components: China vs. United States (% Deviation from Trend)",
    xaxis_title="Year", yaxis_title="Cyclical Component (% deviation from HP trend)",
    height=500, plot_bgcolor="white", paper_bgcolor="white",
    font=dict(family="Arial", size=12), legend=dict(orientation="h", y=-0.12))
fig3.add_annotation(text="Sources: NBS, CEIC, FRED. λ = 100. Authors' calculations.",
    xref="paper", yref="paper", x=0, y=-0.17, showarrow=False,
    font=dict(size=10, color="grey"))
fig3.write_html("figure3_hp_cycles.html")
print("  → Saved: figure3_hp_cycles.html")

print("\n✅  All outputs generated successfully.")
print(f"\n  Business Cycle Correlations:")
print(f"    Full sample (1978–2024): {full_corr:+.4f}")
print(f"    Pre-2000   (1978–1999): {pre_corr:+.4f}")
print(f"    Post-2000  (2000–2024): {post_corr:+.4f}")
