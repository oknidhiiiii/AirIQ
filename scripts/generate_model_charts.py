import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("presentation/charts", exist_ok=True)
OUT_PATH = "/home/adityap/Desktop/model_evaluation_charts.png"
LOCAL_OUT = "presentation/charts/model_evaluation_charts.png"

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'DejaVu Sans'
fig, axs = plt.subplots(2, 2, figsize=(16, 11), dpi=300)
fig.patch.set_facecolor('#0F172A') # Dark Slate background

# Palette
C_PRIMARY = '#FF5A5F' # Airbnb Coral
C_ACCENT = '#38BDF8'  # Sky Blue
C_ORANGE = '#FB923C'  # Spark Orange
C_EMERALD = '#34D399' # Mint/Emerald
C_TEXT = '#F8FAFC'    # Crisp white text
C_MUTED = '#94A3B8'   # Slate 400

for ax in axs.flat:
    ax.set_facecolor('#1E293B')
    ax.tick_params(colors=C_TEXT, labelsize=10)
    ax.xaxis.label.set_color(C_TEXT)
    ax.yaxis.label.set_color(C_TEXT)
    ax.title.set_color(C_TEXT)
    ax.grid(color='#334155', linestyle='--', linewidth=0.7, alpha=0.7)
    for spine in ax.spines.values():
        spine.set_color('#475569')

# ==============================================================================
# 1. Feature Importance (Horizontal Bar)
# ==============================================================================
features = [
    'Guest Capacity (accommodates)',
    'Geographic Market (city_idx)',
    'Dedicated Bedrooms (bedrooms)',
    'Room Privacy Type (room_idx)',
    'Bathrooms Count (bathrooms)',
    'Review Rating (scores_rating)'
]
importance = [31.41, 22.68, 21.98, 11.20, 8.85, 3.88]
y_pos = np.arange(len(features))

bars1 = axs[0, 0].barh(y_pos, importance, color=C_PRIMARY, height=0.6, edgecolor='#FDA4AF', linewidth=1)
axs[0, 0].set_yticks(y_pos)
axs[0, 0].set_yticklabels(features, fontsize=10, fontweight='bold', color=C_TEXT)
axs[0, 0].invert_yaxis()
axs[0, 0].set_xlabel('Predictive Feature Importance (%)', fontsize=11, fontweight='bold')
axs[0, 0].set_title('A. PySpark MLlib Feature Importance Breakdown', fontsize=13, fontweight='bold', pad=12)
axs[0, 0].set_xlim(0, 38)

for bar in bars1:
    w = bar.get_width()
    axs[0, 0].text(w + 0.8, bar.get_y() + bar.get_height()/2, f'{w:.2f}%', 
                   ha='left', va='center', color=C_TEXT, fontweight='bold', fontsize=10)

# ==============================================================================
# 2. Error Metrics: Random Forest vs Baseline OLS (Grouped Bar)
# ==============================================================================
metrics = ['RMSE (Root Mean Sq Error)', 'MAE (Mean Absolute Error)']
baseline_vals = [323.37, 183.32]
rf_vals = [209.98, 114.58]
x = np.arange(len(metrics))
width = 0.32

b1 = axs[0, 1].bar(x - width/2, baseline_vals, width, label='Baseline Linear Regression (OLS)', color='#64748B', edgecolor='#94A3B8')
b2 = axs[0, 1].bar(x + width/2, rf_vals, width, label='AirIQ PySpark Random Forest', color=C_EMERALD, edgecolor='#A7F3D0')

axs[0, 1].set_xticks(x)
axs[0, 1].set_xticklabels(metrics, fontsize=11, fontweight='bold', color=C_TEXT)
axs[0, 1].set_ylabel('Error in USD ($)', fontsize=11, fontweight='bold')
axs[0, 1].set_title('B. Error Metrics: Random Forest vs Baseline OLS', fontsize=13, fontweight='bold', pad=12)
axs[0, 1].set_ylim(0, 390)
axs[0, 1].legend(facecolor='#0F172A', edgecolor='#475569', labelcolor=C_TEXT, fontsize=9.5)

for bar, val in zip(b1, baseline_vals):
    axs[0, 1].text(bar.get_x() + bar.get_width()/2, val + 7, f'${val:.2f}', ha='center', va='bottom', color=C_MUTED, fontweight='bold')

