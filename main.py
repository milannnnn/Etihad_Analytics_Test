# Import required libraries:
from src.my_parser import Parser
from src.my_analyzer import Analyzer
from src.my_plotter import Plotter
import os.path

# Initialize class instances:
parser = Parser()
analyzer = Analyzer()
plotter = Plotter(fig_size=(10, 5))

# Parse the data:

# If already parsed - just load the saved data:
if os.path.exists('data/updated_meteo_data.xlsx'):
    # This method loads previously parsed data
    dfs = parser.load_parsed_dfs()
# If not - parse the data and save to file:
else:
    # This method reads original data, fills missing values,
    # performs required processing and saves obtained data
    dfs = parser.parse_data(save=True)

# Perform comfort level analysis and save counts to file:

# This method computes parameter-specific comfort indicators,
# then uses them to calculate daily comfort levels,
# and performs a daily comfort count over all cities
count = analyzer.calc_day_counts(dfs)
print(count.head())

# Plot required graphs:

# These methods output required violin graphs
plotter.plot_temp_graph(dfs)
plotter.plot_humidity_graph(dfs)
plotter.plot_sunlight_graph(dfs)
plotter.plot_wind_graph(dfs)
plotter.plot_rain_graph(dfs)
