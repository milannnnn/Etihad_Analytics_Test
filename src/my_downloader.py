import urllib.request
import json
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)


class Downloader:

    def __init__(self, wwo_api_key=None):

        self.logger = logging
        self.wwo_api_key = wwo_api_key or '6a8fe4b2abaa419a8fe101143180408'

    # Method for creating WWO download URL string (for given city and date)
    def make_wwo_api_str(self, dt, city):
        # dt   - Datetime object
        # city - City name

        for_str = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=' + self.wwo_api_key + \
                  '&q=' + city + '&format=json&date=' + dt.strftime('%Y-%m-%d')
        return for_str

    # Method for downloading weather data (for given city and date)
    def get_weather_data(self, dt, city):
        # dt   - Datetime object
        # city - City name

        results = {}

        # Try to download and parse data:
        try:
            # Create download URL:
            wwo_url = self.make_wwo_api_str(dt, city)
            # Download data from URL:
            wwo_data = urllib.request.urlopen(wwo_url).read().decode()
            # Parse the downloaded JSON to dictionary:
            wwo_data = json.loads(wwo_data)['data']['weather'][0]

            # Parse min and max daily temperature:
            results['min_temp'] = float(wwo_data['mintempC'])
            results['max_temp'] = float(wwo_data['maxtempC'])
            # Parse daily rainfall (by summing daily precipitation):
            results['rain'] = round(sum([float(k['precipMM']) for k in wwo_data['hourly']]), 1)
            # Parse daily sunlight hours:
            results['sun'] = float(wwo_data['sunHour'])
            # Parse max daily wind speed:
            results['wind'] = max([float(k['windspeedKmph']) for k in wwo_data['hourly']])
            # Parse temperatures at 9AM and 3PM:
            results['temp_9'] = [float(k['tempC']) for k in wwo_data['hourly'] if k['time'] == '900'][0]
            results['temp_3'] = [float(k['tempC']) for k in wwo_data['hourly'] if k['time'] == '1500'][0]
            # Parse rel humidity at 9AM and 3PM:
            results['hum_9'] = [float(k['humidity']) for k in wwo_data['hourly'] if k['time'] == '900'][0]
            results['hum_3'] = [float(k['humidity']) for k in wwo_data['hourly'] if k['time'] == '1500'][0]
            # Parse cloud cover at 9AM and 3PM:
            # results['cloud_9'] = [float(k['cloudcover']) for k in wwo_data['hourly'] if k['time'] == '900'][0]
            # results['cloud_3'] = [float(k['cloudcover']) for k in wwo_data['hourly'] if k['time'] == '1500'][0]

            return results

        # Catch and log any thrown exceptions:
        except Exception:

            msg = 'Error while downloading weather data - please check your connection, API key, city name, date and download limit!\n'

            # msg += 'API:\t'+self.wwo_api_key+'\n'
            # msg += 'City:\t'+city+'\n'
            # msg += 'Date:\t'+dt.strftime('%Y-%m-%d')+'\n'

            # msg += str(Exception)

            logging.error(msg)

            return None

    # Method for downloading weather data with retries
    def get_weather_data_with_retry(self, dt, city, n_retry=3):
        # Try to download data n_retry times
        for _ in range(n_retry):
            results = self.get_weather_data(dt, city)
            # If successfully downloaded - return data
            if results:
                break
            # Else try again

        return results
