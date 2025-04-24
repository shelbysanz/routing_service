import datetime
from math import inf


class Truck:

    max_capacity = 16
    hub_address = "4001 South 700 East"
    avg_mph = 18
    starting_mileage = 0
    starting_location = 0
    starting_distance = inf

    def __init__(self, id, departure_time, driver):
        """
        O(1) - Initializing the truck object
        - id: Integer, Truck identifier
        - packages: List of packages assigned to the truck
        - total_mileage: Integer, total distance traveled by truck
        - route: List of Strings, route taken by truck
        """
        self.id = id
        self.departure_time = datetime.datetime.strptime(departure_time, '%H:%M:%S')
        self.driver = driver
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
        if len(self.packages) == Truck.max_capacity:
            return True
        return False

    def update_mileage(self, distance_param):
        """
        O(1) - Updates the total mileage of the truck
        """
        self.total_mileage += distance_param

    def update_route(self, route, distance):
        """
        O(1) - Updates the route if the new route is an improvement
        """
        if distance < self.total_distance:
            self.route = route
            self.total_distance = distance

    def assign_package(self, package):
        """
        O(1) - Assigns package to the truck
        """
        if not self.is_max_capacity():
            self.packages.append(package)

    def unassign_package(self, package):
        """
        O(1) - Removes package from the truck
        """
        self.packages.remove(package)

    def calculate_distance(self, route, distances):
        """
        O(n) - Calculates distance between all locations in a route
        """

        distance = 0

        for i in range(len(route) - 1):
            loc1 = route[i]
            loc2 = route[i + 1]

            if distances[loc1][loc2]:
                distance += distances[loc1][loc2]
            else:
                distance += distances[loc2][loc1]

        return distance

    def on_time(self, distances, addresses):
        """
        O(n^2) - Tracks time for the truck and packages.
        Will confirm if the packages will be delivered on time (by their deadline)

        returns boolean if the package will be on time or not
        """

        current_time = self.departure_time
        self.total_mileage = 0
        self.location = 0

    def execute_route(self, query_time, distances):
        """
        O(n) - Getting the progress of the truck at the time of the query

        returns the miles traveled and the location of the truck once the time of the query is reached
        """

        current_time = self.departure_time
        location = 0
        miles = 0

        for i in range(len(self.route) - 1):
            if current_time.time() < query_time:
                location = self.route[i]
                next_location = self.route[i + 1]

                distance_traveled = self.calculate_distance(
                    (location, next_location), distances)
                location = next_location
                miles += distance_traveled
                time_to_location = distance_traveled / self.mph
                current_time += datetime.timedelta(hours=time_to_location)
            else:
                return location, miles
        return location, miles
