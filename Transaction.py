"""
Ohad Omrad
Python and Git
"""

import Account
"""
This Class represent a transaction between two accounts
"""
class Transaction:
    def __init__(self, src_account: Account, dest_account: Account, amount: float):
        self._src_account = src_account     # source account
        self._dest_account = dest_account   # destination account
        self._amount = amount               # the transferred amount of money

    def __str__(self):
        src_name = self._src_account.getAccountName()
        dest_name = self._dest_account.getAccountName()
        return "[ " + src_name  +" -> " + dest_name + " , amount: " + str(self._amount) +" ]"

    def getAmount(self):
        return self._amount

    def getSource(self):
        return self._src_account

    def getDest(self):
        return self._dest_account