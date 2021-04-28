"""
Ohad Omrad
Python and Git
"""

import pickle
import threading
import PrintsForUser

"""
This class represent an Account in the bank
"""
class Account:
    _lock = threading.RLock()
    def __init__(self, account_name, secret_code):
        self._account_name = account_name
        self._secret_code = secret_code
        self._transactions = []
        self._balance = 0.0

    def getAccountName(self):
        return self._account_name

    def getSecretCode(self):
        return self._secret_code

    def getBalance(self):
        return self._balance

    def updateBalance(self, money):
        # locking the account's balance
        with Account._lock:
            self._balance += money

    def printBalance(self):
        print("Account Balance: " + self._balance)

    def addTransaction(self, transaction):
        """
        This method get a transaction
        ans add it to the transactions list *if* the current account is part of the transaction (src or dest)
        :return: a boolean: return true if the transaction added else return false
        """
        if self != transaction.getSource() and self != transaction.getDest():
            return False
        self._transactions.append(transaction)
        return True

    def getAllTransactions_as_string(self):
        """
        This method build a string that represent the account's transactions
        """

        res = ""
        for transaction in self._transactions:
            res += str(transaction)
            res += "\n"

        if res == "":
            res += "Their are no transactions"
        return res