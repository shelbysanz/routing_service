from datetime import time


class PackageHt:
    """
    Package hash table that stores the package objects
    """
    load_factor = 1.5
    packages = 0

    def __init__(self, size=40, package_count=0):
        """
        O(1) - Inititalizes the hash table with 40 empty buckets
        """
        self.size = size
        self.table = [[] for _ in range(self.size)]
        self.package_count = package_count

    def get_package_bucket(self, package_id):
        """
        O(1) - Gets the hash of the package using the package id
        """
        i = hash(package_id) % self.size
        bucket = self.table[i]
        return bucket

    def insert(self, package_id, package_data):
        """
        O(n) - Insert/update a package using the package id and the package list
        """
        bucket = self.get_package_bucket(package_id)
        package_info = [package_id, package_data]

        if bucket in self.table:
            for package in bucket:
                if package[0] == package_id:
                    package[1] = package_data
                    return True

            bucket.append(package_info)
            return True

        self.package_count += 1
        load = self.package_count / self.size
        if load > PackageHt.load_factor:
            self.resize()

    def lookup(self, package_id):
        """
        O(n) - Find a package using the package_id
        """
        try:
            bucket = self.get_package_bucket(package_id)
            if bucket in self.table:
                for package in bucket:
                    if package[0] == package_id:
                        return package[1]
        except Exception:
            raise LookupError(f"Package not found, id: {package_id}")

    def resize(self):
        """
        O(n^2) - Resizing the hash table to fit the package size and copy over the existing values
        """
        tmp_packages = self.table.copy()

        # create an empty hash table and double the size
        new_table = PackageHt(self.size * 2, self.package_count)
        self = new_table

        for package_id, package_data in tmp_packages:
            self.insert(package_id, package_data)

    def update_all_statuses(self, custom_time):
        """
        O(n) - Updates the status of each package at a certain time
        """
        for i in range(1, self.size + 1):
            package = self.lookup(i)
            if not package:
                continue
            # special case package with id 9, needs to be updated with the right address
            if custom_time >= time(10, 20):
                if package.id == 9:
                    # updates wrong address
                    package.update_wrong_address()
            if custom_time < package.dispatch_time.time():
                package.update_status("At the hub")
            elif package.dispatch_time.time() <= custom_time < package.delivery_time.time():
                package.update_status("En route")
            elif custom_time >= package.delivery_time.time():
                package.update_status("Delivered")
