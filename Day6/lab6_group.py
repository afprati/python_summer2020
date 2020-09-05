# TODO: write code to answer the following questions: 
# 1) which of these embassies is closest to the White House in meters? 
# how far is it, and what is the address?
# 2) if I wanted to hold a morning meeting there, which cafe would you suggest?
# 3) if I wanted to hold an evening meeting there, which bar would you suggest? 

import sys
import re
import importlib
sys.path.insert(0, 'C:/Users/jenna/Documents/GitHub/python_summer2020/Day6')
imported_items = importlib.import_module('start_google')
gmaps = imported_items.client


whitehouse = '1600 Pennsylvania Avenue, Washington, DC'

embassies = [[38.917228,-77.0522365], 
	[38.9076502, -77.0370427], 
	[38.916944, -77.048739] ]

###################################################################################
# 1) which of these embassies is closest to the White House in meters? 
###################################################################################
whitehouse_geocode = gmaps.geocode(whitehouse)
whitehouse_loc2 = whitehouse_geocode[0]['geometry']['location']
whitehouse_loc2

# Find the distance (in km) between White House and Emb
distance = gmaps.distance_matrix(whitehouse_loc2, embassies)
distance1 = distance['rows'][0]['elements'][0]['distance']['text']
distance2 = distance['rows'][0]['elements'][1]['distance']['text']
distance3 = distance['rows'][0]['elements'][2]['distance']['text']
type(distance2)
print(distance2)


# Print all address info for closest embassy
destination = gmaps.reverse_geocode(embassies[1])
# Name address and ensure it's a string for later
address = str(destination[0]["formatted_address"])

# Convert to meters    
distance2 = re.sub(" km", "", distance2)
dist_meters = float(distance2) * 1000
print(dist_meters)

###################################################################################
### 2) if I wanted to hold a morning meeting there, which cafe would you suggest? #
###################################################################################
dir(whitehouse_geocode)
gmaps.places(whitehouse)

# to use places_nearby, rank by distance with lat/long and keyword of location
test = gmaps.places_nearby(embassies[2], keyword = 'cafe', rank_by = "distance")
print(test)

# To use places, simply enter str address and 'location near'
local = gmaps.places('cafe near' + address)
print(local)
print(local['results'][0]['name'])

###################################################################################
### 3) If I wanted to hold an evening meeting there, which bar would you suggest? #
###################################################################################
local2 = gmaps.places('bar near' + address)
print(local2)
print(local2['results'][0]['name'])

# with 'places_nearby'
bar_test = gmaps.places_nearby(embassies[2], keyword = 'bar', rank_by = "distance")
print(bar_test['results'][0]['name'])














