# 1. Please complete the following:
#   Your First name and Last Name: Anjali Ravi
#   Your Student ID: 261159848
import math
import random

MIN_LAT = -90
MAX_LAT = 90
MIN_LONG = -180
MAX_LONG = 180
EARTH_RADIUS = 6371

def meter_to_feet(meters):
    '''
    (num) -> num
    Takes a measure in meters and returns the measure converted to feet, rounded to 2 decimals
    >>> meter_to_feet(100)
    328.0
    >>> meter_to_feet(4)
    13.12
    >>> meter_to_feet(10.3)
    33.78
    
    '''
    feet = meters * 3.28
    return round(feet, 2)


def degrees_to_radians(degrees):
    '''
    (num) -> num
    Converts an angle in degrees to radians, rounded to 2 decimals
    >>> degrees_to_radians(1)
    0.02
    >>> degrees_to_radians(90)
    1.57
    >>> degrees_to_radians(15)
    0.26
    '''
    radians = degrees * math.pi / 180
    return round(radians, 2)
    
def get_vessel_dimensions():
    '''
    () -> (num, num)
    Asks user for vessel length and width in meters and returns the dimensions in feet
    >>> get_vessel_dimensions()
    Enter the vessel length (in meter): 10
    Enter the vessel width (in meter): 6
    (32.8, 19.68)
    >>> get_vessel_dimensions()
    Enter the vessel length (in meter): 4
    Enter the vessel width (in meter): 10.3
    (13.12, 33.78)
    >>> get_vessel_dimensions()
    Enter the vessel length (in meter): 35
    Enter the vessel width (in meter): 21
    (114.8, 68.88)
    '''
    
    length_meters = float(input('Enter the vessel length (in meter):'))
    width_meters = float(input('Enter the vessel width (in meter):'))
    length_feet = meter_to_feet(length_meters)
    width_feet = meter_to_feet(width_meters)
    return length_feet, width_feet
    
def get_valid_coordinate(val_name, min_float, max_float):
    '''
    (str, float, float) -> float
    Takes a variable name and min/max value.
    Asks user for a value for the variable until variable is within range, then returns that value
    >>> get_valid_coordinate('latitude', -90, 90)
    What is your latitude? -100
    Invalid latitude
    What is your latitude? -87.6
    -87.6
    >>> get_valid_coordinate('x-coordinate', 0, 20)
    What is your x-coordinate? -5
    Invalid x-coordinate
    What is your x-coordinate? 30
    Invalid x-coordinate
    What is your x-coordinate? 15
    15
    >>> get_valid_coordinate('latitude', -25, 25)
    What is your latitude? 4 
    4
    '''
    name = float(input('What is your ' + val_name + ' ?'))
    while name < min_float or name > max_float:
        print('Invalid', val_name)
        name = float(input('What is your ' + val_name + ' ?'))
    
    return name

def get_gps_location():
    '''
    () -> (num, num)
    Calls previous function to get latitude and longitude and returns the corresponding coordinate
    >>> get_gps_location()
    What is your latitude? 45.51
    What is your longitude? -73.56
    (45.51, -73.56)
    >>> get_gps_location()
    What is your latitude? -100
    Invalid latitude
    What is your latitude? 10.2
    What is your longitude? 35.41
    (10.2, 35.41)
    >>> get_gps_location()
    What is your latitude? -23.21
    What is your longitude? 141
    Invalid longitude
    What is your longitude? 41
    (-23.21, 41)
    '''
    latitude = get_valid_coordinate('latitude', MIN_LAT, MAX_LAT)
    longitude = get_valid_coordinate('longitude', MIN_LONG, MAX_LONG)
    return latitude, longitude

