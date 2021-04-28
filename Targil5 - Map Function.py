"""
Ohad Omrad
Python and Git
"""

import math

def Map(f, list):
    # This function get a function and a list and apply the function on any item in the list
    # Get: f (function), list = [x, y, ...]
    # return: the function return a new list with the new items [f(x), f(y), ...]
    return [f(item) for item in list]


# Testing
def main():
    list = [4, 16, 256, 400, 500]
    f = math.sqrt
    flist = Map(f, list)

    for i in range(len(list)):
        print("f("+str(list[i]) + ") = " + str(flist[i]))

if __name__ == "__main__":
    main()