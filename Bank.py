"""
Ohad Omrad
Python and Git
"""
import hashlib
import threading

import Account
import Transaction
import CacheManager
import PrintsForUser

"""
This class represent a bank
"""
class Bank():

    numBytes = 1024    # The maximum number of Bytes to be received from a socket
    _code = 0          # Bank's code generator
    _lock = threading.RLock()     # Bank's Lock -> in case of multi threading

    # Bank Protocol
    accountNameTaken = "ACCOUNT NAME ALREADY TAKEN"
    accountKeyTaken = "ACCOUNT PASSWORD ALREADY TAKEN"
    accountNotExists = "ACCOUNT NOT EXISTS"
    accountAdded = "ACCOUNT ADDED"

    wrongSecretCode = "WRONG SECRET CODE"
    wrongPassword = "WRONG PASSWORD"
    correctKey = "MATCH PASSWORD"
    noEnoughMoney = "ACCOUNT EXCEEDED"

    accountNotBelong = "ACCOUNT NOT BELONG TO THE BANK"

    success = "SUCCESS"

    # Bank's accounts Actions
    optionOne = "DEPOSIT"
    optionTwo = "WITHDRAW"
    optionThree = "TRANSFER"
    optionFour = "DISPLAY ACCOUNT'S BALANCE"
    optionFive = "DISPLAY ACCOUNT'S TRANSACTIONS"

    @staticmethod
    def genarateKey(password):
        """
        This method get a password as a string and return the password hash code using MD5 hash function
        """
        return str(hashlib.md5(str(password).encode()).digest())

    """
    _____________________objects methods_____________________
    """

    def __init__(self, bankName=""):
        self.bankName = bankName
        self.bankCode = Bank._code
        Bank._code += 1
        self.balance = 0

        # used to save all the credentials of all the accounts
        # The format: {account_name : hash(password), ...} , note: key = hash(password)
        self.credentials_dict = {}

        # for each account Their is: one account name and one password
        # The format: {hash(password) : account, ...}
        # example: accounts = {ohad_key: ohad_account, noa_key: noa_account }

        self.accounts_dict = {}

    @classmethod
    def bank_from_file(cls):
        """
        Constructor overloading -> load a bank from a file
        """
        bank = CacheManager.FileCacheManager.loadBank()
        return bank

    def save_bank_in_file(self):
        """
        This method save the bank in a file
        """
        CacheManager.FileCacheManager.saveBank(self)

    def getAccount_by_account_name(self, account_name):
        """
        This method get an account name and return his account
        The method assume that the account name is exists in the bank
        """
        account_key = self.getAccountKey(account_name)
        account = self.getAccount(account_key)
        return account


    def getAccountKey(self, account_name):
        """
        This method get the account name and return its match key
        """
        return self.credentials_dict.get(account_name)

    def getAccount(self, key):
        """
        This method get the account key and return its match account
        """
        return self.accounts_dict.get(key)

    def isAccountBelong(self, account):
        """
        This method get an account, and check if its belong to the bank
        :return: a boolean
        """
        if account in self.accounts_dict.values():
            return True
        return False

    def isAccountNameExists(self, account_name):
        """
        This method get an account name, and check if its exists in the bank system
        :return: a boolean
        """
        if account_name in self.credentials_dict.keys():
            return True
        return False

    def isKeyExists(self, key):
        """
        This method get an account key, and check if its exists in the bank system
        :return: a boolean
        """
        if key in self.accounts_dict.keys():
            return True
        return False

    def check_given_account_key(self, account_name, given_key):
        """
        This method get an account name and an account key, and check
        if the given key is match to the saved key for this account
        :return: if the account name not exists in the system -> return Bank.accountNotExists
                if the given key is not match to the saved key for this account -> return Bank.wrongPassword
                else -> return Bank.correctKey
        """
        if not self.isAccountNameExists(account_name):
            return Bank.accountNotExists
        system_key = self.getAccountKey(account_name)

        if str(system_key) != str(given_key):
            return Bank.wrongPassword

        return Bank.correctKey


    def addAccount(self, account_name, key, secret_code):
        """
        This method get the account details and create new account and adding it to the bank
        :return: return a tuple -> if the account is already exists: (status, None)
                                   else ("ACCOUNT ADDED", account object)
        """

        # Step 1: Check if the given account name is already exist in the system
        if self.isAccountNameExists(account_name):
            return (Bank.accountNameTaken, None)

        # Step 2: Check if the given key is already exist in the system
        if self.isKeyExists(key):
            return (Bank.accountKeyTaken, None)

        # Step 3: adding the account to the bank system
        self.credentials_dict[account_name] = key
        account = Account.Account(account_name, secret_code)
        self.accounts_dict[key] = account

        PrintsForUser.printOptions("[INFO] Adding new account: ")
        Bank.printAccount(key, account)

        return Bank.accountAdded, account

    def printAllAccounts(self):
        """
        This method prints all the account in the bank using the printAccount() static method
        :return:
        """
        numStars = 45
        string = "BANK ACCOUNTS"
        i = 1
        PrintsForUser.printOptions("*" *numStars + string + "*" *numStars +"\n")
        for key in self.credentials_dict.values():
            PrintsForUser.printOptions("",newLine=False)
            print("*  " + str(i) +". ", end="")
            i += 1
            account = self.getAccount(key)
            Bank.printAccount(key, account)
        PrintsForUser.printOptions("\n" + "*" *(numStars*2+len(string)))

    @staticmethod
    def printAccount(key,account):
        """
        This method get a account's key and the match account and print the account
        :param key:
        :param account:
        :return:
        """
        account_name = account.getAccountName()
        secret_code = account.getSecretCode()
        balance = str(account.getBalance())
        PrintsForUser.printOptions("", newLine=False)
        print("[account name: \""+str(account_name) + "\", key: " + str(key) + ", secret code: " + str(secret_code) +
              " , balance: " + balance + "]")


    def updateBankBalance(self, money):
        """
        This method responsible to update the bank balance
        :param money:
        """
        with Bank._lock:
            self.balance += money


    def check_secret_code(self, account, secret_code):
        """
        This method check if the given secret code is match to the account secret code
        :return: if it match -> return True
                 else return False
        """

        if account.getSecretCode() != secret_code:
            return False
        return True


    def deposit(self, account, money, secret_code = None, transfer = False):
        """
        This method deposit money in the account
        :return: if the account is not belong to the bank -> return Bank.accountNotBelong
                 if the given secret code is not match to the account's secret code -> return Bank.wrongSecretCode
                 else -> return Bank.success

        assumption: we can deposit money only in at account that belongs to the bank
        """

        # cant happened at our client-server (ATM-Bank) System
        if not self.isAccountBelong(account):
            return Bank.accountNotBelong

        if not transfer:
            if not self.check_secret_code(account, secret_code):
                return Bank.wrongSecretCode


        account.updateBalance(money)
        self.updateBankBalance(money)
        return Bank.success


    def withdraw(self, account, money, secret_code):
        """
        This method withdraw maney from the account
        The account must to be belong to the current bank

        :return: if the account is not belong to the bank -> return Bank.accountNotBelong
                 if the given secret code is not match to the account's secret code -> return Bank.wrongSecretCode
                 else -> return Bank.success
        """

        # cant happened at our client-server (ATM-Bank) System
        if not self.isAccountBelong(account):
            return Bank.accountNotBelong

        if not self.check_secret_code(account, secret_code):
            return Bank.wrongSecretCode

        if money > account.getBalance():
            return Bank.noEnoughMoney

        money = - money
        account.updateBalance(money)
        self.updateBankBalance(money)
        return Bank.success


    def transfer(self, src_account, dest_account,  money, src_secret_code):
        """
        This method withdraw maney from the account
        The account must to be belong to the current bank

        :return: if the source or dest accounts are not belong to the bank -> return Bank.accountNotBelong
                 if the given source account's secret code is not match to the account's secret code -> return Bank.wrongSecretCode
                 else -> return Bank.success
        """

        # This method transfer money from source account to destination account
        # assumption: we can transfer money between two accounts that belongs to the bank

        ret_message = self.withdraw(src_account, money, src_secret_code)
        if ret_message != Bank.success:
            return ret_message
        ret_message = self.deposit(dest_account, money, transfer=True)

        transaction = Transaction.Transaction(src_account,dest_account, money)
        src_account.addTransaction(transaction)
        dest_account.addTransaction(transaction)

        return ret_message


    def deleteAccount(self, account_name, account_key, secretCode):
        """
        This method get the account details and delete the match account
        :return: if the account name is not wxists -> return Bank.accountNotExists
                 if the given key is wrong -> return Bank.wrongPassword
                 if the given secret code is wrong -> return Bank.wrongSecretCode
                 else -> return Bank.success
        """

        # Step 1: find the match key for the account name
        if not self.isAccountNameExists(account_name):
            return Bank.accountNotExists

        system_key = self.getAccountKey(account_name)

        # Step 2: compare the given key to the system key
        if system_key != account_key:
            return Bank.wrongPassword

        # Step 3: the user has an access to the account
        account = self.getAccount(system_key)

        # Step 4: compare between the account's secret code to the given secret code
        if account.getSecretCode() != secretCode:
            return Bank.wrongSecretCode

        # Step 5: sub account's balance from the bank's balance
        self.updateBankBalance(-account.getBalance())

        # Step 6: Delete the account
        PrintsForUser.printOptions("[INFO] Deleting Account")
        Bank.printAccount(system_key, account)
        self.accounts_dict.pop(system_key)
        self.credentials_dict.pop(account_name)
        return Bank.success


# Testing
def main():
    bank = Bank("MyBank")
    account_name = "ohad"
    key = "123"
    secret_code = "456"
    bank.addAccount(account_name, key, secret_code)
    bank.addAccount("noa", "999", "999")
    print(bank.deleteAccount(account_name, key, secret_code))

    bank.printAllAccounts()

if __name__ == "__main__":
    main()