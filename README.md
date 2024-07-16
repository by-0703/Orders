<h1 align="center">Customer Orders Analysis Script</h3>

<!-- ABOUT THE PROJECT -->
## About The Project
This Python script reads an input CSV file containing order data in batches and performs various analyses including aggregating spending per customer, calculating cost per mile for deliveries, and understanding customer distribution based on sources and destinations.

<!-- DEPENDENCIES -->
## Dependencies
To run this script, the following Python libraries are required:
* `pandas`
* `geopy`

Install these dependencies in terminal by using following codes：

```sh
   python -m pip install pandas
   ```
```sh
   python -m pip install geopy
   ```

<!-- DESCRIPTION -->
## Description
The script performs the following tasks:
* Aggregates customer spending: Sums up the payment amounts for each customer.
* Counts occurrences: Counts the number of occurrences of each source and destination to understand customer distribution.
* Retrieves coordinates: Uses the Nominatim API to get latitude and longitude for source and destination locations.
* Calculates distances: Computes distances between source and destination coordinates using the geodesic function from the geopy library.
* Calculates cost per mile: Determines the cost per mile for each delivery

<!-- USAGE -->
## Usage
**1. Input CSV File**

   Input CSV file named orders.csv with the following columns:
* order_id: Unique identifier for each order.
* source: The source location.
* destination: The destination location.
* customer_id: Unique identifier for each customer.
* customer_payment_amount: The amount spent by the customer. 
* item_weight: The weight of the item being shipped.

**2. Script Execution**

   The script can be executed by running the following code in your terminal:
```sh
   python script_location.py
   ```

<!-- EXAMPLES FOR USAGE -->
## Examples for Usage
**1. Input CSV Files**

![image](https://github.com/user-attachments/assets/e8ce5b07-c3f6-40a9-b898-e7b5375dacab)

**2. Script Execution**

![image](https://github.com/user-attachments/assets/ae85fbca-5389-49cd-9f2f-85e00626b65c)

**3. Output**

![image](https://github.com/user-attachments/assets/244fead6-352f-433f-82df-624f4709ce0e)

<!-- Parameters -->
## Parameters

* `chunksize`: The size of the batch to read from the CSV file at a time (default is set to 100).
* `chunk`: A chunk of the orders DataFrame.
* `lists`: List of elements to count.
* `locations`: List of location names.
* `source_coords`: List of tuples containing source coordinates (latitude, longitude).
* `destination_coords`: List of tuples containing destination coordinates (latitude, longitude).
* `payment_amounts`: List of customer payment amounts.
* `weights`: List of item weights.
* `distances`: List of distances.
