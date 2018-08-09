# Import required libraries:
from src.my_parser import Parser
from src.my_analyzer import Analyzer
from src.my_plotter import Plotter
import os.path

# Initialize class instances:
parser = Parser()
analyzer = Analyzer()
plotter = Plotter(fig_size=(10, 5))

# Parse the data (read, fill and process):
# If previously parsed, just load the data:
if os.path.exists('updated_meteo_data.xlsx'):
    dfs = parser.load_parsed_dfs()
# Else parse the data from scratch:
else:
    dfs = parser.parse_data()

# Perform comfort level analysis and save counts to file:
count = analyzer.calc_day_counts(dfs)
print(count.head())

# Plot required graphs:
plotter.plot_temp_graph(dfs)
plotter.plot_humidity_graph(dfs)
plotter.plot_sunlight_graph(dfs)
plotter.plot_wind_graph(dfs)
plotter.plot_rain_graph(dfs)
