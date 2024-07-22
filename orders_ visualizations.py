import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import seaborn as sns

chunksize = 100
orders = pd.read_csv("/Users/xiaye/Downloads/orders.csv", chunksize=chunksize)

for chunk in orders:
    def aggregate_customer_spend(chunk):
        """
        Aggregates customer payment amount by customer_id.

        Args:
        chunk (DataFrame): A chunk of the orders DataFrame.

        Returns:
        DataFrame: Aggregated customer payment amount per customer_id.
        """
        agg_functions = {'customer_payment_amount': 'sum'}
        return chunk.groupby('customer_id').aggregate(agg_functions)

    def count_occurrences(lists):
        """
        Counts occurrences of elements in a list.

        Args:
        lists (list): List of elements to count.

        Returns:
        dict: Dictionary with elements as keys and their counts as values.
        """
        count_dict = {}
        for i in lists:
            if i in count_dict:
                count_dict[i] += 1
            else:
                count_dict[i] = 1
        return count_dict

    def get_coordinates(locations):
        """
        Retrieves coordinates for a list of locations.
        
        Args:
        locations (list): List of location names.

        Returns:
        tuple: Two lists containing latitudes and longitudes.
        """
        loc = Nominatim(user_agent="GetLoc")
        latitudes = []
        longitudes = []
        for location in locations:
            getLoc = loc.geocode(location)
            latitudes.append(getLoc.latitude)
            longitudes.append(getLoc.longitude)
        return latitudes, longitudes

    def calculate_distances(source_coords, destination_coords):
        """
        Calculates distances between pairs of source and destination coordinates.
        
        Args:
        source_coords (list): List of tuples containing source coordinates (latitude, longitude).
        destination_coords (list): List of tuples containing destination coordinates (latitude, longitude).

        Returns:
        list: List of distances in miles.
        """
        distances = []
        for i in range(len(source_coords)):
            distance = geodesic(source_coords[i], destination_coords[i]).miles
            distances.append(distance)
        return distances

    def calculate_cost_per_mile(payment_amounts, weights, distances):
        """
        Calculates cost per mile.

        Args:
        payment_amounts (list): List of customer payment amounts.
        weights (list): List of item weights.
        distances (list): List of distances.

        Returns:
        list: List of cost per mile.
        """
        cost_per_mile = []
        for i in range(len(payment_amounts)):
            cost = payment_amounts[i] / (weights[i] * distances[i])
            cost_per_mile.append(float(cost))
        return cost_per_mile
    
    source_coords = get_coordinates(chunk['source'])
    destination_coords = get_coordinates(chunk['destination'])
    distances = calculate_distances(list(zip(*source_coords)), list(zip(*destination_coords)))
    cost_per_mile = calculate_cost_per_mile(chunk['customer_payment_amount'], chunk['item_weight'], distances)

    def plot_source_destination_distribution(chunk):
        """
        Plots the distribution of source and destination locations.

        Args:
        chunk (DataFrame): A chunk of the orders DataFrame.
        """
        plt.figure(figsize=(10, 6))
        sns.countplot(y='source', data=chunk, order=chunk['source'].value_counts().index)
        plt.title('Count of Orders by Source Location')
        plt.xlabel('Number of Orders')
        plt.ylabel('Source Location')
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.countplot(y='destination', data=chunk, order=chunk['destination'].value_counts().index)
        plt.title('Count of Orders by Destination Location')
        plt.xlabel('Number of Orders')
        plt.ylabel('Destination Location')
        plt.show()

    def plot_customer_payment_amount(chunk):
        """
        Plots a boxplot of customer payment amounts.

        Args:
        chunk (DataFrame): A chunk of the orders DataFrame.
        """
        plt.figure(figsize=(20, 6))
        sns.boxplot(x='customer_payment_amount', data=chunk)
        plt.title('Boxplot of Customer Payment Amounts')
        plt.xlabel('Customer Payment Amount')
        plt.show()

    def print_cost_per_mile(chunk, cost_per_mile):
        """
        Prints the cost per mile for each source and destination pair.

        Args:
        chunk (DataFrame): A chunk of the orders DataFrame.
        cost_per_mile (list): List of cost per mile values.
        """
        printed_items = set()
        for i in range(len(chunk['source'])):
            item = (chunk['source'][i], chunk['destination'][i], cost_per_mile[i])
            if item not in printed_items:
               print(f"source: {item[0]}")
               print(f"destination: {item[1]}")
               print(f"cost_per_mile: {item[2]:.2f}\n")
               printed_items.add(item)
    
    print(aggregate_customer_spend(chunk))
    print("Total number of orders is", len(chunk['source']))
    print("The distribution of source is:", count_occurrences(chunk['source']), sep='\n')
    print("The distribution of destination is:", count_occurrences(chunk['destination']), sep='\n')
    plot_source_destination_distribution(chunk)
    plot_customer_payment_amount(chunk)
    print_cost_per_mile(chunk,cost_per_mile)
