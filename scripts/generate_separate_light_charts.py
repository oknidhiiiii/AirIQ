import os
import matplotlib.pyplot as plt
import numpy as np

# Ensure destination directory exists
OUT_DIR = "/home/adityap/Desktop"
LOCAL_DIR = "presentation/charts"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(LOCAL_DIR, exist_ok=True)

# Common light theme styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'DejaVu Sans'

BG_COLOR = '#FFFFFF'
CARD_BG = '#F8FAFC'
BORDER_COLOR = '#CBD5E1'
GRID_COLOR = '#E2E8F0'
TEXT_DARK = '#0F172A'
TEXT_MUTED = '#475569'

def apply_light_theme(ax):
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=TEXT_DARK, labelsize=11)
    ax.xaxis.label.set_color(TEXT_DARK)
    ax.yaxis.label.set_color(TEXT_DARK)
    ax.title.set_color(TEXT_DARK)
    ax.grid(color=GRID_COLOR, linestyle='--', linewidth=0.8, alpha=0.9)
    for spine in ax.spines.values():
        spine.set_color(BORDER_COLOR)
        spine.set_linewidth(1.2)

# ==============================================================================
# CHART 1: PySpark MLlib Feature Importance Breakdown
# ==============================================================================
def generate_chart_feature_importance():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    apply_light_theme(ax)

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

    bars = ax.barh(y_pos, importance, color='#FF5A5F', height=0.55, edgecolor='#E11D48', linewidth=1.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(features, fontsize=11, fontweight='bold', color=TEXT_DARK)
    ax.invert_yaxis()
    ax.set_xlabel('Predictive Feature Importance (%)', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_title('AirIQ: PySpark MLlib Feature Importance Breakdown', fontsize=15, fontweight='bold', pad=18, color=TEXT_DARK)
    ax.set_xlim(0, 38)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.6, bar.get_y() + bar.get_height()/2, f'{w:.2f}%', 
                ha='left', va='center', color='#9F1239', fontweight='bold', fontsize=11)

    # Subtitle / note
    fig.text(0.5, 0.015, 'Trained on 224,098 Verified Airbnb Listings | 45 Random Forest Trees (Max Depth = 9)', 
             ha='center', fontsize=10, color=TEXT_MUTED)

    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    out_path = os.path.join(OUT_DIR, "chart_1_feature_importance.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.savefig(os.path.join(LOCAL_DIR, "chart_1_feature_importance.png"), facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[+] Saved: {out_path}")

# ==============================================================================
# CHART 2: Error Metrics (Random Forest vs Baseline OLS)
# ==============================================================================
def generate_chart_error_metrics():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    apply_light_theme(ax)

    metrics = ['RMSE\n(Root Mean Squared Error)', 'MAE\n(Mean Absolute Error)']
    baseline_vals = [323.37, 183.32]
    rf_vals = [209.98, 114.58]
    x = np.arange(len(metrics))
    width = 0.30

    b1 = ax.bar(x - width/2, baseline_vals, width, label='Baseline Linear Regression (OLS)', color='#94A3B8', edgecolor='#64748B', linewidth=1.5)
    b2 = ax.bar(x + width/2, rf_vals, width, label='AirIQ PySpark Random Forest', color='#10B981', edgecolor='#059669', linewidth=1.5)

    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=12, fontweight='bold', color=TEXT_DARK)
    ax.set_ylabel('Model Error in USD ($)', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_title('AirIQ: Predictive Error Comparison (Random Forest vs Baseline OLS)', fontsize=15, fontweight='bold', pad=18, color=TEXT_DARK)
    ax.set_ylim(0, 390)
    ax.legend(facecolor='#FFFFFF', edgecolor='#CBD5E1', labelcolor=TEXT_DARK, fontsize=11, loc='upper right')

    for bar, val in zip(b1, baseline_vals):
        ax.text(bar.get_x() + bar.get_width()/2, val + 6, f'${val:.2f}', ha='center', va='bottom', color='#475569', fontweight='bold', fontsize=11)

    for bar, val in zip(b2, rf_vals):
        ax.text(bar.get_x() + bar.get_width()/2, val + 6, f'${val:.2f}', ha='center', va='bottom', color='#065F46', fontweight='bold', fontsize=11)

    # Reduction badges
    ax.text(0, 260, '▼ 35.1% Lower RMSE', ha='center', color='#991B1B', fontweight='bold', fontsize=11, 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEE2E2', edgecolor='#EF4444', linewidth=1.5))
    ax.text(1, 150, '▼ 37.5% Lower MAE', ha='center', color='#991B1B', fontweight='bold', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEE2E2', edgecolor='#EF4444', linewidth=1.5))

    fig.text(0.5, 0.015, 'Evaluated on 44,272 Held-Out Test Records (20% Split) across 9 International Markets', 
             ha='center', fontsize=10, color=TEXT_MUTED)

    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    out_path = os.path.join(OUT_DIR, "chart_2_error_metrics.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.savefig(os.path.join(LOCAL_DIR, "chart_2_error_metrics.png"), facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[+] Saved: {out_path}")

# ==============================================================================
# CHART 3: Model Variance Explained (R² Score Comparison)
# ==============================================================================
def generate_chart_r2_variance():
    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    apply_light_theme(ax)

    models = ['Baseline Linear Regression (OLS)', 'AirIQ PySpark Random Forest\n(45 Trees, Depth 9)']
    r2_scores = [0.1463, 0.3659]
    colors_r2 = ['#94A3B8', '#0284C7']
    edge_r2 = ['#64748B', '#0369A1']

    bars = ax.bar(models, r2_scores, color=colors_r2, width=0.45, edgecolor=edge_r2, linewidth=1.5)
    ax.set_ylabel('Coefficient of Determination (R² Score)', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_title('AirIQ: Model Variance Explained (R² Score Comparison)', fontsize=15, fontweight='bold', pad=18, color=TEXT_DARK)
    ax.set_ylim(0, 0.46)

    for bar, val in zip(bars, r2_scores):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.012, f'{val:.4f}\n({val*100:.1f}%)', 
                ha='center', va='bottom', color=TEXT_DARK, fontweight='bold', fontsize=12)

    ax.text(0.5, 0.28, '▲ 150.1% Higher R² Score\n(2.5x More Variance Captured)', ha='center', color='#0369A1', fontweight='bold', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=1.5))

    fig.text(0.5, 0.015, 'R² demonstrates non-linear ensemble trees outperform rigid single-plane linear baselines', 
             ha='center', fontsize=10, color=TEXT_MUTED)

    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    out_path = os.path.join(OUT_DIR, "chart_3_r2_variance.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.savefig(os.path.join(LOCAL_DIR, "chart_3_r2_variance.png"), facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[+] Saved: {out_path}")

# ==============================================================================
# CHART 4: Regional Pricing Benchmark Across All 9 Markets
# ==============================================================================
def generate_chart_city_pricing():
    fig, ax = plt.subplots(figsize=(11, 6.8), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    apply_light_theme(ax)

    cities = ['Bengaluru', 'Mumbai', 'Rome', 'London', 'New York', 'Paris', 'Amsterdam', 'Tokyo', 'Sydney']
    usd_equiv_prices = [33.1, 67.9, 256.2, 296.3, 280.6, 323.2, 364.0, 182.3, 298.6]
    currencies = ['₹2,784', '₹5,707', '€237', '£228', '$281', '€299', '€337', '¥27,207', 'A$452']

    bars = ax.bar(cities, usd_equiv_prices, color='#F97316', width=0.55, edgecolor='#C2410C', linewidth=1.5)
    ax.set_ylabel('Normalized Nightly Rate in USD ($)', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_title('AirIQ: Average Observed Nightly Rates Across All 9 Markets', fontsize=15, fontweight='bold', pad=18, color=TEXT_DARK)
    ax.set_xticklabels(cities, rotation=25, ha='right', fontsize=11, fontweight='bold', color=TEXT_DARK)
    ax.set_ylim(0, 430)

    for bar, curr, usd in zip(bars, currencies, usd_equiv_prices):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 8, f'{curr}\n(${usd:.0f})', 
                ha='center', va='bottom', color='#9A3412', fontweight='bold', fontsize=9.5)

    fig.text(0.5, 0.015, 'Authentic Native Currencies Annotated Above Bars (USD Normalization Baseline Used for Spatial Cross-Comparison)', 
             ha='center', fontsize=10, color=TEXT_MUTED)

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    out_path = os.path.join(OUT_DIR, "chart_4_city_pricing.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.savefig(os.path.join(LOCAL_DIR, "chart_4_city_pricing.png"), facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[+] Saved: {out_path}")

if __name__ == "__main__":
    generate_chart_feature_importance()
    generate_chart_error_metrics()
    generate_chart_r2_variance()
    generate_chart_city_pricing()
