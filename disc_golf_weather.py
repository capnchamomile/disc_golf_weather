'''disc_golf_weather.py - Gets weather at Disc Golf courses in the Lane County, Oregon area'''

import json
import requests

STATE = 'OR'
OWM_KEY = '' # Sign up for a free API key at http://openweathermap.org/appid
WUG_KEY = '' # Sign up for a free API key at https://www.wunderground.com/weather/api/
GGL_KEY = '' # Sign up for a free API key at https://developers.google.com/maps/documentation/geocoding/start
DSN_KEY = '' # Sign up for a free API key at https://darksky.net/dev/docs

# Locations with city codes for openweathermap.org. Wunderground and DarkSky doesn't require city codes.

LOCATIONS = ['Eugene', \
            'Dexter', \
            'Noti', \
            'Cottage Grove']

EXTRA_LOCATIONS = ['Roseburg', \
                   'Corvallis', \
                   'Lebanon', \
                   'Estacada', \
                   'Portland', \
                   'Grants Pass']

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
        answer_one = input("1: OpenWeatherMap.org -- Short Forecast with High/Low \n\n2: Wunderground.com -- Verbose Forecast\n\n3: DarkSky.net -- Weekly Summary\n\n")
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
        elif answer_one == '3':
            get_darksky(LOCATIONS)
            answer_two = input('Would you like to check areas outside of Lane County? Y/n\n\n')
            if answer_two.lower() == "y":
                get_darksky(EXTRA_LOCATIONS)
                print("\nSick.\n")
                return False
            else:
                print("\nNo judgment here. Have a huckin' good time!\n")
                return False
        else:
            print("That's not a valid selection. Let's try again.")

def pull_json(url):
    response = requests.get(url)
    response.raise_for_status()
    json_data = json.loads(response.text)
    return json_data

def gmaps_geolocator(location):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address={place},+{state}&key={key}".format(place=location, state=STATE, key=GGL_KEY)

    geometry_data = pull_json(url)

    place_latitude = geometry_data['results'][0]['geometry']['location']['lat']
    place_longitude = geometry_data['results'][0]['geometry']['location']['lng']
    return place_latitude, place_longitude

def get_openweather(location):
    for place in location:
        lat, lng = gmaps_geolocator(place)
        url = 'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lng}&appid={key}&cnt=3&units=imperial'.format(lat=str(lat), lng=str(lng), key=OWM_KEY)

        w = pull_json(url)['list']

        todays_high = str(round((w[0]['main']['temp_max'])))
        todays_low = str(round((w[0]['main']['temp_min'])))
        tomorrows_high = str(round((w[1]['main']['temp_max'])))
        tomorrows_low = str(round((w[1]['main']['temp_min'])))
        day_after_tomorrows_high = str(round((w[2]['main']['temp_max'])))
        day_after_tomorrows_low = str(round((w[2]['main']['temp_min'])))

        print('*' * 40)
        print('Today\'s weather in {place}:'.format(place=place))
        print(w[0]['weather'][0]['main'], '-', w[0]['weather'][0]['description'])
        print('High of ' + todays_high + 'F, low of ' + todays_low + 'F\n')
        print('Tomorrow in {place}:'.format(place=place))
        print(w[1]['weather'][0]['main'], '-', w[1]['weather'][0]['description'])
        print('High of ' + tomorrows_high + 'F, low of ' + tomorrows_low + 'F\n')
        print('Day after tomorrow in {place}:'.format(place=place))
        print(w[2]['weather'][0]['main'], '-', w[2]['weather'][0]['description'])
        print('High of ' + day_after_tomorrows_high + 'F, low of ' + day_after_tomorrows_low + 'F')
        print('*' * 40)

def get_wunderground(location):
    for place in location:
        url = "http://api.wunderground.com/api/{key}/forecast/q/{state}/{city}.json".format(key=WUG_KEY, state=STATE, city=place)

        w = pull_json(url)['forecast']['txt_forecast']['forecastday']

        print('*' * 100)
        print('Today\'s weather in {place}:'.format(place=place))
        print(w[0]['fcttext'], '\n')
        print('Tomorrow in {place}:'.format(place=place))
        print(w[1]['fcttext'], '\n')
        print('Tomorrow in {place}:'.format(place=place))
        print(w[2]['fcttext'])
        print('*' * 100)

def get_darksky(location):
    print("Powered by Dark Sky: https://darksky.net/poweredby")
    for place in location:
        lat, lng = gmaps_geolocator(place)
        url = "https://api.darksky.net/forecast/{key}/{lat},{lng}".format(key=DSN_KEY, lat=str(lat), lng=str(lng))

        w = pull_json(url)

        print('*' * 100)
        print('Today\'s weather in {place}\n'.format(place=place))
        print(w['daily']['summary'])
        print('*' * 100)

if __name__ == "__main__":
    main()
