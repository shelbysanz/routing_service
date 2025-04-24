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
        self.departure_time = datetime.datetime.strptime(
            departure_time, '%H:%M:%S')
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

    def on_time(self, distances, addresses, truck3):
        """
        O(n^2) - Tracks time for the truck and packages.
        Will confirm if the packages will be delivered on time (by their deadline)

        returns boolean if the package will be on time or not
        """

        current_time = self.departure_time
        self.miles_traveled = 0
        self.location = 0

        # iterates throught truck route
        for i in range(len(self.route) - 1):
            current_location = self.route[i]
            next_location = self.route[i + 1]
            self.location = next_location

            # increments miles traveled and arrival time at each location
            travel_distance = self.calculate_distance(
                (current_location, next_location), distances)
            self.miles_traveled += travel_distance
            time_to_location = travel_distance / self.mph
            current_time += datetime.timedelta(hours=time_to_location)

            # sets the departure time
            if self.id == 1 and self.location == 0 and current_time > truck3.departure_time:
                truck3.departure_time = current_time

            # updates package delivery times
            for parcel in self.packages:
                if addresses.index(parcel.address['address']) == next_location:
                    parcel.delivery_time = current_time

        return all(parcel.delivery_time <= parcel.deadline for parcel in self.packages)

    def execute_route(self, custom_time, distances):
        """
        O(n) - Gets the current location (or previous one if between) and miles traveled at a specific time.

        returns location and miles
        """
        current_time = self.departure_time
        location = self.route[0] if self.route else 0
        miles = 0

        for current_location, next_location in zip(self.route, self.route[1:]):
            distance = self.calculate_distance(
                (current_location, next_location), distances)
            travel_time = datetime.timedelta(hours=distance / self.mph)

            # converts custom_time to datetime so it can compare properly
            if not isinstance(custom_time, datetime.datetime):
                custom_time = datetime.datetime.combine(
                    current_time.date(), custom_time)

            if current_time + travel_time > custom_time:
                # this means truck is in between two locations (en route)
                # Time difference in hours
                time_diff = (custom_time - current_time).total_seconds() / 3600
                partial_distance = self.mph * time_diff
                miles += partial_distance
                return current_location, miles

            current_time += travel_time
            miles += distance
            location = next_location

        return location, miles
