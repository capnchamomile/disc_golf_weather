''' disc_golf_weather.py - weather checking script for Lane County, OR and beyond '''

import json
import requests

STATE = 'OR'
OWM_KEY = '' # Sign up for a free API key at http://openweathermap.org/appid
WUG_KEY = '' # Sign up for a free API key at https://www.wunderground.com/weather/api/
GGL_KEY = '' # Sign up for a free API key at https://developers.google.com/maps/documentation/geocoding/start
DSN_KEY = '' # Sign up for a free API key at https://darksky.net/dev/docs

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

print('*' * 40)
print("*      Disc Golf Weather Checker      *")
print('*' * 40)
print("* Support Development: Buy Dan Coffee *")
print('*' * 40)

def main():
    ''' Primary control function '''
    print("\n\nWould you like to check the weather at locations in Lane County, Oregon or enter a US city and state?")
    answer_one = input("\n\n1: Lane County, OR Locations\n\n2: Enter US City and State\n\n")
    while True:
        if answer_one == '1':
            lane_county()
            return False
        elif answer_one == '2':
            cl_state = input('\n\nPlease enter the state\n\n')
            cl_city = input('\n\nPlease enter the city\n\n')
            if len(cl_city) < 3:
                print("That doesn't look right. Let's start over.")
                main()
            elif len(cl_state) < 2:
                print("That doesn't look right. Let's start over.")
                main()
            else:
                city_lookup(cl_city, cl_state)
            return False
        else:
            print("That's not a valid selection. Let's try again.")


def lane_county():
    ''' Checks weather in Lane County '''
    oregon = 'Oregon'
    print("\nAt which website would you like to check the weather in Lane County?\n\n")
    lc_answer_one = input("1: OpenWeatherMap.org -- Short Forecast with High/Low \n\n"
                          "2: Wunderground.com -- Verbose Forecast\n\n"
                          "3: DarkSky.net -- Weekly Summary\n\n")
    if lc_answer_one == '1':
        for place in LOCATIONS:
            get_openweather(place, oregon)
        lc_answer_two = input('Would you like to check areas in Oregon outside of Lane County? y/n\n\n')
        if lc_answer_two.lower() == 'y':
            for extra in EXTRA_LOCATIONS:
                get_openweather(extra, oregon)
        else:
            return False
    elif lc_answer_one == '2':
        for place in LOCATIONS:
            get_wunderground(place, oregon)
        lc_answer_two = input('Would you like to check areas in Oregon outside of Lane County? y/n\n\n')
        if lc_answer_two.lower() == 'y':
            for extra in EXTRA_LOCATIONS:
                get_wunderground(extra, oregon)
        else:
            return False
    elif lc_answer_one == '3':
        for place in LOCATIONS:
            get_darksky(place, oregon)
        lc_answer_two = input('Would you like to check areas in Oregon outside of Lane County? y/n\n\n')
        if lc_answer_two.lower() == 'y':
            for extra in EXTRA_LOCATIONS:
                get_darksky(extra, oregon)
        else:
            return False


def city_lookup(city, state):
    '''  returns weather based on supplied city/state name '''
    print("\nAt which website would you like to check the weather in {city}, {state}?\n\n".format(city=city, state=state))
    cl_answer_one = input("1: OpenWeatherMap.org -- Short Forecast with High/Low \n\n"
                          "2: Wunderground.com -- Verbose Forecast\n\n"
                          "3: DarkSky.net -- Weekly Summary\n\n")
    if cl_answer_one == '1':
        try:
            get_openweather(city, state)
        except:
            KeyError
            print("Did you mispell one of those by chance? Let's start over.")
            main()
    elif cl_answer_one == '2':
        try:
            get_wunderground(city, state)
        except:
            KeyError
            print("Did you mispell one of those by chance? Let's start over.")
            main()
    elif cl_answer_one == '3':
        try:
            get_darksky(city, state)
        except:
            KeyError
            print("Did you mispell one of those by chance? Let's start over.")
            main()
    else:
        print("That's not a valid selection. Let's try again")
        city_lookup(city, state)


