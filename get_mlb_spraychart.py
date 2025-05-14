import matplotlib.pyplot as plt
from matplotlib import patches
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional
import seaborn as sns
import pandas as pd
import warnings
from statcast_utils import *

warnings.filterwarnings('ignore')
CUR_PATH = Path(__file__).resolve().parent

STADIUM_COORDS = pd.read_csv(Path(CUR_PATH, "STADIUM_DATA", "mlb_stadium_data.csv"))
BASE_COORDS = {
    "1B": (150, 175),
    "2B": (125, 150),
    "3B": (100, 175),
    "PM": (125, 177)  # Pitcher's mound
}
BASES = pd.DataFrame.from_dict(BASE_COORDS, orient='index', columns=['x', 'y']).reset_index()

def plot_stadium_spraychart(
    data: pd.DataFrame, team: str, show_scatter: bool = True, show_kde: bool = True, cmap: str = 'coolwarm', 
    size: int = 10, width: int = 10, height: int = 10, title: Optional[str] = None, color: Optional[str] = "black"
):
    coords = STADIUM_COORDS[STADIUM_COORDS["team"] == team.lower()]
    if coords.empty:
        raise ValueError(f"No stadium data found for team '{team}'")

    fig, ax = plt.subplots(figsize=(width or 10, height or 10))

    segments = coords["segment"].unique()
    for segment in segments:
        seg_data = coords[coords["segment"] == segment]
        if seg_data.empty:
            continue

        color = seg_data["color"].iloc[0] if "color" in seg_data.columns else "grey"

        path = matplotlib.path.Path(seg_data[['x', 'y']].values)
        patch = patches.PathPatch(path, facecolor='None', edgecolor=color, lw=1, zorder=3)
        ax.add_patch(patch)

    sub_data = (data.copy())
    sub_data = sub_data[
        sub_data['hitLocationX'].notna() &
        sub_data['hitLocationY'].notna()
    ]

    sns.scatterplot(data=BASES, x="x", y="y", ax=ax, color="black", s=25, marker="D", zorder=5)

    if show_scatter and not sub_data.empty:
        palette = sns.color_palette("coolwarm")
        sns.scatterplot(data=sub_data, x="hitLocationX", y="hitLocationY", hue="hitSector", palette=palette, ax=ax, s=size, color="navy", zorder=2)
    
    if show_kde:
        sns.kdeplot(data=sub_data, x="hitLocationX", y="hitLocationY", cmap=cmap)

    ax.set_xlim(0, 250)
    ax.set_ylim(0, 250)
    ax.set_aspect('equal')
    ax.grid(True)

    if title:
        ax.set_title(title)

    plt.gca().invert_yaxis()
    plt.show()
    return ax




