"""
Ohad Omrad
Python and Git
"""

"""
    this file contains the functions that prints messages for the user in colors
"""

from colorama import init, Fore, Back, Style

def printError(message, newLine = True):
    """
    Get: message
    prints it in red
    """
    init(convert=True)
    if newLine:
        print(Fore.RED + message)
    else:
        print(Fore.RED + message, end="")
    Style.RESET_ALL


def printOptions(message, newLine = True):
    """
    Get: message
    prints it in green
    """
    init(convert=True)
    if newLine:
        print(Fore.GREEN + message)
    else:
        print(Fore.GREEN + message, end="")

    Style.RESET_ALL


def printProcess(message, newLine = True):
    """
    Get: message
    prints it in blue
    """
    init(convert=True)
    if newLine:
        print(Fore.BLUE + message)
    else:
        print(Fore.BLUE + message, end="")
    Style.RESET_ALL