def pull_json(url):
    '''JSON helper function'''
    response = requests.get(url)
    response.raise_for_status()
    json_data = json.loads(response.text)
    return json_data


def gmaps_geolocator(city, state):
    '''Provides Latitude/Longitude Coordinates for OpenWeatherMap and DarkSky'''
    url = "https://maps.googleapis.com/maps/api/geocode/json?address={place},+{state}&key={key}".format(place=city, state=state, key=GGL_KEY)

    geometry_data = pull_json(url)

    place_latitude = geometry_data['results'][0]['geometry']['location']['lat']
    place_longitude = geometry_data['results'][0]['geometry']['location']['lng']
    return place_latitude, place_longitude


def get_openweather(city, state):
    '''Pulls OpenWeatherMap data and prints it'''
    lat, lng = gmaps_geolocator(city, state)
    url = 'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lng}&appid={key}&cnt=3&units=imperial'.format(lat=str(lat), lng=str(lng), key=OWM_KEY)

    w_data = pull_json(url)['list']

    todays_high = str(round((w_data[0]['main']['temp_max'])))
    todays_low = str(round((w_data[0]['main']['temp_min'])))
    tomorrows_high = str(round((w_data[1]['main']['temp_max'])))
    tomorrows_low = str(round((w_data[1]['main']['temp_min'])))
    day_after_tomorrows_high = str(round((w_data[2]['main']['temp_max'])))
    day_after_tomorrows_low = str(round((w_data[2]['main']['temp_min'])))

    print('*' * 40)
    print('Today\'s weather in {place}, {state}:'.format(place=city.title(), state=state.title()))
    print(w_data[0]['weather'][0]['main'], '-', w_data[0]['weather'][0]['description'])
    print('High of ' + todays_high + 'F, low of ' + todays_low + 'F\n')
    print('Tomorrow in {place}, {state}:'.format(place=city.title(), state=state.title()))
    print(w_data[1]['weather'][0]['main'], '-', w_data[1]['weather'][0]['description'])
    print('High of ' + tomorrows_high + 'F, low of ' + tomorrows_low + 'F\n')
    print('Day after tomorrow in {place}, {state}:'.format(place=city.title(), state=state.title()))
    print(w_data[2]['weather'][0]['main'], '-', w_data[2]['weather'][0]['description'])
    print('High of ' + day_after_tomorrows_high + 'F, low of ' + day_after_tomorrows_low + 'F')
    print('*' * 40)


def get_wunderground(city, state):
    ''' Pulls Wunderground data and prints it '''
    url = "http://api.wunderground.com/api/{key}/forecast/q/{state}/{city}.json".format(key=WUG_KEY, state=state, city=city)

    w_data = pull_json(url)['forecast']['txt_forecast']['forecastday']

    print('*' * 100)
    print('Today\'s weather in {place}, {state}:'.format(place=city.title(), state=state.title()))
    print(w_data[0]['fcttext'], '\n')
    print('Tomorrow in {place}, {state}:'.format(place=city.title(), state=state.title()))
    print(w_data[1]['fcttext'], '\n')
    print('Tomorrow in {place}, {state}:'.format(place=city.title(), state=state.title()))
    print(w_data[2]['fcttext'])
    print('*' * 100)


def get_darksky(city, state):
    ''' Pulls DarkSky data and prints it '''
    print("Powered by Dark Sky: https://darksky.net/poweredby")
    lat, lng = gmaps_geolocator(city, state)
    url = "https://api.darksky.net/forecast/{key}/{lat},{lng}".format(key=DSN_KEY, lat=str(lat), lng=str(lng))

    w_data = pull_json(url)

    print('*' * 100)

    print('Today\'s weather in {place}, {state}\n'.format(place=city.title(), state=state.title()))
    print(w_data['daily']['summary'])
    print('*' * 100)


if __name__ == "__main__":
    main()
