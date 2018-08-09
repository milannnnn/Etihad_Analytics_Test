import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


class Plotter:
    def __init__(self, fig_size=None):
        self.fig_size = fig_size or (25, 10)
        self.palette = 'Set3'

    # Method for plotting temperature violin graph
    def plot_temp_graph(self, dfs):
        # dfs - dictionary mapping cities to corresponding DataFrames

        # Merge relevant data to single DataFrame (for violin plot)
        dfs_temp = []
        for city in dfs:
            df_min = pd.DataFrame(dfs[city].min_temp).rename(columns={'min_temp': 'Temperature [*C]'})
            df_min['Measurement'] = 'Min Temp'
            df_max = pd.DataFrame(dfs[city].max_temp).rename(columns={'max_temp': 'Temperature [*C]'})
            df_max['Measurement'] = 'Max Temp'
            df = pd.concat([df_min, df_max])
            df['City'] = city
            dfs_temp += [df]
        df = pd.concat(dfs_temp)

        plt.figure(figsize=self.fig_size)
        sns.set_style("whitegrid")
        sns.violinplot(x="City", y="Temperature [*C]", hue="Measurement", data=df, palette=self.palette,
                       split=True, scale="count", inner="quartile", cut=0)
        plt.show()

    # Method for plotting humidity violin graph
    def plot_humidity_graph(self, dfs):
        # dfs - dictionary mapping cities to corresponding DataFrames

        # Merge relevant data to single DataFrame (for violin plot)
        dfs_hum = []
        for city in dfs:
            df_max = pd.DataFrame(dfs[city].dew_9).rename(columns={'dew_9': 'Dew Point [*C]'})
            df_max['Measurement'] = 'Dew Point at 9 am'
            df_min = pd.DataFrame(dfs[city].dew_3).rename(columns={'dew_3': 'Dew Point [*C]'})
            df_min['Measurement'] = 'Dew Point at 3 pm'
            df = pd.concat([df_min, df_max])
            df['City'] = city
            dfs_hum += [df]
        df = pd.concat(dfs_hum)

        plt.figure(figsize=self.fig_size)
        sns.set_style("whitegrid")
        sns.violinplot(x="City", y="Dew Point [*C]", hue="Measurement", data=df, palette=self.palette,
                       split=True, scale="count", inner="quartile", cut=0)
        plt.show()

    # Method for plotting sunlight violin graph
    def plot_sunlight_graph(self, dfs):
        # dfs - dictionary mapping cities to corresponding DataFrames

        # Merge relevant data to single DataFrame (for violin plot)
        dfs_sun = []
        for city in dfs:
            df = pd.DataFrame(dfs[city].sun_perc).rename(columns={'sun_perc': 'Sunlight Percentage [%]'})
            df['City'] = city
            dfs_sun += [df]
        df = pd.concat(dfs_sun)

        plt.figure(figsize=self.fig_size)
        sns.set_style("whitegrid")
        sns.violinplot(x='City', y='Sunlight Percentage [%]', data=df, palette=self.palette,
                       scale='count', inner='quartile', cut=0)
        # plt.ylim((0, 100))
        plt.show()

    # Method for plotting wind speed violin graph
    def plot_wind_graph(self, dfs):
        # dfs - dictionary mapping cities to corresponding DataFrames

        # Merge relevant data to single DataFrame (for violin plot)
        dfs_wind = []
        for city in dfs:
            df = pd.DataFrame(dfs[city].wind).rename(columns={'wind': 'Maximum Wind Speed [km/h]'})
            df['City'] = city
            dfs_wind += [df]
        df = pd.concat(dfs_wind)

        plt.figure(figsize=self.fig_size)
        sns.set_style("whitegrid")
        sns.violinplot(x='City', y='Maximum Wind Speed [km/h]', data=df, palette=self.palette,
                       scale='count', inner='quartile', cut=0)
        plt.show()

    # Method for plotting rainfall violin graph
    def plot_rain_graph(self, dfs):
        # dfs - dictionary mapping cities to corresponding DataFrames

        # Merge relevant data to single DataFrame (for violin plot)
        dfs_rain = []
        for city in dfs:
            df = pd.DataFrame(dfs[city].rain).rename(columns={'rain': 'Daily Precipitation [mm/m^2]'})
            df['City'] = city
            dfs_rain += [df]
        df = pd.concat(dfs_rain)

        plt.figure(figsize=self.fig_size)
        sns.set_style("whitegrid")
        sns.violinplot(x='City', y='Daily Precipitation [mm/m^2]', data=df, palette=self.palette,
                       scale='count', inner='quartile', cut=0)
        plt.show()


