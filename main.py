from helper import dispatch, package_hashTable, initial_trucks
from interface import interface_main

"""
 This runs the program
 It ensures it runs only when executed and not when simply imported

 Created by: Shelby Sanchez-Herrera | Student ID: 012272973
"""
if __name__ == "__main__":
    dispatch(initial_trucks)
    interface_main(package_hashTable, initial_trucks)
