'''disc_golf_weather.py - Gets weather at Disc Golf courses in the Lane County, Oregon area'''

import json
import requests

OWM_KEY = '' # Sign up for a free API key at http://openweathermap.org/appid
WUG_KEY = '' # Sign up for a free API key at https://www.wunderground.com/weather/api/

# Locations with city codes for openweathermap.org. Wunderground doesn't require city codes.

LOCATIONS = {'Eugene' : '5725846', \
            'Dexter': '5735869', \
            'Noti': '5758566', \
            'Cottage Grove': '5720755'}

EXTRA_LOCATIONS = {'Roseburg': '5749352', \
                   'Corvallis': '5720727', \
                   'Lebanon': '5736218', \
                   'Estacada': '5725801', \
                   'Portland': '5746545', \
                   'Grants Pass': '5729080'}

def main():
    print()
    print()
    print("*" * 40)
    print("* Disc Golf Weather in Lane County, OR *")
    print("*" * 40)
    print("* Support Development: Buy Dan Coffee  *")
    print("*" * 40)
    while True:
        print("\nAt which website would you like to check the weather?\n\n")
        answer_one = input("1: OpenWeatherMap.org -- Short Forecast with High/Low \n\n2: Wunderground.com -- Verbose Forecast\n\n")
        if answer_one == '1':
            get_openweather(LOCATIONS)
            answer_two = input('Would you like to check areas outside of Lane County? Y/n\n\n')
            if answer_two.lower() == "y":
                get_openweather(EXTRA_LOCATIONS)
                print("\nRemember: Slow is smooth and smooth is far.\n")
                return False
            else:
                print("\nCrush some drives!\n")
                return False
        elif answer_one == '2':
            get_wunderground(LOCATIONS)
            answer_two = input('Would you like to check areas outside of Lane County? Y/n\n\n')
            if answer_two.lower() == "y":
                get_wunderground(EXTRA_LOCATIONS)
                print("\nGo bang them chains!\n")
                return False
            else:
                print("\nYeah I wouldn't want to drive out there either. Have fun huckin'!\n")
                return False
        else:
            print("That's not a valid selection. Let's try again.")

def get_openweather(location):
    for place, city_code in location.items():
        url = 'http://api.openweathermap.org/data/2.5/forecast?id={id}&appid={key}&cnt=3&units=imperial'.format(id=city_code, key=OWM_KEY)

        response = requests.get(url)
        response.raise_for_status()
        weather_data = json.loads(response.text)

        w = weather_data['list']

        todays_high = str(round((w[0]['main']['temp_max'])))
        todays_low = str(round((w[0]['main']['temp_min'])))
        tomorrows_high = str(round((w[1]['main']['temp_max'])))
        tomorrows_low = str(round((w[1]['main']['temp_min'])))
        day_after_tomorrows_high = str(round((w[2]['main']['temp_max'])))
        day_after_tomorrows_low = str(round((w[2]['main']['temp_min'])))

        print('*' * 40)
        print('Today\'s weather in {place}:'.format(place=place))
        print(w[0]['weather'][0]['main'], '-', w[0]['weather'][0]['description'])
        print('High of ' + todays_high + 'F, low of ' + todays_low + 'F')
        print()
        print('Tomorrow in {place}:'.format(place=place))
        print(w[1]['weather'][0]['main'], '-', w[1]['weather'][0]['description'])
        print('High of ' + tomorrows_high + 'F, low of ' + tomorrows_low + 'F')
        print()
        print('Day after tomorrow in {place}:'.format(place=place))
        print(w[2]['weather'][0]['main'], '-', w[2]['weather'][0]['description'])
        print('High of ' + day_after_tomorrows_high + 'F, low of ' + day_after_tomorrows_low + 'F')
        print('*' * 40)

def get_wunderground(location):
    for place, city_code in location.items():
        url = "http://api.wunderground.com/api/{key}/forecast/q/OR/{city}.json".format(key=WUG_KEY, city=place)
        
        response = requests.get(url)
        response.raise_for_status()
        weather_data = json.loads(response.text)

        w = weather_data['forecast']['txt_forecast']['forecastday']

        print('*' * 140)
        print('Today\'s weather in {place}:'.format(place=place))
        print(w[0]['fcttext'])
        print()
        print('Tomorrow in {place}:'.format(place=place))
        print(w[1]['fcttext'])
        print()
        print('Tomorrow in {place}:'.format(place=place))
        print(w[2]['fcttext'])
        print('*' * 140)

if __name__ == "__main__":
    main()
