import pandas as pd
from pathlib import Path
import warnings
from get_mlb_spraychart import *
warnings.filterwarnings("ignore")

path = Path("MLB_HIT_DATA")
years = [2024]
files = [pd.read_csv(path/f"MLB_HIT_DATA_{year}.csv") for year in years]
data = pd.concat(files)

data = data[data["eventtype"] == "home_run"]

plot_stadium_spraychart(data, "rockies")

