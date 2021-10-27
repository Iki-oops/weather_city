import os
import datetime as dt
import requests


class Weather:
    def __init__(self, days):
        self.days = days

    def get_max_daylight(self):
        daily = self.days.get('daily')
        result = (dt.timedelta(days=0), dt.datetime.today())
        for day in daily[:5]:
            from_ts = dt.datetime.fromtimestamp
            difference = from_ts(day.get('sunset')) - from_ts(day.get('sunrise'))
            if difference > result[0]:
                result = (difference, from_ts(day.get('dt')))
        return f'Максимальная продолжительность светового дня - {result[0]}.\n' \
               f'День - {result[1].date()}'

    def get_min_difference(self):
        daily = self.days.get('daily')
        result = (float('inf'), dt.datetime.today())
        for obj in daily:
            difference = abs(
                obj.get('feels_like').get('night') - obj.get('temp').get('night')
            )
            if difference < result[0]:
                result = (
                    difference,
                    dt.datetime.fromtimestamp(obj.get('dt'))
                )
        return f'Минимальная разница между фактической температурой и ' \
               f'"ощущаемой" - {result[0]}.\nДень - {result[1].date()}'


if __name__ == '__main__':
    lat, lon = 51.8261, 107.6098  # Координаты г.Улан-Удэ
    API_KEY = os.environ.get('API_KEY')
    URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&' \
          f'lon={lon}&exclude=current,minutely,alerts&appid={API_KEY}'
    weather = requests.get(URL).json()
    a = Weather(weather)
    print(a.get_min_difference())