def distance_two_points(lat_1, long_1, lat_2, long_2):
    '''
    (num, num, num, num) -> num
    Takes the latitude and longitude of two locations and returns the
    distance between the locations
    >>> distance_two_points(45.508888, -73.561668, 19.432608, -99.133209)
    3719.22
    >>> distance_two_points(50, 22, 39, -14)
    3034.71
    >>> distance_two_points(-44, 17, 56, -32)
    12064.17
    
    '''
    lat_1 = degrees_to_radians(lat_1)
    long_1 = degrees_to_radians(long_1)
    lat_2 = degrees_to_radians(lat_2)
    long_2 = degrees_to_radians(long_2)
    
    if lat_1 >= lat_2:
        lat_diff = lat_1 - lat_2
    else:
        lat_diff = lat_2 - lat_1
    
    if long_1 >= long_2:
        long_diff = long_1 - long_2
    else:
        long_diff = long_2 - long_1
        
    a = pow(math.sin(lat_diff / 2), 2) + math.cos(lat_1) * math.cos(lat_2) * pow(math.sin(long_diff / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = round(EARTH_RADIUS * c, 2)
    
    return distance

def check_safety(lat, long):
    '''
    (num, num) -> None
    Checks if vessel is with 400km of a restricted zone, in a hazardous zone,
    or safe and prints corresponding message
    >>> check_safety(21.804132, -72.305832)
    Error: Restricted zone!
    >>> check_safety(40.7, -70.3)
    Warning: Hazardous area! Navigate with caution.
    >>> check_safety(30, -62.34)
    Safe navigation.
    '''
    if distance_two_points(lat, long, 25, -71) <= 400:
        print('Error: Restricted zone!')
    elif 40 <= lat <= 41 and -71 <= long <= -70:
        print('Warning: Hazardous area! Navigate with caution.')
    else:
        print('Safe navigation.')

def get_max_capacity(length, width):
    '''
    (num, num) -> int
    Returns vessel's capacity based on its dimensions
    >>> get_max_capacity(27, 8)
    17
    >>> get_max_capacity(2, 4)
    0
    >>> get_max_capacity(10, 13)
    8
    '''
    if length <= 26:
        capacity = length * width / 15
    else:
        capacity = (length * width / 15) + (length - 26) * 3
    
    return int(capacity)

def passengers_on_boat(length, width, passengers):
    '''
    (num, num, num) -> num
    Checks if we can fit all the passengers we want to on the boat or not
    >>> passengers_on_boat(20, 6, 8)
    True
    >>> passengers_on_boat(12, 5, 5)
    False
    >>> passengers_on_boat(34, 11, 44)
    True
    '''
    capacity = get_max_capacity(length, width)
    
    if passengers <= capacity and passengers % 4 == 0:
        return True
    else:
        return False

def update_coordinate(position, min_float, max_float):
    '''
    (num, num, num) -> num
    Generates random number between -10 and 10, and if that number added to the position
    is between min and max float, returns new position. If not in range, continues
    to generate numbers until a valid position is generated
    >>> update_coordinate(44, -90, 90)
    46.49
    >>> update_coordinate(44, -90, 90)
    39.95
    >>> update_coordinate(44, -90, 90)
    48.72
    '''
    random.seed(123)
    x = 20 * random.random() - 10
    while position + x <= min_float or position + x >= max_float:
        x = 20 * random.random() - 10
        
    return round(position + x, 2)
    
def wave_hit_vessel(lat, long):
    '''
    (num, num, num) -> (num, num)
    uses update_coordinate function to get new latitude and longitude, prints
    the safety of the new location, and returns new coordinates
    >>> wave_hit_vessel(25, 32)
    Safe navigation.
    (16.05, 23.05)
    >>> wave_hit_vessel(40, 19)
    Safe navigation.
    (31.05, 10.05)
    >>> wave_hit_vessel(-18, -4)
    Safe navigation.
    (-26.95, -12.95)
    '''
    new_lat = update_coordinate(lat, MIN_LAT, MAX_LAT)
    new_long = update_coordinate(long, MIN_LONG, MAX_LONG)
    check_safety(new_lat, new_long)
    return new_lat, new_long

def vessel_menu():
    print('Welcome to the boat menu!')
    
    latitude = get_valid_coordinate('latitude', MIN_LAT, MAX_LAT)
    longitude = get_valid_coordinate('longitude', MIN_LONG, MAX_LONG)
    
    print('Your current position is at latitude', latitude, 'and longitude', longitude)
    
    length, width = get_vessel_dimensions()
    
    print('Your boat measures', length, 'feet by', width, 'feet')
    
    print('Please select an option below: ')
    print('1. Check the safety of your boat')
    print('2. Check the maximum number of people that can fit on the boat')
    print('3. Update the position of your boat')
    print('4. Exit boat menu')
    
    selection = int(input('Your selection:'))
    
    while selection != 4:
        if selection == 1:
            check_safety(latitude, longitude)
            print('Please select an option below: ')
            print('1. Check the safety of your boat')
            print('2. Check the maximum number of people that can fit on the boat')
            print('3. Update the position of your boat')
            print('4. Exit boat menu')
            selection = int(input('Your selection:'))
        
        elif selection == 2:
            passengers = int(input('How many adults go on the boat?'))
            if passengers_on_boat(length, width, passengers) == True:
                print('Your boat can hold', passengers, 'adults')
            else:
                print('Your boat cannot hold', passengers, 'adults')
            print('Please select an option below: ')
            print('1. Check the safety of your boat')
            print('2. Check the maximum number of people that can fit on the boat')
            print('3. Update the position of your boat')
            print('4. Exit boat menu')
            selection = int(input('Your selection:'))
        
        else:
            latitude, longitude = wave_hit_vessel(latitude, longitude)
            print('Your new position is latitude of', latitude, 'and longitude of', longitude)
            print('Please select an option below: ')
            print('1. Check the safety of your boat')
            print('2. Check the maximum number of people that can fit on the boat')
            print('3. Update the position of your boat')
            print('4. Exit boat menu')
            selection = int(input('Your selection:'))
    
    print('End of boat menu.')







