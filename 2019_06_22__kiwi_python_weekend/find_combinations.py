import sys
import json
from datetime import datetime, timedelta

import pandas as pd 

sys.stderr = open('error_file', 'w')

try:
    df = pd.read_csv(sys.stdin)

    flights = df.values.tolist()

    flights = [
        {
            'flights': [flight],
            'route':[flight[0], flight[1]], 
            'schedule': flight[2:4], 
            'flight_numbers':[flight[4]], 
            'total_price': flight[5], 
            'max_bags_allowed': flight[6], 
            'total_per_bag_price': flight[7], 
            'can_be_extended': True
        } for flight in flights
    ]

    for flight in (flight for flight in flights if flight['can_be_extended']):
        for next_flight in flights:
            if (next_flight['route'][0] == flight['route'][-1] and (timedelta(hours=1) <= (datetime.strptime(next_flight['schedule'][0], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(flight['schedule'][-1], '%Y-%m-%dT%H:%M:%S'))<= timedelta(hours=4))):
                new_route =  {
                    'flights': [flight['flights']] + [next_flight['flights']],
                    'route':flight['route'] + [next_flight['route'][1]], 
                    'schedule': flight['schedule'] + next_flight['schedule'], 
                    'flight_numbers':flight['flight_numbers'] + next_flight['flight_numbers'], 
                    'total_price': flight['total_price'] + next_flight['total_price'], 
                    'max_bags_allowed': min(flight['max_bags_allowed'], next_flight['max_bags_allowed']),
                    'total_per_bag_price': flight['total_per_bag_price'] + next_flight['total_per_bag_price'], 
                    'can_be_extended': True,
                }

                if new_route['route'][0] == new_route['route'][-1]:
                    new_route['can_be_extended'] = False
                
                flights += [new_route]
        flight['can_be_extended'] == False

    output = []

    for flight in flights:
        if 'final_price' not in flight:
            for i in range (flight['max_bags_allowed'] + 1):
                print (i)
                flight['bags_selected'] = i
                flight['final_price'] = flight['total_price'] + flight['total_per_bag_price'] * i
                output += [{**flight}]
                print (flight)

    json.dump( output, open( "output.json", 'w' ) )

    for flight in output:
        sys.stdout.write(
            'Route: ' + ','.join(flight['route']) + ' | Amount of bags: ' + str(flight['bags_selected'])+
            ' | Price: ' + str(flight['final_price']) + ' | Departure time: ' + str(flight['schedule'][0]) + '\n'
            )
except Exception as e:
    sys.stderr.write(e +     "\n")