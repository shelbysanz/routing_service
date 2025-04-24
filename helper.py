from Truck import Truck
from Package import Package
from PackageHt import PackageHt
from datetime import datetime
from math import inf
import csv

EOD = datetime.datetime.strptime("16:59:59", '%H:%M:%S')
package_hashTable = PackageHt()


def dispatch():
    """
    O(n^2) - Dispatch controller
    - Loads trucks
    - Implements 3-opt algorithm
    - Finds routes and distances
    - Ensures packages are on time
    """

    # import data using csv readers
    loads = load_package_csv()
    distances = load_distance_csv()
    locations = list(load_locations_csv())

    # create 3 truck objects
    trucks = [
        Truck(1, '08:00:00', 1),
        Truck(2, '09:06:00', 2),
        Truck(3, '10:21:00', 1)
    ]

    trucks = load_trucks()

    for truck in trucks:
        for parcel in truck.packages:
            parcel.dispatch_time = truck.departure_time
            if parcel.id == 9:
                # updates wrong address
                parcel = update_wrong_address(parcel)

    final_distances = [inf, inf, inf]
    final_route = [[], [], []]

    for _ in range(100):
        for i, truck in enumerate(truck.trucks):
            final_route[i] = three_opt_algorithm(truck, distances, locations)
            final_distances[i] = truck.update_route(
                truck, final_route[i], final_distances[i], distances)

    # make sure packages arrive by deadline or swap until they will
    for i in range(len(truck.trucks)):
        for j in range(i + 1, len(truck.trucks)):
            truck1 = truck.trucks[i]
            truck2 = truck.trucks[j]

            if not truck1.on_time(distances, locations) or not truck2.on_time(distances, locations):
                swap_packages(truck1, truck2, distances, locations)


    # loads trucks
def load_trucks(loads, trucks):
    """
    Loads the trucks from the load list
    """

    # assign packages to trucks
    for i, truck in enumerate(loads):
        for package_id in loads[i + 1]:
            package = package_hashTable.lookup(package_id)
            truck.assign_package(package)
            package.assign_truck(truck)

    return trucks


    # updates address that was wrong
def load_package_csv():
    """
    O(1) - Load the packages csv

    returns: list of packages
    """
    eod = datetime.datetime.strptime("16:59:59", '%H:%M:%S')

    # initialize package hash table

    # read csv
        # creates packages
            # create package object
    # insert them into the hashtable
    # append them to the package list
    # return the package list
def sort_package_load_list(package_list):
    """
    O(n) - Sort the packages into truck load lists based on:
    - Special notes
    - Deadlines
    - Locations

    returns: list of loads, filled with package_ids for each truck
    """
    # first sort by deadline
    # use match case to organize by special notes
    """
    make sure to remove the package from the list when it's assigned
        'on truck' - for special truck
        'Wrong address' - address will be updated later
        'delivered with' - add related package ids
        'Delayed' - find hub arrival and sort based on truck departure
    """
    # get list of addresses and zip codes for packages in each load list as locales
    # add early deadline packages to load list if address or zip code matches an existing locale
    # add early deadline packages w/ no matching locales

    # add remaining packages to any load under capacity with a matching address
    # add remaining packages to any load under capacity with a matching zip
    # add remianing packages to the load with the least # of packages
    # raise and error if all loads are at max capacity
def update_wrong_address(package):
    """
    O(1) - Fixes address for a package
    - Specific case - Simulation for package.id == 9
    """
def update_ending_location(truck, route, start_location):
    """
    O(1) - Updates special case, setting starting location for first truck
    """
def three_opt_algorithm(truck, distances, locations):
    """
    O(n^3) - Get the original truck route, remove, swap, 3 locations on the route continuously
    - Goal: Finding the shortest overall distance
    - Minimizing paths on the route that cross over others
    """
    # O(n^2) - Map package addresses to location indices
    # O(1) - Remove duplicate locations
    # O(1) - Randomize the route
    # O(n^3) - Iterate through route assigning 3 variables to adjacent locations
    """
        O(1) - Create new route after swapping variables
        O(1) - Calculate hub to first location distance
        O(1) - Calculate distance of route
        O(1) - Update best_route if it is shorter
    """
    # return best_route
def calculate_distance(route, distances):
    """
    O(n) - Calculates distance between all locations in a route
    """

    # Get two locations to get distance at a time
def verify_route(truck, route, distance, distance_list):
    """
    Makes sure that the route is the best one before updating it

    returns the smaller distance
    """
