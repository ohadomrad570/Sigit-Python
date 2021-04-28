"""
Ohad Omrad
Python and Git
"""

from abc import ABC, abstractmethod
import os
import sys

import Bank
import pickle
import PrintsForUser

"""
This abstract class define the functionality that each Cache Manager required to have
"""
class CacheManager(ABC):

    @classmethod
    @abstractmethod
    def saveBank(cls, bank: Bank):
        """
        an abstract class method that responsible to save a bank in a file
        """
        pass

    @classmethod
    @abstractmethod
    def loadBank(cls):
        """
        an abstract class method that responsible to load a bank from a file
        """
        pass


"""
This class inherit the CacheManger class and implements the functionality ob File Cache Manger
"""
class FileCacheManager(CacheManager):

    # The file path
    file_name = "Bank Data.txt"
    @classmethod
    def saveBank(cls, bank: Bank):
        """
        This method get a bank object and save it in a file
        """
        try:
            file = open(os.path.join(sys.path[0], FileCacheManager.file_name) , "wb")
        except:
            PrintsForUser.printError("Failed opening file")
            return

        try:
            pickle.dump(bank, file, protocol=pickle.HIGHEST_PROTOCOL)
        except:
            PrintsForUser.printError("Failed saving the current bank state")
        finally:
            file.close()

    @classmethod
    def loadBank(cls):
        """
        This method return the bank object that we saved in our file
        If the file is empty we will return a new Bank object
        :return: a bank object
        """
        try:
            file = open(os.path.join(sys.path[0], FileCacheManager.file_name), "rb")
        except:
            PrintsForUser.printError("Failed opening file")
            return

        try:
            bank = pickle.load(file)
        except EOFError:
            bank = Bank.Bank()
        finally:
            file.close()
        return bank