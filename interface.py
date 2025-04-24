import datetime
import sys
from helper import load_distance_csv, load_locations_csv, update_ending_location


def interface_main(package_hashTable, trucks):
    """
    O(1) - Interface of the initial menu for the routing service
    """

    # will loop until user exits program, or enters valid option
    while True:
        show_main_menu()
        time_input = input("Enter option: ").strip()

        if time_input == '1':
            current_time_menu(package_hashTable, trucks)
            break
        elif time_input == '2':
            custom_time_menu(package_hashTable, trucks)
            break
        elif time_input == '3':
            print('\nGoodbye!\n')
            sys.exit()
        else:
            print('\nPlease enter a valid option and press enter.\n')


def show_main_menu():
    print()
    print("""
----------- WGU Routing Postal Service -----------

Choose an option:

1: Get Real Time Information
2: Get Information For A Specific Time
3: Exit The Program
""".strip())


def current_time_menu(package_hashTable, trucks):
    """
    O(1) - Shows options to get data from the current time
    """

    # gets the current time
    time_now = datetime.datetime.now().time()

    # shows menu for getting reports for the current time
    while True:
        print(
            f"\n\n\nThe current time is {time_now.strftime('%I:%M %p')}\n\n"
            '1 - Report of All Packages\n'
            '2 - Look Up a Specific Package\n'
            '3 - See All Trucks Summary\n'
            '4 - Exit the Program\n\n'
        )

        menu_input = input('Enter option: ')
        if menu_input == '1':
            print(print_all_packages(time_now, package_hashTable, trucks))
        elif menu_input == '2':
            package_lookup(time_now, package_hashTable, trucks)
        elif menu_input == '3':
            truck_stats(time_now, package_hashTable, trucks)
        elif menu_input == '4':
            print('\n\nGoodbye!\n')
            sys.exit()
        else:
            print(
                '\n\nPlease enter a valid option and press enter.\n\n')


def custom_time_menu(package_hashTable, trucks):
    """
    O(1) - Allows user to pick a custom time, and get reports
    """

    custom_time = (
        input('\n\n\n\nEnter the Custom Time (HH:MM am/pm): '))
    try:
        custom_time = datetime.datetime.strptime(
            custom_time, '%I:%M %p').time()
    except ValueError:
        print(
            '\n\nPlease enter a valid time. Use 12-hour format, followed by a space and \'am\' or \'pm\'.\n\n')
        custom_time_menu(package_hashTable, trucks)

    while True:

        print(f"You entered {custom_time.strftime('%I:%M %p')}.\n\n"

              'Report Options:\n'

              '1 - Report of All Packages\n'
              '2 - Look Up a Specific Package\n'
              '3 - See All Trucks Summary\n'
              '4 - Exit the Program\n\n'
              )

        menu_input = input('Enter option: ')
        if menu_input == '1':
            print(print_all_packages(custom_time, package_hashTable, trucks))
        elif menu_input == '2':
            package_lookup(custom_time, package_hashTable, trucks)
        elif menu_input == '3':
            truck_stats(custom_time, package_hashTable, trucks)
        elif menu_input == '4':
            print('\n\nGoodbye!\n')
            sys.exit()
        else:
            print(
                '\n\nPlease enter a valid option and press enter.\n\n')


def print_package_report_header(custom_time):
    line = '-' * 83
    time_str = custom_time.strftime('%I:%M %p')

    print(f"{line:^155}")
    print(f"{'All Packages':^151}")
    print(f"{f'Time Chosen: {time_str}':^151}")
    print(f"{line:^155}")
    print('\n' * 2)


def print_all_packages(custom_time, package_hashTable, trucks):
    """
    Prints all the packages and their information along with status and delivery details
    """

    # updates status according to the custom time chosen
    package_hashTable.update_all_statuses(custom_time)

    # assignin headers for viewing it in columns
    id_header = 'ID'
    address_header = 'DELIVERY ADDRESS'
    deadline_header = 'DEADLINE'
    notes_header = 'NOTES'
    status_header = 'STATUS'
    truck_header = 'TRUCK'
    delivery_header = 'DELIVERY DETAILS'

    # prints the report header
    print_package_report_header(custom_time)

    print('  %-15s %-35s %-22s %-36s %-15s %-12s %-15s\n' % (id_header, address_header, deadline_header,
                                                             notes_header, status_header, truck_header,
                                                             delivery_header))

    # parses the package hash table using the look up function and populates the package data
    for i in range(1, 41):
        current_package = package_hashTable.lookup(i)
        package_id = current_package.id
        address = current_package.address["address"][:26]
        deadline = current_package.deadline.time().strftime('%I:%M %p')
        notes = current_package.notes
        status = current_package.status
        truck = current_package.truck
        delivery_time = current_package.delivery_time.time()
        delivery_details = ''
        if custom_time < delivery_time:
            delivery_details = f"{delivery_time.strftime('%I:%M %p')}"
        elif custom_time >= delivery_time:
            delivery_details = f"{delivery_time.strftime('%I:%M %p')}"

        if not isinstance(truck, int):
            truck = truck.id
        print('  %-15s %-35s %-22s %-36s %-15s %-12s %15s' % (package_id, address, deadline, notes.split('-')[0],
                                                              status, truck, delivery_details))

    print('\n')

    # can return to the main menu or exit the program
    next_input = input(
        '\nEnter 0 to return to the main menu.\nEnter any other key to exit.\n')
    if next_input == '0':
        interface_main(package_hashTable, trucks)
    else:
        print('\n\n\n\nGoodbye!\n\n\n')
        sys.exit()


