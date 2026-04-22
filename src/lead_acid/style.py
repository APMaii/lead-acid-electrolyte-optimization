import matplotlib.pyplot as plt
from matplotlib import patheffects

SAMPLE_TEXT_COLOR = "#0B3D91"
SAMPLE_TEXT_STROKE = [patheffects.withStroke(linewidth=2.2, foreground="white")]


def apply_global_style() -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams["figure.figsize"] = (12, 7)
    plt.rcParams["font.size"] = 11
    plt.rcParams["axes.titlesize"] = 16
    plt.rcParams["axes.labelsize"] = 12
    plt.rcParams["xtick.labelsize"] = 10
    plt.rcParams["ytick.labelsize"] = 10
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.linewidth"] = 1.2
    plt.rcParams["grid.alpha"] = 0.35
    plt.rcParams["grid.linestyle"] = "--"
    plt.rcParams["savefig.dpi"] = 400
    plt.rcParams["figure.dpi"] = 140


def annotate_sample_number(
    ax, x, y, sample_id, *, fontsize=9, ha="left", va="bottom", boxed=False, zorder=6
):
    text = ax.text(
        x,
        y,
        str(int(sample_id)),
        fontsize=fontsize,
        color=SAMPLE_TEXT_COLOR,
        fontweight="bold",
        ha=ha,
        va=va,
        zorder=zorder,
    )
    text.set_path_effects(SAMPLE_TEXT_STROKE)
    if boxed:
        text.set_bbox(
            dict(
                facecolor="white",
                edgecolor="black",
                alpha=0.78,
                boxstyle="round,pad=0.16",
            )
        )
