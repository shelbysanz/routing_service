from datetime import datetime
from Package import Package
from helper import calculate_distance


class Truck:

    max_capacity = 16
    hub_address = "4001 South 700 East"
    avg_mph = 18
    starting_mileage = 0
    starting_location = 0
    starting_distance = 0

    def __init__(self, id, departure_time, driver):
        """
        O(1) - Initializing the truck object
        - id: Integer, Truck identifier
        - packages: List of packages assigned to the truck
        - total_mileage: Integer, total distance traveled by truck
        - route: List of Strings, route taken by truck
        """
        self.id = id
        self.departure_time = datetime.strptime(departure_time, '%H:%M:%S')
        self.mph = Truck.avg_mph
        self.max_capacity = Truck.max_capacity
        self.packages = []
        self.location = Truck.starting_location
        self.total_mileage = Truck.starting_mileage
        self.total_distance = Truck.starting_distance
        self.route = []

    def is_max_capacity(self):
        """
        O(1) - Checks if the truck is at max capacity

        returns boolean if the truck is full or not
        """
    def update_mileage(self, distance_param):
        """
        O(1) - Updates the total mileage of the truck
        """
    def update_route(self, route, distance_param):
        """
        O(1) - Updates the route if the new route is an improvement
        """
    def assign_package(self, package_id):
        """
        O(1) - Assigns package to the truck
        """
    def on_time(self, distances, addresses):
        """
        O(n^2) - Tracks time for the truck and packages.
        Will confirm if the packages will be delivered on time (by their deadline)

        returns boolean if the package will be on time or not
        """
    def execute_route(self, query_time, distances):
        """
        O(n) - Getting the progress of the truck at the time of the query

        returns the miles traveled and the location of the truck once the time of the query is reached
        """
