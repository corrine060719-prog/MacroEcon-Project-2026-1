# Intermediate Macroeconomics: Data Analysis Project
### China's Economic Development, 1978–2024: A Comparative Macroeconomic Analysis

> **Course:** Intermediate Macroeconomics  
> **Due Date:** April 23, 2026  
> **Group Size:** 5 members  

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Data Description](#data-description)
4. [Methodology Summary](#methodology-summary)
5. [Key Findings](#key-findings)
6. [Team Contributions](#team-contributions)
7. [How to Reproduce](#how-to-reproduce)
8. [References](#references)

---

## Project Overview

This project provides an empirical analysis of China's macroeconomic development from 1978 to 2024, benchmarked against the United States. Using annual data on real GDP, consumption, investment, population, and youth unemployment, we:

- Describe and visualise long-run structural trends in both economies.
- Apply advanced time-series techniques (rolling volatility, HP filter) to characterise business cycle dynamics.
- Evaluate the degree of business cycle synchronisation between China and the US.
- Derive evidence-based policy recommendations addressing China's key macroeconomic challenges.

All analysis is fully reproducible: code is written in Python and documented with inline comments. Interactive visualisations are generated with Plotly and provided as standalone HTML files.

---

## Repository Structure

```
project-root/
│
├── data/
│   └── macro_data_clean_1978_2024.csv        # Final cleaned dataset (Task 1)
│
├── code/
│   ├── task3_analysis.py                     # Rolling volatility & HP filter (Member 1)
│   └── generate_charts_final_v2.py           # Interactive Plotly charts (Member 3)
│
├── figures/
│   ├── figure1_rolling_volatility.html       # Interactive: China GDP volatility
│   ├── figure2_hp_trend.html                 # Interactive: HP trend decomposition
│   ├── figure3_hp_cycles.html                # Interactive: Cyclical components
│   ├── Chart_1_GDP_Growth_Comparison.html    # Interactive: China vs US growth
│   ├── Chart_2_Consumption_Investment_Rates.html  # Interactive: Stacked area
│   └── Chart_3_Youth_Unemployment_vs_GDP.html     # Interactive: Scatter + regression
│
├── report/
│   ├── final_report_and_policy_brief.pdf     # Full report + Task 4 policy brief (PDF)
│   └── interactive_appendix.html            # All 6 charts in one interactive HTML page
│
└── README.md                                 # This file
```

---

## Data Description

| Variable | Abbreviation | Unit | Source | Coverage |
|---|---|---|---|---|
| China Real GDP | CRGDP | Billions USD (constant 2015 prices) | NBS / World Bank | 1978–2024 |
| China Gross Capital Formation | CGCF | Billions CNY | NBS / CEIC | 1978–2024 |
| China Final Consumption Expenditure | CFCE | Billions CNY | NBS / CEIC | 1978–2024 |
| China Total Population | CPOP | 10,000 Persons | NBS | 1978–2024 |
| China Fixed Asset Investment | CFAI | Billions CNY | NBS / CEIC | 1990–2024 |
| China Youth Unemployment Rate (16–24) | CYUR | Percent | NBS / ILO | 1991–2024 |
| US Real GDP | USRGDP | Billions USD (constant 2017 prices) | FRED | 1978–2024 |
| US Personal Consumption Expenditure | USPCE | Billions USD | FRED | 1978–2024 |

**Data Processing Notes:**
- Youth unemployment data are unavailable before 1991 (ILO data availability). Pre-1991 observations are excluded rather than interpolated given the structural break of the pre-reform labour market.
- Fixed Asset Investment (CFAI) is unavailable before 1990 as NBS did not report to SNA international standards before that year. Pre-1990 cells are left as NaN.
- US GDP was converted to CNY using annual average USD/CNY exchange rates (PBoC / FRED series DEXCHUS).
- All monetary series are expressed in constant prices to eliminate inflationary distortion.
- All known data gaps and methodological notes are recorded in the `README_notes` column of the CSV.

---

## Methodology Summary

### Task 1: Data Collection & Cleaning
Annual data were collected from NBS, CEIC, and FRED. Raw series were standardised to a common unit basis, missing values were treated per the notes above, and the final clean dataset was exported to `macro_data_clean_1978_2024.csv`.

### Task 2: Descriptive Analysis & Visualisation
Three interactive visualisations were produced using Plotly (Python ≥ 3.9):
1. **Dual-axis line chart** – China vs. US real GDP growth rates (1979–2024), with annotations for WTO accession (2001), GFC (2008), COVID-19 (2020), and post-2023 rebalancing.
2. **Stacked area chart** – China's consumption rate and capital formation rate as shares of GDP, highlighting the investment-led growth phase (2000–2012) and subsequent rebalancing.
3. **Scatter plot with regression line** – Youth unemployment rate vs. GDP growth (2020–2024), with OLS regression (slope = −0.27, R² = 0.14).

### Task 3: Advanced Time-Series Analysis

#### 3.1 Rolling Volatility
The 10-year rolling standard deviation of China's year-on-year real GDP growth rate is calculated as:

$$\sigma_t^{(10)} = \sqrt{\frac{1}{9} \sum_{s=t-9}^{t} \left(g_s - \bar{g}_{[t-9,t]}\right)^2}$$


#### 3.2 HP Filter — Business Cycle Decomposition
The Hodrick–Prescott (1997) filter decomposes log-level real GDP $y_t$ into trend $\tau_t$ and cycle $c_t$:

$$\min_{\{\tau_t\}} \left\lbrace \sum_{t=1}^{T}(y_t - \tau_t)^2 + \lambda \sum_{t=2}^{T-1}\left[(\tau_{t+1} - \tau_t) - (\tau_t - \tau_{t-1})\right]^2 \right\rbrace$$

Annual data: $\lambda = 100$ (Ravn & Uhlig, 2002). Business cycle synchronisation is measured via Pearson correlation of the two cyclical series.

**Key results (real data):**

| Sub-sample | Period | Pearson r |
|---|---|---|
| Full sample | 1978–2024 | +0.252 |
| Pre-2000 | 1978–1999 | +0.453 |
| Post-2000 | 2000–2024 | −0.106 |

### Task 4: Policy Brief
A policy brief (1) rising youth unemployment amid moderate GDP growth; (2) structural imbalances between consumption and investment. Each challenge is paired with a policy recommendation comprising a measurable objective, evidence-based rationale, and concrete implementation steps. At least two peer-reviewed academic sources are cited.

---

## Key Findings

### Rolling Volatility
- China's 10-year rolling growth volatility **declined substantially** from above 4.7 pp in the late 1980s to a historic low near 1.4 pp in 2003–2004, consistent with the 'Chinese Great Moderation'.
- A modest uptick around 2007–2009 reflects the GFC shock; post-COVID stabilisation has returned rolling volatility to approximately 2.3 pp.

### HP Filter — Business Cycle Decomposition
- China's trend GDP growth has followed a **monotonically declining path** since the early 2000s: from above 10% to approximately 5–6% in the early 2020s, consistent with convergence dynamics.
- **Post-2000 decoupling:** The correlation between the Chinese and US cyclical components falls from +0.45 (pre-2000) to −0.11 (post-2000), indicating China's cycle is driven primarily by domestic policy levers rather than synchronised demand shocks with the US.

### Structural Trends
- China's **investment rate** peaked above 55% during 2011–2013, one of the highest sustained rates ever recorded, before declining to 42.4% in 2024.
- The **consumption rate** fell to a trough of ~50.7% and has partially recovered to 53.4%, remaining well below the 60–70% typical of developed economies.
- **Youth unemployment** rose sharply to 15.56% in 2023, reflecting structural mismatch between graduate supply and labour market demand.

---

## Team Contributions

| Member | Name | Role | Tasks |
|---|---|---|---|
| **Member 1** | **陈锐** (Team Lead) | Advanced analysis & project management | Task 3.2: HP filter, rolling volatility, Figures 1–3; GitHub repository management; README; final report compilation; ZIP packaging |
| **Member 2** | **阮熙** | Data collection & cleaning | Task 1: Sourced all variables from NBS/CEIC/FRED; linear interpolation for missing values; unit standardisation; USD–CNY conversion; CSV export |
| **Member 3** | **蓝尹梓** | Visualisation | Task 2.2: Three required Plotly interactive charts (dual-axis GDP growth, stacked area consumption/investment, scatter + regression for youth unemployment) |
| **Member 4** | **李牧画** | Economic research | Tasks 2.1 & 3.1: Variable definitions table; descriptive statistics; interpretive summary paragraph; academic references |
| **Member 5** | **刘子睿** | Policy analysis | Task 4: Policy brief (≤5 pages); two empirical challenges; policy recommendations with measurable objectives, evidence-based rationale, and implementation steps |

---

## How to Reproduce

### Requirements
```
Python >= 3.9
pandas >= 1.5
numpy >= 1.23
statsmodels >= 0.13
plotly >= 5.10
scipy >= 1.9
```

- `generate_charts_final_v2.py` (updated): Original script contained hardcoded Windows absolute paths (`d:/桌面文件/大二下学期/中宏/...`). All paths have been replaced with relative filenames so the script runs on any OS from the project root.

Install all dependencies:
```bash
pip install pandas numpy statsmodels plotly scipy
```

### Steps
1. Place the clean dataset at the project root as `macro_data_clean_1978_2024.csv`.
2. Run the Task 3 analysis script (Figures 1–3):
   ```bash
   python code/task3_analysis.py
   ```
3. Run the Task 2 visualisation script (Charts 1–3):
   ```bash
   python code/generate_charts_final_v2.py
   ```
   Output HTML figures will be written to the `figures/` directory.

---

## References

- Cai, F. (2007). Demographic transition, demographic dividend, and the Lewis turning point in China. *Economic Research Journal*, 4, 4–13.
- Eggertsson, G. B., Mehrotra, N. R., & Robbins, J. A. (2019). A model of secular stagnation: Theory and quantitative evaluation. *American Economic Journal: Macroeconomics*, 11(1), 1–48.
- Hodrick, R. J., & Prescott, E. C. (1997). Postwar US business cycles: An empirical investigation. *Journal of Money, Credit and Banking*, 29(1), 1–16.
- Kose, M. A., Otrok, C., & Prasad, E. (2012). Global business cycles: Convergence or decoupling? *International Economic Review*, 53(2), 511–538.
- National Bureau of Statistics of China (NBS). (2024). *China Statistical Yearbook 2024*. China Statistics Press.
- Ravn, M. O., & Uhlig, H. (2002). On adjusting the Hodrick-Prescott filter for the frequency of observations. *Review of Economics and Statistics*, 84(2), 371–376.
- World Bank. (2023). *China Economic Update — December 2023*. Washington, DC: The World Bank Group.
- Zhang, B. (2023). Structural factors in the soaring youth unemployment rate in China. SMBC Economic Research.
- Federal Reserve Bank of St. Louis. FRED Economic Data. https://fred.stlouisfed.org

---

Project hosted on GitHub: https://github.com/corrine060719-prog/MacroEcon-Project-2026-1
