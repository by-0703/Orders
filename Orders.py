import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

chunksize = 100
orders = pd.read_csv('orders.csv', chunksize=chunksize)
print(orders)

for chunk in orders:
    agg_functions = { 'customer_payment_amount': 'sum', }
    aggspendpercustomer = chunk.groupby(chunk['customer_id']).aggregate(agg_functions)

    lists = chunk['source']
    count_source = dict()
    for i in lists:
        if i in count_source:
            count_source[i] += 1
        else:
            count_source[i] = 1
    
    listd = chunk['destination']
    total = len(listd)
    count_destination = dict()
    for i in listd:
        if i in count_destination:
            count_destination[i] += 1
        else:
            count_destination[i] = 1

    totalorder = len(lists)

    loc = Nominatim(user_agent="GetLoc")
    sourcelatitudes = []
    sourcelongitudes = []
    for location in lists:
        getLoc = loc.geocode(location)
        sourcelatitudes.append(getLoc.latitude)
        sourcelongitudes.append(getLoc.longitude)
    
    destinationlatitudes = []
    destinationlongitudes = []
    for location in listd:
        getLoc = loc.geocode(location)
        destinationlatitudes.append(getLoc.latitude)
        destinationlongitudes.append(getLoc.longitude)
    
    distances = []
    for i in range(len(sourcelatitudes)):
        source_coords = (sourcelatitudes[i], sourcelongitudes[i])
        destination_coords = (destinationlatitudes[i], destinationlongitudes[i])
        distance = geodesic(source_coords, destination_coords).miles
        distances.append(distance)
    
    listw = chunk['item_weight']
    listm = chunk['customer_payment_amount']
    costpermiles = []
    for x in range(len(listm)):
        cost = listm[x] / (listw[x] * distances[x])
        costpermiles.append(float(cost))
    



print(aggspendpercustomer)
print("Total number of orders is",totalorder)
print("The distribution of source is:",count_source,sep='\n')
print("The distribution of destination is:",count_destination,sep='\n')
#print(sourcelatitudes)
#print(sourcelongitudes)
#print(destinationlatitudes)
#print(destinationlongitudes)
#print(distances)

setprint = set()
for i in range(len(lists)):
    item = (lists[i], listd[i], costpermiles[i])
    if item not in setprint:
        print(f"source: {item[0]}")
        print(f"destination: {item[1]}")
        print(f"cost_per_miles: {item[2]:.2f}\n")
        setprint.add(item)


    