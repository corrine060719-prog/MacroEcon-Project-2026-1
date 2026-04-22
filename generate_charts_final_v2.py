"""
中宏经济学数据分析 - 学术可视化 (美化版)
基于 图.py 优化，参考CLAUDE.md要求和经济学期刊风格
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
from scipy import stats

# ============ 数据加载 ============
df = pd.read_csv("macro_data_clean_1978_2024.csv")
df_clean = df.dropna(subset=['CN_RGDP_growth_pct', 'US_RGDP_growth_pct'])

print(f"Data loaded: {len(df_clean)} years ({df_clean['Year'].min()}-{df_clean['Year'].max()})")

# ============ 学术配色方案 (经济学顶刊风格) ============
COLORS = {
    'china': '#8B0000',           # 深红 (中国)
    'china_light': '#C41E3A',     # 中国红
    'us': '#003366',              # 深蓝 (美国)
    'us_light': '#1E3A5F',        # 美国蓝
    'consumption': '#27AE60',     # 绿色 (消费)
    'investment': '#E67E22',      # 橙色 (投资)
    'text': '#2C3E50',            # 深灰文字
    'grid': '#E8E8E8',            # 浅灰网格
    'regression': '#34495E',      # 回归线
}

# ============ 图表1: 中美GDP增长率 (双轴折线图) ============
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

# 中国实际GDP增长率 (主Y轴)
fig1.add_trace(
    go.Scatter(
        x=df_clean['Year'],
        y=df_clean['CN_RGDP_growth_pct'],
        name="China",
        line=dict(color=COLORS['china'], width=2.5, shape='spline'),
        mode='lines+markers',
        marker=dict(size=5, symbol='circle'),
        connectgaps=True,
        hovertemplate='<b>China</b><br>Year: %{x}<br>Growth: %{y:.1f}%<extra></extra>'
    ),
    secondary_y=False,
)

# 美国实际GDP增长率 (副Y轴)
fig1.add_trace(
    go.Scatter(
        x=df_clean['Year'],
        y=df_clean['US_RGDP_growth_pct'],
        name="United States",
        line=dict(color=COLORS['us'], width=2.5, dash='dash', shape='spline'),
        mode='lines+markers',
        marker=dict(size=5, symbol='diamond'),
        connectgaps=True,
        hovertemplate='<b>US</b><br>Year: %{x}<br>Growth: %{y:.1f}%<extra></extra>'
    ),
    secondary_y=True,
)

# 零线
fig1.add_hline(y=0, line_dash="dot", line_color="gray", opacity=0.5, secondary_y=False)
fig1.add_hline(y=0, line_dash="dot", line_color="gray", opacity=0.5, secondary_y=True)

# 结构性转变节点标注
shifts = [
    dict(year=2001, y=8.4, text="<b>2001</b><br>WTO<br>Accession", color=COLORS['china']),
    dict(year=2008, y=9.6, text="<b>2008</b><br>Financial<br>Crisis", color='#E67E22'),
    dict(year=2020, y=1.2, text="<b>2020</b><br>COVID-19<br>Pandemic", color='#C0392B'),
    dict(year=2023, y=6.0, text="<b>2023</b><br>Post-Pandemic<br>Rebalancing", color='#27AE60'),
]

for shift in shifts:
    fig1.add_vline(x=shift['year'], line_width=1.2, line_dash="dot", line_color="slategray", opacity=0.6)
    fig1.add_annotation(
        x=shift['year'], y=shift['y'],
        text=shift['text'],
        showarrow=True, arrowhead=2, arrowsize=0.7,
        arrowcolor=shift['color'], ax=0, ay=-35,
        bgcolor="rgba(255,255,255,0.95)", bordercolor=shift['color'],
        font=dict(size=9, color=shift['color'])
    )

# 高亮区域 - 中国高速增长期
fig1.add_vrect(x0=2003, x1=2012, fillcolor="rgba(139, 0, 0, 0.05)", layer="below", line_width=0)

fig1.update_layout(
    title=dict(
        text='<b>China vs. U.S. Real GDP Growth Rates</b><br><span style="font-size:12px; color:#666;">1979–2024</span>',
        x=0.5,
        font=dict(size=17, family="Georgia, serif")
    ),
    xaxis=dict(
        title=dict(text='Year', font=dict(size=12)),
        tickmode='linear', dtick=5,
        gridcolor=COLORS['grid'], showgrid=True,
        linecolor='#333', tickfont=dict(size=10)
    ),
    legend=dict(
        x=0.5, y=1.15, xanchor='center', orientation='h',
        bgcolor='rgba(255,255,255,0.95)', bordercolor='#ddd', borderwidth=1,
        font=dict(size=11)
    ),
    template="plotly_white",
    hovermode="x unified",
    plot_bgcolor='white',
    margin=dict(l=65, r=65, t=130, b=70),
    height=520
)

fig1.update_yaxes(title_text="<b>China GDP Growth (%)</b>", secondary_y=False,
                  gridcolor=COLORS['grid'], tickfont=dict(size=10))
fig1.update_yaxes(title_text="<b>U.S. GDP Growth (%)</b>", secondary_y=True,
                  gridcolor=COLORS['grid'], tickfont=dict(size=10))

# 数据来源脚注
fig1.add_annotation(
    dict(x=0, y=-0.18, xref='paper', yref='paper',
         text='<i>Source: National Bureau of Statistics (NBS), World Bank, FRED</i>',
         showarrow=False, font=dict(size=10, color="gray"), align='left')
)

fig1.write_html("Chart_1_GDP_Growth_Comparison.html")

# ============ 图表2: 消费率与资本形成率 (堆叠面积图) ============
fig2 = go.Figure()

# 消费率 (Consumption Rate) - 绿色系
fig2.add_trace(go.Scatter(
    x=df['Year'], y=df['CN_consumption_rate'],
    mode='lines',
    line=dict(width=0),
    name='Consumption Rate',
    fill='tozeroy',
    fillcolor='rgba(39, 174, 96, 0.8)',
    hovertemplate='<b>Consumption Rate</b><br>Year: %{x}<br>Rate: %{y:.1f}%<extra></extra>'
))

# 资本形成率 (Capital Formation Rate) - 橙色系
fig2.add_trace(go.Scatter(
    x=df['Year'], y=df['CN_investment_rate'],
    mode='lines',
    line=dict(width=0),
    name='Investment Rate',
    fill='tozeroy',
    fillcolor='rgba(230, 126, 34, 0.8)',
    hovertemplate='<b>Investment Rate</b><br>Year: %{x}<br>Rate: %{y:.1f}%<extra></extra>'
))

# 投资主导型增长阶段阴影 (2000-2012)
fig2.add_vrect(x0=2000, x1=2012, fillcolor="rgba(230, 126, 34, 0.15)", layer="below", line_width=0)
fig2.add_annotation(
    x=2006, y=56,
    text="<b>Investment-led<br>Growth Phase</b><br><span style='font-size:10px'>2000–2012</span>",
    showarrow=False,
    bgcolor="rgba(255, 229, 153, 0.9)",
    bordercolor='#E67E22',
    font=dict(size=11, color='#333')
)

# 消费驱动转变阶段 (2013-Present)
fig2.add_vrect(x0=2013, x1=2024, fillcolor="rgba(39, 174, 96, 0.1)", layer="below", line_width=0)
fig2.add_annotation(
    x=2018.5, y=56,
    text="<b>Shift toward<br>Consumption</b><br><span style='font-size:10px'>2013–Present</span>",
    showarrow=True, arrowhead=2,
    arrowcolor=COLORS['consumption'], ax=40, ay=-15,
    bgcolor="rgba(255,255,255,0.95)",
    bordercolor=COLORS['consumption'],
    font=dict(size=10, color=COLORS['consumption'])
)

# 关键节点标注
fig2.add_annotation(x=1992, y=38, text="1992: Reform",
                    showarrow=True, arrowhead=2, arrowcolor='#7F8C8D',
                    ax=0, ay=-25, bgcolor="white", bordercolor='#ddd',
                    font=dict(size=9, color='#555'))

fig2.update_layout(
    title=dict(
        text="<b>China's Consumption and Capital Formation Rates</b><br><span style='font-size:12px; color:#666;'>1978–2024 (% of GDP)</span>",
        x=0.5,
        font=dict(size=17, family="Georgia, serif")
    ),
    xaxis=dict(
        title=dict(text='Year', font=dict(size=12)),
        tickmode='linear', dtick=5,
        gridcolor=COLORS['grid'], showgrid=True,
        linecolor='#333', tickfont=dict(size=10),
        range=[1977, 2025]
    ),
    yaxis=dict(
        title=dict(text='<b>Percentage of GDP (%)</b>', font=dict(size=12)),
        gridcolor=COLORS['grid'], showgrid=True,
        linecolor='#333', tickfont=dict(size=10),
        range=[30, 72]
    ),
    legend=dict(
        x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.95)',
        bordercolor="#D3D3D3", borderwidth=1,
        font=dict(size=11)
    ),
    template="plotly_white",
    hovermode="x unified",
    plot_bgcolor='white',
    margin=dict(l=65, r=35, t=130, b=70),
    height=520
)

fig2.add_annotation(
    dict(x=0, y=-0.18, xref='paper', yref='paper',
         text='<i>Source: National Bureau of Statistics (NBS), World Bank</i>',
         showarrow=False, font=dict(size=10, color="gray"), align='left')
)

fig2.write_html("Chart_2_Consumption_Investment_Rates.html")

# ============ 图表3: 青年失业率与GDP增长 (散点图+回归线) ============
df_recent = df[(df['Year'] >= 2020) & (df['Year'] <= 2024)].dropna(
    subset=['CN_RGDP_growth_pct', 'CN_Youth_unemp']
).copy()

# 计算回归
x = df_recent['CN_RGDP_growth_pct'].values
y = df_recent['CN_Youth_unemp'].values
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# 扩展回归线范围
x_line = np.linspace(-1, 12, 100)
y_line = slope * x_line + intercept

# 置信区间
y_pred = slope * x + intercept
residuals = y - y_pred
se = np.std(residuals)
ci_upper = y_line + 1.96 * se
ci_lower = y_line - 1.96 * se

fig3 = go.Figure()

# 95%置信区间
fig3.add_trace(go.Scatter(
    x=np.concatenate([x_line, x_line[::-1]]),
    y=np.concatenate([ci_upper, ci_lower[::-1]]),
    fill='toself',
    fillcolor='rgba(52, 73, 94, 0.1)',
    line=dict(color='rgba(52, 73, 94, 0)'),
    name='95% Confidence Interval',
    hoverinfo='skip'
))

# 年份颜色映射
year_colors = {2020: '#E74C3C', 2021: '#E67E22', 2022: '#F39C12', 2023: '#3498DB', 2024: '#2980B9'}

# 散点
for year in sorted(df_recent['Year'].unique()):
    mask = df_recent['Year'] == year
    fig3.add_trace(go.Scatter(
        x=df_recent.loc[mask, 'CN_RGDP_growth_pct'],
        y=df_recent.loc[mask, 'CN_Youth_unemp'],
        mode='markers+text',
        name=str(year),
        text=[f"{year}<br>{df_recent.loc[mask, 'CN_Youth_unemp'].values[0]:.1f}%"],
        textposition='top center',
        textfont=dict(size=9, color='#333'),
        marker=dict(
            size=16,
            color=year_colors.get(year, '#2C3E50'),
            line=dict(color='white', width=2)
        ),
        hovertemplate=f'<b>{year}</b><br>GDP Growth: %{{x:.1f}}%<br>Youth Unemployment: %{{y:.1f}}%<extra></extra>'
    ))

# 回归线
fig3.add_trace(go.Scatter(
    x=x_line, y=y_line,
    mode='lines',
    name=f'OLS Regression (R²={r_value**2:.3f})',
    line=dict(color=COLORS['regression'], width=3, dash='dash'),
    hovertemplate='GDP: %{x:.1f}% → Unemployment: %{y:.1f}%<extra></extra>'
))

# 统计信息
stats_text = (f"<b>Regression Results</b><br>"
              f"y = {slope:.2f}x + {intercept:.2f}<br>"
              f"R² = {r_value**2:.3f}<br>"
              f"p = {p_value:.3f}<br>"
              f"n = {len(x)}")

fig3.update_layout(
    title=dict(
        text="<b>Youth Unemployment vs. GDP Growth in China</b><br><span style='font-size:12px; color:#666;'>2020–2024</span>",
        x=0.5,
        font=dict(size=17, family="Georgia, serif")
    ),
    xaxis=dict(
        title=dict(text='<b>Real GDP Growth Rate (%)</b>', font=dict(size=12)),
        gridcolor=COLORS['grid'], showgrid=True,
        linecolor='#333', tickfont=dict(size=10),
        zeroline=True, zerolinecolor='gray',
        range=[-1, 12]
    ),
    yaxis=dict(
        title=dict(text='<b>Youth Unemployment Rate (%)</b>', font=dict(size=12)),
        gridcolor=COLORS['grid'], showgrid=True,
        linecolor='#333', tickfont=dict(size=10),
        range=[10, 17]
    ),
    legend=dict(
        x=0.5, y=1.15, xanchor='center', orientation='h',
        bgcolor='rgba(255,255,255,0.95)', bordercolor='#ddd', borderwidth=1,
        font=dict(size=10)
    ),
    template="plotly_white",
    hovermode='closest',
    plot_bgcolor='white',
    margin=dict(l=65, r=65, t=130, b=70),
    height=520,
    annotations=[dict(
        x=0.98, y=0.98,
        text=stats_text,
        showarrow=False, xref="paper", yref="paper",
        bgcolor="rgba(248,248,248,0.95)", bordercolor='#ddd',
        font=dict(size=10, color='#2C3E50'),
        align="left", xanchor='right', yanchor='top'
    )]
)

fig3.add_annotation(
    dict(x=0, y=-0.18, xref='paper', yref='paper',
         text='<i>Source: National Bureau of Statistics (NBS), ILO, World Bank</i>',
         showarrow=False, font=dict(size=10, color="gray"), align='left')
)

fig3.write_html("Chart_3_Youth_Unemployment_vs_GDP.html")

# ============ 合并生成主HTML (可选) ============
# html_template = """<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>China Macroeconomic Analysis</title>
#     <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
#     <style>
#         * {{ margin: 0; padding: 0; box-sizing: border-box; }}
#         body {{
#             font-family: 'Georgia', 'Times New Roman', serif;
#             background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
#             min-height: 100vh;
#             padding: 30px 20px;
#         }}
#         .container {{ max-width: 1050px; margin: 0 auto; }}
#         h1 {{
#             text-align: center;
#             color: #fff;
#             font-size: 30px;
#             font-weight: 400;
#             letter-spacing: 2px;
#             margin-bottom: 8px;
#             text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
#         }}
#         .subtitle {{
#             text-align: center;
#             color: rgba(255,255,255,0.7);
#             font-size: 13px;
#             margin-bottom: 35px;
#             font-family: 'Arial', sans-serif;
#         }}
#         .chart {{
#             background: #fff;
#             border-radius: 12px;
#             padding: 25px;
#             margin-bottom: 30px;
#             box-shadow: 0 15px 50px rgba(0,0,0,0.35), 0 8px 20px rgba(0,0,0,0.2);
#         }}
#     </style>
# </head>
# <body>
#     <div class="container">
#         <h1>China Macroeconomic Analysis</h1>
#         <p class="subtitle">Intermediate Macroeconomics • 1978–2024</p>
#
#         <div class="chart">{fig1}</div>
#         <div class="chart">{fig2}</div>
#         <div class="chart">{fig3}</div>
#     </div>
# </body>
# </html>
# """
#
# combined = html_template.format(
#     fig1=fig1.to_html(full_html=False, include_plotlyjs=False),
#     fig2=fig2.to_html(full_html=False, include_plotlyjs=False),
#     fig3=fig3.to_html(full_html=False, include_plotlyjs=False)
# )
#
# with open("macro_analysis_charts.html", 'w', encoding='utf-8') as f:
#     f.write(combined)

print("\nAll charts generated successfully!")
print("Output: Chart_1_GDP_Growth_Comparison.html")
print("Output: Chart_2_Consumption_Investment_Rates.html")
print("Output: Chart_3_Youth_Unemployment_vs_GDP.html")