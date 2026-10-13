import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import math


def calculate_dist(org,dest):
    lat_per_degree = 69
    lon_per_degree = 54.6
    org_lat,org_lon = org
    dest_lat,dest_lon = dest
    return math.sqrt((lat_per_degree * (org_lat - dest_lat)) ** 2 + (lon_per_degree * (org_lon - dest_lon)) ** 2)

def search_price(number,type):
    price_data = {'self-driving': {'price_per_mile': 0.3, 'speed': 60, 'efficiency': 1},
                    'taxi': {'price_per_mile': 0.3, 'speed': 60, 'efficiency': 1.5},
                    'flight': {'price_per_mile': 1.3, 'speed': 600, 'efficiency': 10}}
    
    return price_data[type]['price_per_mile'] * number


def get_all_costs(json_list):
    total_cost = 0
    transportation_cost = 0
    breakfast_cost = 0
    lunch_cost = 0
    dinner_cost = 0
    attraction_cost = 0
    accommodation_cost = 0
    for unit in json_list:
        if 'transportation' in unit and unit['transportation'] and unit['transportation'] != '-':
            if 'flight number' in unit['transportation'] and 'self-driving' not in unit['transportation'].lower() and 'taxi' not in unit['transportation'].lower():
                org = unit['current_city']
                dest = unit['transportation'].split(' to ')[1].split(',')[0]
                if 'price' in unit and unit['price']:
                    transportation_cost += unit['price']
                else:
                    transportation_cost += 500
            else:
                org = unit['current_city']
                if 'self-driving' in unit['transportation'].lower():
                    dest = unit['transportation'].split(' to ')[1].split(',')[0]
                    # dest = unit['destination']
                    # org_lat,org_lon = search_cities(org)[0],search_cities(org)[1]
                    # dest_lat,dest_lon = search_cities(dest)[0],search_cities(dest)[1]
                    # dist = calculate_dist([org_lat,org_lon],[dest_lat,dest_lon])
                    # transportation_cost += search_price(dist,'self-driving')
                    transportation_cost += 0

                elif 'taxi' in unit['transportation'].lower():
                    if 'from' not in unit['transportation'].lower():
                        taxi_cost = 8
                    else:
                        org = unit['transportation'].split(' from ')[1].split(' to ')[0]
                        dest = unit['transportation'].split(' from ')[1].split(' to ')[1]
                        
                        # org_lat,org_lon = search_lat_lon(org)
                        # dest_lat,dest_lon = search_lat_lon(dest)
                        
                        # dist = calculate_dist([org_lat,org_lon],[dest_lat,dest_lon])
                        # taxi_cost = search_price(dist,'taxi')
                        taxi_cost = 8
                    transportation_cost += taxi_cost
        if 'breakfast' in unit and unit['breakfast'] and unit['breakfast'] != '-':
            if 'cost' in unit['breakfast']:
                breakfast_cost += eval(unit['breakfast'].split('cost: ')[1].split(')')[0])
        if 'lunch' in unit and unit['lunch'] and unit['lunch'] != '-':
            if 'cost' in unit['lunch']:
                lunch_cost += eval(unit['lunch'].split('cost: ')[1].split(')')[0])
        if 'dinner' in unit and unit['dinner'] and unit['dinner'] != '-':
            if 'cost' in unit['dinner']:
                dinner_cost += eval(unit['dinner'].split('cost: ')[1].split(')')[0])
        if 'attraction' in unit and unit['attraction'] and unit['attraction'] != '-':
            if 'cost' in unit['attraction']:
                try:
                    attraction_cost += eval(unit['attraction'].split('cost: ')[1].split(')')[0])
                except:
                    attraction_cost += 0
        if 'accommodation' in unit and unit['accommodation'] and unit['accommodation'] != '-':
            if 'cost' in unit['accommodation']:
                accommodation_cost += eval(unit['accommodation'].split('cost: ')[1].split(')')[0].replace('per night','').strip())
    total_cost = transportation_cost + breakfast_cost + lunch_cost + dinner_cost + attraction_cost + accommodation_cost
    return total_cost