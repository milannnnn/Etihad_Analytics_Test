import pandas as pd


class Analyzer:
    # Method for initializing decision tree rules:
    def __init__(self):
        # Temperature limits (minimum, maximum, swing and mean temperatures):
        self.temp_1 = {'min': 15, 'max': 30, 'delta': 12.5, 'mean': [20, 25]}
        self.temp_2 = {'min': 10, 'max': 32.5, 'delta': 17.5, 'mean': [17.5, 27.5]}
        # Dew point limits (minimum and maximum points):
        self.dew_1 = {'min': 10, 'max': 18}
        self.dew_2 = {'min': 0, 'max': 21}
        # Sunlight percentage limits (daily sunlight percentage):
        self.sun_1 = {'min': 75}
        self.sun_2 = {'min': 50}
        # Daily rainfall limits (net daily rainfall):
        self.rain_1 = {'max': 0.25}  # 1h of very light rain (drizzle) per day
        self.rain_2 = {'max': 1.00}  # 1h of light rain per day
        # Maximum wind speed limits (from Beaufort scale):
        self.wind_1 = {'max': 28}  # Moderate breeze
        self.wind_2 = {'max': 38}  # Fresh breeze

    # # # Method for saving daily weather indicators
    def calc_day_counts(self, dfs, save=True):
        d = {}
        for city in dfs:
            y = self.apply_criterion(dfs[city]).value_counts()
            d[city] = [y[2] if 2 in y.index else 0, y[1] if 1 in y.index else 0, y[0] if 0 in y.index else 0]
        df = pd.DataFrame(data=d).rename(index={0: 'Great Day', 1: 'Good Day', 2: 'Bad Day'})
        if save:
            df.to_excel('data/day_counts.xlsx')
        return df

    # # # Method for counting daily weather indicators
    def print_day_counts(self, dfs):
        for city in dfs:
            print('#', city + ':')
            y = self.apply_criterion(dfs[city]).value_counts()
            print('Great:', y[2] if 2 in y.index else '/')
            print('Good :', y[1] if 1 in y.index else '/')
            print('Bad  :', y[0] if 0 in y.index else '/', '\n')

    # # # Method for computing all daily weather indicators
    def apply_criterion(self, df):
        data = {}

        # Computing day type indicators
        data['temp'] = self.temp_criterion(df)
        data['dew'] = self.dew_criterion(df)
        data['sun'] = self.sun_criterion(df)
        data['rain'] = self.rain_criterion(df)
        data['wind'] = self.wind_criterion(df)

        crit = pd.DataFrame(data=data)

        x = ((crit.sum(axis=1) > (3 * 2 + 2 * 1)) & ((crit == 0).sum(axis=1) == 0)) * 1
        x += ((crit.sum(axis=1) > (4 * 1)) & ((crit == 0).sum(axis=1) <= 1)) * 1

        return x

    # # # Method for computing daily temperature indicators
    def temp_criterion(self, df):
        # Great day limits:
        min_1 = self.temp_1['min']
        max_1 = self.temp_1['max']
        del_1 = self.temp_1['delta']
        mean_1 = self.temp_1['mean']
        # Good day limits:
        min_2 = self.temp_2['min']
        max_2 = self.temp_2['max']
        del_2 = self.temp_2['delta']
        mean_2 = self.temp_2['mean']

        t_mean = df[['min_temp', 'max_temp', 'temp_3', 'temp_9']].mean(axis=1)

        # Compute great day indicators:
        x = ((df.min_temp >= min_1) & (df.max_temp <= max_1) & (df.max_temp - df.min_temp <= del_1) &
             (t_mean >= mean_1[0]) & (t_mean <= mean_1[1])) * 1
        # Compute good day indicators (and add to great day):
        x += ((df.min_temp >= min_2) & (df.max_temp <= max_2) & (df.max_temp - df.min_temp <= del_2) &
              (t_mean >= mean_2[0]) & (t_mean <= mean_2[1])) * 1

        return x

    # # # Method for computing daily dew point indicators
    def dew_criterion(self, df):
        # Great day limits:
        min_1 = self.dew_1['min']
        max_1 = self.dew_1['max']
        # Good day limits:
        min_2 = self.dew_2['min']
        max_2 = self.dew_2['max']

        # Finding min and max dew points:
        dew_min = df[['dew_3', 'dew_9']].min(axis=1)
        dew_max = df[['dew_3', 'dew_9']].max(axis=1)

        # Compute great day indicators:
        x = ((dew_min >= min_1) & (dew_max <= max_1)) * 1
        # Compute good day indicators (and add to great day):
        x += ((dew_min >= min_2) & (dew_max <= max_2)) * 1

        return x

    # # # Method for computing daily sunlight indicators
    def sun_criterion(self, df):
        # Great day limits:
        min_1 = self.sun_1['min']
        # Good day limits:
        min_2 = self.sun_2['min']

        # Compute great day indicators:
        x = (df.sun_perc >= min_1) * 1
        # Compute good day indicators (and add to great day):
        x += (df.sun_perc >= min_2) * 1

        return x

    # # # Method for computing daily rainfall indicators
    def rain_criterion(self, df):
        # Great day limits:
        max_1 = self.rain_1['max']
        # Good day limits:
        max_2 = self.rain_2['max']

        # Compute great day indicators:
        x = (df.rain <= max_1) * 1
        # Compute good day indicators (and add to great day):
        x += (df.rain <= max_2) * 1

        return x

    # # # Method for computing daily wind gust indicators
    def wind_criterion(self, df):
        # Great day limits:
        max_1 = self.wind_1['max']
        # Good day limits:
        max_2 = self.wind_2['max']

        # Compute great day indicators:
        x = (df.wind <= max_1) * 1
        # Compute good day indicators (and add to great day):
        x += (df.wind <= max_2) * 1

        return x
