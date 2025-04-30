from datetime import datetime


class Package:
    """
    Package class
    """

    def __init__(self, id, address, deadline, weight, notes, truck=None):
        """
        O(1) - Initialize the package object
        """
        self.id = id
        self.address = address
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.truck = truck
        self.status = "At the hub"
        self.dispatch_time = datetime.strptime("00:00", "%H:%M")
        self.delivery_time = datetime.strptime("00:00", "%H:%M")

    def __str__(self):
        """
        O(1) - Return a string representation of the Package object
        """
        return "%s, %s, %s, %s, %s, %s, %s %s, %s, %s" % (
            self.package_id, self.address, self.city, self.state, self.zip_code,
            self.weight, self.deadline, self.notes, self.status, self.delivery_time)

    def assign_truck(self, truck):
        """
        O(1) - Assigns truck to the package

        returns: boolean, if package was successfully assigned
        """
        self.truck = truck

    def deliver(self):
        """
        O(1) - Delivers the package
        """
        self.truck = None

    def update_status(self, status):
        """
        O(1) - Updates status of the package
        """
        self.status = status

    def update_wrong_address(self):
        """
        O(1) - Fixes address for a package
        - Specific case - Simulation for package.id == 9
        """
        self.address["address"] = '410 S State St'
        self.address["city"] = 'Salt Lake City'
        self.address["state"] = 'UT'
        self.address["zip"] = '84111'
