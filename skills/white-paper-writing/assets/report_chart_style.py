"""Optional neutral chart defaults; adapt to the report's requested brand."""


def configure():
    import matplotlib as mpl
    mpl.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 10,
        "figure.facecolor": "white", "axes.facecolor": "white",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.labelcolor": "#243746", "text.color": "#243746",
        "grid.color": "#DEE4E8", "grid.linewidth": 0.6,
        "legend.frameon": False, "pdf.fonttype": 42, "ps.fonttype": 42,
    })


def save_figure(fig, directory, stem):
    from pathlib import Path
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "png"):
        fig.savefig(target / f"{stem}.{suffix}", bbox_inches="tight", dpi=300)
