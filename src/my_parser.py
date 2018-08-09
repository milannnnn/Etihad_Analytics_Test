import pandas as pd
import numpy as np

from src.my_downloader import Downloader


class Parser:

    # # # Method for class initialization:
    def __init__(self, cities=None, latitudes=None, excel_file=None):
        self.cities = cities or ['Melbourne', 'Sydney', 'Adelaide', 'Brisbane', 'Perth']
        self.latitudes = latitudes or [-37.8136, -33.8688, -34.9285, -27.4698, -31.9505]
        self.excel_file = excel_file or 'data/Meteorological Data.xlsx'
        self.downloader = Downloader()

    # # # Method for parse meteorological data (loading, filling and processing)
    def parse_data(self, save=True):

        dfs = {}

        # For each city:
        for k, city in enumerate(self.cities):

            # Load the corresponding Excel sheet into Pandas DF:
            df = self.load_excel_sheet(k, self.excel_file)

            # Fill all missing values (download from WWO database):
            df = self.fill_df(df, city)

            # Calculate dew points at 9am and 3pm:
            df = df.assign(dew_9=self.calc_dew(df.hum_9, df.temp_9))
            df = df.assign(dew_3=self.calc_dew(df.hum_3, df.temp_3))

            # Calculate daily sunlight percentage:
            df = df.assign(sun_perc=self.calc_sun_perc(df.index.dayofyear, df.sun, self.latitudes[k]))

            # Add the created DF (for given city) to dictionary:
            dfs[city] = df

        # Save parsed data to new Excel file (optionally)
        if save:
            self.save_parsed_dfs(dfs)

        return dfs

    # # # Method for saving parsed DFs to Excel file
    @staticmethod
    def save_parsed_dfs(dfs, file_path='data/updated_meteo_data.xlsx'):
        # Initialize Excel writer:
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        # Include all cities to the writer:
        for city in dfs:
            dfs[city].to_excel(writer, sheet_name=city)
        # Saved to provided file path:
        writer.save()

    # # # Method for loading parsed DFs from Excel file
    @staticmethod
    def load_parsed_dfs(file_path='data/updated_meteo_data.xlsx'):
        dfs = pd.read_excel(file_path, sheet_name=None, index_col='Date')
        return dict(dfs)

    # # # Method for loading provided Excel data into Pandas DataFrame
    @staticmethod
    def load_excel_sheet(sheet_no, file_path):
        # sheet_no - number of the sheet to be read

        # Read-in DataFrame from excel sheet:
        df = pd.read_excel(file_path, sheet_name=sheet_no)

        # Parse dates to datetime objects:
        df.Date = pd.to_datetime(df.Date, dayfirst=True)
        df = df.set_index('Date')

        # Select relevant columns:
        df = df[['Minimum temperature (°C)', 'Maximum temperature (°C)', 'Rainfall (mm)', 'Sunshine (hours)',
                 'Speed of maximum wind gust (km/h)', '9am Temperature (°C)', '9am relative humidity (%)',
                 '3pm Temperature (°C)', '3pm relative humidity (%)']]

        # Rename columns:
        df.columns = ['min_temp', 'max_temp', 'rain', 'sun', 'wind', 'temp_9', 'hum_9', 'temp_3', 'hum_3']

        return df

    # # # Method for filling missing meteorological values
    def fill_df(self, df, city):
        # df   - original DataFrame
        # city - city name

        # For each row (day) in DataFrame:
        for k in range(len(df)):

            # Check for missing data:
            if df.iloc[k].isnull().sum() > 0:

                dt = df.index[k]

                # Download missing data from WWO (with WeatherDataDownloader class):
                results = self.downloader.get_weather_data_with_retry(dt, city)

                # If data successfully downloaded:
                if results:
                    # Fill all missing values with new data:
                    for col in df.columns:
                        if np.isnan(df.loc[dt, col]):
                            df.loc[dt, col] = results[col]
        return df

    # # # Function for calculating meteorological dew point:
    @staticmethod
    def calc_dew(RH, T):
        # The calculation is based on dew point equations presented on
        # https://en.wikipedia.org/wiki/Dew_point#Calculating_the_dew_point
        #
        # RH - relative humidity vector [ % ]
        # T  - air temperature vector   [* C]

        # Dew point calculation constants:
        b = 18.678
        c = 257.14
        d = 234.5

        # Gamma parameter calculation:
        g_m = np.log(RH / 100 * np.exp((b - T / d) * (T / (c + T))))

        # Dew point calculation:
        dew = (c * g_m / (b - g_m)).round(1)

        return dew

    # # # Function for calculating daily sunlight percentage
    @staticmethod
    def calc_sun_perc(day_of_year, sun_hour, geo_lat):
        # The calculation is based on sunrise equations presented on
        # https://en.wikipedia.org/wiki/Sunrise_equation
        #
        # day_of_year - day of the year vector      [ / ]
        # sun_hour    - daily sunlight hours vector [ h ]
        # geo_lat     - geographical latitude       [deg]

        # Calculate solar declination:
        dec = -23.45 * np.pi / 180 * np.cos(2 * np.pi * (day_of_year + 10) / 365)

        # Calculate daylight length:
        day_len = np.arccos(-np.tan(geo_lat * np.pi / 180) * np.tan(dec)) * 24 / np.pi

        # Normalize sunlit hours with daylight length to get sunlight percentage:
        sun_perc = (sun_hour / day_len * 100).round(1).clip(lower=0, upper=100)

        return sun_perc

