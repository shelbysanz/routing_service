class PackageHt:
    """
    Package hash table that stores the package objects
    """
    def __init__(self, size=40, package_count=0):
        """
        O(1) - Inititalizes the hash table with 40 empty buckets
        """
    def get_package_bucket(self, package_id):
        """
        O(1) - Gets the hash of the package using the package id
        """
    def insert(self, package_id, package_data):
        """
        O(n) - Insert/update a package using the package id and the package list
        """
    def lookup(self, package_id):
        """
        O(n) - Find a package using the package_id
        """
    def resize(self):
        """
        O(n^2) - Resizing the hash table to fit the package size and copy over the existing values
        """