for bar, val in zip(b2, rf_vals):
    axs[0, 1].text(bar.get_x() + bar.get_width()/2, val + 7, f'${val:.2f}', ha='center', va='bottom', color='#A7F3D0', fontweight='bold')

# Reduction banner annotation
axs[0, 1].text(0, 260, '▼ 35.1% Lower RMSE', ha='center', color='#F87171', fontweight='bold', fontsize=10, 
               bbox=dict(boxstyle='round,pad=0.4', facecolor='#450A0A', edgecolor='#EF4444'))
axs[0, 1].text(1, 150, '▼ 37.5% Lower MAE', ha='center', color='#F87171', fontweight='bold', fontsize=10,
               bbox=dict(boxstyle='round,pad=0.4', facecolor='#450A0A', edgecolor='#EF4444'))

# ==============================================================================
# 3. Variance Explained (R² Score Comparison)
# ==============================================================================
r2_models = ['Baseline OLS', 'AirIQ Random Forest\n(45 Trees, Depth 9)']
r2_scores = [0.1463, 0.3659]
colors_r2 = ['#64748B', C_ACCENT]

b_r2 = axs[1, 0].bar(r2_models, r2_scores, color=colors_r2, width=0.42, edgecolor='#BAE6FD')
axs[1, 0].set_ylabel('Coefficient of Determination (R² Score)', fontsize=11, fontweight='bold')
axs[1, 0].set_title('C. Model Variance Explained (R² Score Comparison)', fontsize=13, fontweight='bold', pad=12)
axs[1, 0].set_ylim(0, 0.45)

for bar, val in zip(b_r2, r2_scores):
    axs[1, 0].text(bar.get_x() + bar.get_width()/2, val + 0.012, f'{val:.4f} ({val*100:.1f}%)', 
                   ha='center', va='bottom', color=C_TEXT, fontweight='bold', fontsize=11)

axs[1, 0].text(0.5, 0.28, '▲ 150% Increase in R²', ha='center', color='#38BDF8', fontweight='bold', fontsize=11,
               bbox=dict(boxstyle='round,pad=0.4', facecolor='#082F49', edgecolor='#0284C7'))

# ==============================================================================
# 4. Regional Pricing Benchmark Across Markets
# ==============================================================================
cities = ['Bengaluru', 'Mumbai', 'Rome', 'London', 'New York', 'Paris', 'Amsterdam', 'Tokyo', 'Sydney']
# Converted to approximate USD for comparability in this plot
usd_equiv_prices = [33.1, 67.9, 256.2, 296.3, 280.6, 323.2, 364.0, 182.3, 298.6]
currencies = ['₹2,784', '₹5,707', '€237', '£228', '$281', '€299', '€337', '¥27,207', 'A$452']

bars4 = axs[1, 1].bar(cities, usd_equiv_prices, color=C_ORANGE, width=0.55, edgecolor='#FED7AA')
axs[1, 1].set_ylabel('Normalized Price in USD ($)', fontsize=11, fontweight='bold')
axs[1, 1].set_title('D. Multi-City Pricing Benchmark (Local Currencies Displayed)', fontsize=13, fontweight='bold', pad=12)
axs[1, 1].set_xticklabels(cities, rotation=35, ha='right', fontsize=9.5, fontweight='bold', color=C_TEXT)
axs[1, 1].set_ylim(0, 430)

for bar, curr in zip(bars4, currencies):
    h = bar.get_height()
    axs[1, 1].text(bar.get_x() + bar.get_width()/2, h + 8, curr, 
                   ha='center', va='bottom', color='#FDE047', fontweight='bold', fontsize=9)

# Overall Super Title
plt.suptitle('AirIQ: Multi-City Airbnb Price Intelligence — Empirical Model Evaluation', 
             fontsize=17, fontweight='bold', color=C_TEXT, y=0.98)
plt.figtext(0.5, 0.015, 'Trained on 224,098 Real Rental Listings (80/20 Train-Test Split) | Apache Spark 4.2 MLlib & Apache Cassandra 4.1', 
            ha='center', fontsize=10.5, color=C_MUTED)

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig(OUT_PATH, facecolor=fig.get_facecolor(), edgecolor='none')
plt.savefig(LOCAL_OUT, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print(f"[+] Saved Model Evaluation Charts to: {OUT_PATH}")