def print_package_lookup_header(custom_time):
    divider = '-' * 58
    time_str = custom_time.strftime('%I:%M %p')

    print(f"""
    {divider}
                         PACKAGE QUERY
                      Query Time: {time_str}
    {divider}
    """)


def package_lookup(custom_time, package_hashTable, trucks):
    """
    Show the details of a packae at a certain point in time
    """

    # update the package statuses
    package_hashTable.update_all_statuses(custom_time)

    # get users package id to look up
    p_query = int(input('Enter a Package ID number: '))
    if p_query not in range(1, len(package_hashTable.table) + 1):
        print('\n\nPlease enter a valid Package ID number and press enter.\n\n')
        package_lookup(custom_time, package_hashTable, trucks)
    else:
        pass

    parcel = package_hashTable.lookup(p_query)

    # print the report header
    print_package_lookup_header(custom_time)

    # print the package information
    print(f'    Package ID: {parcel.id}\n'
          f'    Address: {parcel.address["address"]}\n'
          f'    City: {parcel.address["city"]}\n'
          f'    State: {parcel.address["state"]}\n'
          f'    Zip Code: {parcel.address["zip"]}\n'
          f'    Weight: {parcel.weight}\n'
          f"    Delivery Deadline: {parcel.deadline.time().strftime('%I:%M %p')}\n"
          f'    Notes: {parcel.notes}\n'
          f'    Truck: {parcel.truck}\n'
          f'    Status: {parcel.status}\n'
          )
    if custom_time < parcel.delivery_time.time():
        print(
            f"Expected Delivery Time: {parcel.delivery_time.time().strftime('%I:%M %p')}")
    elif custom_time >= parcel.delivery_time.time():
        print(
            f"Delivered At: {parcel.delivery_time.time().strftime('%I:%M %p')}")

    distances = load_distance_csv()
    l1, m1 = trucks[0].execute_route(custom_time, distances)
    l2, m2 = trucks[0].execute_route(custom_time, distances)
    l3, m3 = trucks[0].execute_route(custom_time, distances)
    print(f'\nCumulative Truck Miles: {round(m1 + m2 + m3, 1)}')

    print()

    # allows users to return to the main menu or exit the program
    next_input = input(
        '\nEnter 0 to return to the main menu.\nEnter any other key to exit.\n')
    if next_input == '0':
        interface_main(package_hashTable, trucks)
    else:
        print('\n\n\n\nGoodbye!\n\n\n')
        sys.exit()


def print_truck_stats_report_header(custom_time):
    width = 145
    divider = '-' * 70
    time_str = custom_time.strftime('%I:%M %p')

    print(f"""

    {divider:^{width}}
    {"All Trucks Summary":^{width}}
    {f"At Time: {time_str}":^{width}}
    {divider:^{width}}

    """)


def truck_stats(custom_time, package_hashTable, trucks):
    """
    Show all truck statistics.
    """
    distances = load_distance_csv()
    locations = load_locations_csv()

    # collects and sorts packages by truck
    truck_packages = {truck.id: [] for truck in trucks}
    for truck in trucks:
        for parcel in truck.packages:
            truck_packages[truck.id].append(str(parcel.id))
    for pkg_list in truck_packages.values():
        pkg_list.sort()

    print_truck_stats_report_header(custom_time)
    print('\n\n')

    total_miles = 0

    for truck in trucks:
        packages = truck_packages[truck.id]
        print(f'---------------  Truck {truck.id}  ----------------')
        print('General Information')
        print(
            f"Departure Time: {truck.departure_time.time().strftime('%I:%M %p')}")
        print(f'Driver: {truck.driver}')
        print("Today's Assigned Packages: " + ', '.join(packages))

        progress_location, progress_miles = truck.execute_route(
            custom_time, distances)
        total_miles += progress_miles

        print('\nCurrent Progress')
        if truck.route and progress_location == truck.route[-1]:
            if truck.id == 1 and truck.route[-1] != 0:
                update_ending_location(truck, truck.route, 0)
                progress_location = 0
        print(f'Latest Location: {locations[progress_location]}')
        print(f'Miles Traveled so Far: {round(progress_miles, 1)}')

        if truck.route and progress_location == truck.route[-1]:
            print('Route Completed')
        print('\n')

    # summary
    print(
        f"Total miles traveled by {custom_time.strftime('%I:%M %p')}: {round(total_miles, 1)}\n\n")

    # menu navigation
    next_input = input(
        '\nEnter 0 to return to the main menu.\nEnter any other key to exit.\n')
    if next_input == '0':
        interface_main(package_hashTable, trucks)
    else:
        print('\n\nGoodbye!\n\n\n')
        sys.exit()
