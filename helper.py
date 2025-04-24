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


def load_package_csv():
    """
    O(1) - Load the packages csv

    returns: list of packages
    """
    # package_list, will be used to sort packages
    package_list = []

    # read csv
    with (open('packages.csv') as package_file):
        reader = csv.reader(package_file, delimeter=',')
        next(reader)  # skips first line (header)

        # creates packages
        for row in reader:
            package_id = int(row[0])
            address = {
                "address": row[1],
                "city": row[2],
                "state": row[3],
                "zip": row[4],
            }
            deadline = datetime.strptime(
                row[5], '%H:%M %p') if row[5][0].isnumeric() else EOD
            weight = row[6]
            notes = row[7]
            truck = None

            # create package object
            new_package = Package(package_id, address,
                                  deadline, weight, notes, truck)
            # insert into the package hash table
            package_hashTable.insert(package_id, new_package)
            # append them to the package list
            package_list.append(new_package)
            package_list = sort_package_load_list(package_list)
    # return the package list
    return package_list


def sort_package_load_list(package_list):
    """
    O(n) - Sort the packages into truck load lists based on:
    - Special notes
    - Deadlines
    - Locations

    returns: list of loads, filled with packages for each truck
    """
    group_set = set()
    package_list.sort(key=lambda package: package.deadline)
    original_list = package_list.copy()
    loads = {1: [], 2: [], 3: []}
    loaded_packages = []

    # sorts packages by sorting criteria in the notes
    for package in package_list:
        if package.notes:
            note = package.notes

            # if must be from a specific truck
            if 'on truck' in note:
                truck = int(note.split()[-1])
                loads[truck].append(package.package_id)
                loaded_packages.append(package)
                continue

            # if must be delivered later due to wrong address
            if 'Wrong address' in note:
                loads[3].append(package.package_id)
                loaded_packages.append(package)
                continue

            # if needs to be delivered along with another package (same truck)
            if 'delivered with' in note:
                group = list(
                    map(int, note[note.find('with') + 5:].split(', ')))
                group_set.add(package.package_id)
                loaded_packages.append(package)
                if package.package_id not in loads[1]:
                    loads[1].append(package.package_id)
                    for item in group:
                        group_set.add(item)
                        for copy_pkg in original_list:
                            if copy_pkg.package_id == item and copy_pkg.package_id not in loads[1]:
                                loads[1].append(copy_pkg.package_id)
                                loaded_packages.append(copy_pkg)

            # if the package is delayed and must be delivered later
            if 'Delayed' in note:
                time_str = next(word for word in note.split()
                                if word[0].isdigit())
                delay_time = datetime.datetime.strptime(
                    time_str, '%H:%M').time()
                if delay_time.hour < 9:
                    loads[1].append(package.package_id)
                elif delay_time.hour < 10 or (delay_time.hour == 10 and delay_time.minute < 20):
                    loads[2].append(package.package_id)
                else:
                    loads[3].append(package.package_id)
                loaded_packages.append(package)
                continue

    # remove loaded packages from list
    loaded_ids = set(id for truck in loads.values() for id in truck)
    package_list = [
        pkg for pkg in package_list if pkg.package_id not in loaded_ids]
    original_list = package_list.copy()

    # gather locations for each truck
    truck_locales = {1: set(), 2: set(), 3: set()}
    for truck_num, truck_load in loads.items():
        for pkg in loaded_packages:
            if pkg.package_id in truck_load:
                truck_locales[truck_num].add(pkg.address["address"])
                truck_locales[truck_num].add(pkg.address["zip"])

    # assign based on location deadline
    for pkg in package_list.copy():
        if pkg.deadline != EOD:
            for truck_num in (1, 2, 3):
                if (pkg.address["address"] in truck_locales[truck_num] or
                        pkg.address["zip"] in truck_locales[truck_num]) and len(loads[truck_num]) < 16:
                    loads[truck_num].append(pkg.package_id)
                    loaded_packages.append(pkg)
                    package_list.remove(pkg)
                    break

    for pkg in package_list.copy():
        if pkg.deadline != EOD:
            loads[1].append(pkg.package_id)
            loaded_packages.append(pkg)
            package_list.remove(pkg)

    original_list = package_list.copy()

    # match by address
    for truck_num, truck_load in loads.items():
        for loaded_pkg in loaded_packages:
            if loaded_pkg.package_id in truck_load:
                for pkg in original_list.copy():
                    if pkg.address["address"] == loaded_pkg.address["address"] and len(truck_load) < 16:
                        truck_load.append(pkg.package_id)
                        package_list.remove(pkg)

    original_list = package_list.copy()

    # match by zip
    for truck_num, truck_load in loads.items():
        for loaded_pkg in loaded_packages:
            if loaded_pkg.package_id in truck_load:
                for pkg in original_list.copy():
                    if pkg.address["zip"] == loaded_pkg.address["zip"] and len(truck_load) < 16:
                        truck_load.append(pkg.package_id)
                        package_list.remove(pkg)

    # load remaining packages
    for pkg in package_list.copy():
        truck_sizes = {k: len(v) for k, v in loads.items()}
        for truck_num in sorted(truck_sizes, key=lambda x: (truck_sizes[x], x)):
            if len(loads[truck_num]) < Truck.max_capacity:
                loads[truck_num].append(pkg.package_id)
                package_list.remove(pkg)
                break
        else:
            raise IndexError('Trucks are at max capacity')

    return loads


def update_wrong_address(package):
    """
    O(1) - Fixes address for a package
    - Specific case - Simulation for package.id == 9
    """
    package.address["address"] = '410 S State St'
    package.address["city"] = 'Salt Lake City'
    package.address["state"] = 'UT'
    package.address["zip"] = '84111'

    return package


def update_ending_location(truck, route, start_location):
    """
    O(1) - Updates special case, setting starting location for first truck
    """
    if truck.id == 1:
        route.append(start_location)
    return route


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

    distance = 0

    # Get two locations to get distance at a time
    for i in range(len(route) - 1):
        loc1 = route[i]
        loc2 = route[i + 1]

        if distances[loc1][loc2]:
            distance += distances[loc1][loc2]
        else:
            distance += distances[loc2][loc1]

    return distance


def verify_route(truck, route, distance, distance_list):
    """
    Makes sure that the route is the best one before updating it

    returns the smaller distance
    """
