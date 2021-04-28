"""
Ohad Omrad
Python and Git
"""

"""
This class constitutes a Decorator Cache
"""
class DecoratorChache:

    def __init__(self, function):
        self._cahche = {}
        self._function = function

    def __str__(self):
        # This method return a string that contain the cached results

        retVal = "Cached Calculations:"
        for key, y in self._cahche.items():
            retVal += "\nf(" + key + ") = " + str(y)
        return retVal


    def _generateKey(self, *argv):
        # This method gets the function's current parameters and generate a key
        # example: argv = (x1,x2) -> key = str(x1)+","+str(x2)
        print("[INFO] Generate Key")
        key = ""
        for parm in argv:
            key += str(parm) +","

        key = key[:len(key)-1]
        print("key: "+key)
        return key


    def _saveResult(self, key, y):
        # This method saves the function call with the parameters that represent by key
        print("[INFO] Saves Result: f(" + key + ") = " + str(y))
        self._cahche[key] = y


    def applyFucntion(self, *argv):
        key = self._generateKey(*argv)
        y = self._cahche.get(key)

        if y == None:
            print("[INFO] Calculate f(" + key + ") = ?")
            y = self._function(*argv)
            self._saveResult(key,y)

        else:
            print("[INFO] Solutions is already exists f(" + key + ") = " + str(y))
        return y


def mul(*argv):
    # This function get N parameters and multiply them one another
    retVal = 1
    for parm in argv:
        retVal *= parm
    return retVal


def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


# Testing
def main():
    print("\n*************** fibonacci  Cache ***************\n")
    buffer = "\n" + "-" * 50 + "\n"
    fibCache = DecoratorChache(fib)

    for i in range(5):
        fibCache.applyFucntion(i)

    n = 20
    fibCache.applyFucntion(n)
    fibCache.applyFucntion(n)

    print(buffer)
    print(fibCache.__str__())

    print("\n*************** multiplication Cache ***************\n")

    mulCache = DecoratorChache(mul)
    x1 = 6
    x2 = 2
    mulCache.applyFucntion(x1,x2)
    mulCache.applyFucntion(x1,x2)

    print(buffer)
    print(mulCache.__str__())

if __name__ == "__main__":
    main()