import matplotlib.pyplot as plt
import config
def plot_fares(results):
    """
    Renders a premium bar graph comparing transport fares using the app's visual style.
    """
    if not results:
        return
    companies = [item["company"] for item in results]
    fares = [item["fare"] for item in results]
    # Style the plot with a modern dark theme
    plt.style.use('dark_background')
    
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(config.BG_MAIN)
    ax.set_facecolor(config.BG_CARD)
    # Define brand accents for bars from config
    colors = [config.ACCENT, config.ACCENT2, config.WARNING]
    bar_colors = colors[:len(companies)]
    
    bars = ax.bar(companies, fares, color=bar_colors, width=0.45, edgecolor=config.BG_INPUT, linewidth=1)
    # Set labels and title with custom typography details from config
    ax.set_title("Manzil - Fare Comparison", fontsize=14, color=config.TEXT_LIGHT, fontweight='bold', pad=15)
    ax.set_ylabel("Fare (PKR)", fontsize=11, color=config.TEXT_MUTED, labelpad=10)
    ax.tick_params(colors=config.TEXT_MUTED, labelsize=10)
    # Display value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"Rs. {height:,.0f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),  # 5 points vertical offset
            textcoords="offset points",
            ha='center',
            va='bottom',
            fontsize=9.5,
            color=config.TEXT_LIGHT,
            fontweight='bold'
        )
    # Hide unnecessary borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(config.BG_INPUT)
    ax.spines['bottom'].set_color(config.BG_INPUT)
    # Add a light horizontal grid for readability
    ax.yaxis.grid(True, linestyle='--', alpha=0.15, color=config.TEXT_MUTED)
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.show()