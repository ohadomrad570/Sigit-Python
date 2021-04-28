"""
Ohad Omrad
Python and Git
"""

from abc import ABC, abstractmethod
import socket
import Bank

"""
This class define a Client Handler 
"""
class HandleClient(ABC):
    @abstractmethod
    def handleClient(self, aClient: socket):
        """
        This method responsible to habndle a client -> define the server side protocol
        """
        pass

"""
This class inherit the HandleClient class and implement the server side protocol at our project
"""
class HandleSocketClient(HandleClient):

    # The Protocol (adding casing to the bank protocol)
    keepConnection = "CONTINUE"
    closeConnection = "CLOSE CONNECTION"

    def __init__(self, bank: Bank):
        self._bank = bank

    def saveData(self):
        self._bank.save_bank_in_file()

    def printAllBankAccounts(self):
        """
        This method prints all banks accounts
        """
        self._bank.printAllAccounts()


    def _send_data(self, aClient, data):
        """
        This method send a given data to a given client socket
        :return: if the send process succeed return HandleSocketClient.keepConnection
                 else return HandleSocketClient.closeConnection
        """
        try:
            aClient.send(data.encode())
            return HandleSocketClient.keepConnection
        except:
            return HandleSocketClient.closeConnection

    def _received_data(self, aClient):
        """
        This method wait for a data from a given client socket
        :return: if the receive process succeed return the data that we got
                 else return HandleSocketClient.closeConnection
        """
        try:
            return aClient.recv(Bank.Bank.numBytes).decode()
        except:
            return HandleSocketClient.closeConnection


    def handleClient(self, aClient: socket):
        """
        This method handle a client
        """

        # Step 1: login or creating an account
        account = self.client_authentication(aClient)

        if account == HandleSocketClient.closeConnection:
            return  # The connection will be closed by the server

        # Step 2: ATM Menu
        while True:
            # Step 2.1: input the client selected action
            received_choice = str(self._received_data(aClient))
            send_message = ""

            if received_choice == HandleSocketClient.closeConnection:   # exit
                return

            if received_choice == Bank.Bank.optionOne:
                send_message = self.case_one(aClient, account)

            if received_choice == Bank.Bank.optionTwo:
                send_message = self.case_two(aClient, account)

            if received_choice == Bank.Bank.optionThree:
                send_message = self.case_three(aClient, account)

            if received_choice == Bank.Bank.optionFour:
                send_message = self.case_four(account)

            if received_choice == Bank.Bank.optionFive:
                send_message = self.case_five(account)

            self._send_data(aClient, send_message)

            if send_message == HandleSocketClient.closeConnection:
                return


    def client_authentication(self, aClient):
        """
        This method responsible for the client authentication (Server Side)
        if their is no account the method suggests to create one
        :param: aClient socket
        :return: This method return the client account.
                 if the connection between the server and the client failed -> return HandleSocketClient.closeConnection
        """
        account_name = str(self._received_data(aClient))
        if account_name == HandleSocketClient.closeConnection:
            return HandleSocketClient.closeConnection

        retVal = self._bank.isAccountNameExists(account_name)

        if not retVal:
            self._send_data(aClient, Bank.Bank.accountNotExists)
            answer = str(self._received_data(aClient))
            if answer == HandleSocketClient.keepConnection:
                account = self._createAccount(aClient)
                return account
            else:
                return HandleSocketClient.closeConnection

        self._send_data(aClient, HandleSocketClient.keepConnection)

        given_key = str(self._received_data(aClient))
        if given_key == HandleSocketClient.closeConnection:
            return HandleSocketClient.closeConnection

        ret_message = self._bank.check_given_account_key(account_name, given_key)

        if ret_message != Bank.Bank.correctKey:
            self._send_data(aClient, ret_message)
            return HandleSocketClient.closeConnection

        self._send_data(aClient, HandleSocketClient.keepConnection)
        account = self._bank.getAccount(given_key)
        return account

    def _createAccount(self, aClient):
        """
        This method creates a new account and add it to the bank system
        if the received account details are already taken the method will asked for them again
        :param aClient socket:
        :return: a new account
                 if the connection between the server and the client failed -> return HandleSocketClient.closeConnection
        """

        status = Bank.Bank.accountNameTaken

        while status != Bank.Bank.accountAdded:

            account_name = str(self._received_data(aClient))
            if account_name == HandleSocketClient.closeConnection:
                return HandleSocketClient.closeConnection

            key = str(self._received_data(aClient))
            if key == HandleSocketClient.closeConnection:
                return HandleSocketClient.closeConnection

            secret_code = str(self._received_data(aClient))
            if secret_code == HandleSocketClient.closeConnection:
                return HandleSocketClient.closeConnection

            # Call to addAccount() bank's method
            status, account = self._bank.addAccount(account_name, key, secret_code)
            self._send_data(aClient, status)

        return account


    def received_secret_code(self, aClient):
        return str(self._received_data(aClient))

    # DEPOSIT
    def case_one(self, aClient, account):
        """
        This method manage the first option -> DEPOSIT money in the account
        :return: a massage that indicate if the deposit action succeed
                 if the connection between the server and the client failed -> return HandleSocketClient.closeConnection
        """
        # get the amount of money
        money_string = str(self._received_data(aClient))
        if money_string == HandleSocketClient.closeConnection:
            return HandleSocketClient.closeConnection

        money = float(money_string)
        # get the secret code
        secret_code = self.received_secret_code(aClient)
        if secret_code == HandleSocketClient.closeConnection:
            return HandleSocketClient.closeConnection

        # Call to bank's deposit() method
        ret_message = self._bank.deposit(account, money, secret_code)

        # save the new bank state at the file
        if ret_message == Bank.Bank.success:
            self.saveData()

        return ret_message


    # WITHDRAW
    def case_two(self, aClient, account):
        """
        This method manage the second option -> WITHDRAW money from the account
        :return: a massage that indicate if the withdraw action succeed
                 if the connection between the server and the client failed -> return HandleSocketClient.closeConnection
        """
        # get the amount of money
        money_string = str(self._received_data(aClient))
        if money_string == HandleSocketClient.closeConnection:
            return HandleSocketClient.closeConnection

        money = float(money_string)

        # get the secret code
        secret_code = self.received_secret_code(aClient)
        if secret_code == HandleSocketClient.closeConnection:
            return HandleSocketClient.closeConnection

        # Call to bank's withdraw() method
        ret_message = self._bank.withdraw(account, money, secret_code)

        # save the new bank state at the file
        if ret_message == Bank.Bank.success:
            self.saveData()

        return ret_message


    # TRANSFER
    def case_three(self, aClient, src_account):
        """
        This method manage the third option -> TRANSFER money from our account to another account
        :return: a massage that indicate if the transfer action succeed
                 if the connection between the server and the client failed -> return HandleSocketClient.closeConnection
        """

        # get the dest account name
        dest_account_name = str(self._received_data(aClient))
        if dest_account_name == HandleSocketClient.closeConnection:
            return HandleSocketClient.closeConnection

        if not self._bank.isAccountNameExists(dest_account_name):
            return Bank.Bank.accountNotExists
        dest_account = self._bank.getAccount_by_account_name(dest_account_name)

        # get the amount of money
        money_string = str(self._received_data(aClient))
        if money_string == HandleSocketClient.closeConnection:
            return HandleSocketClient.closeConnection

        money = float(money_string)

        # get the secret code
        src_secret_code = self.received_secret_code(aClient)
        if src_secret_code == HandleSocketClient.closeConnection:
            return HandleSocketClient.closeConnection

        # Call to bank's transfer() method
        ret_message = self._bank.transfer(src_account, dest_account, money, src_secret_code)

        # save the new bank state at the file
        if ret_message == Bank.Bank.success:
            self.saveData()

        return ret_message

    # DISPLAY ACCOUNT'S BALANCE
    def case_four(self, account):
        return "Your Account's Balance: " + str(account.getBalance())

    # DISPLAY ACCOUNT'S TRANSACTIONS
    def case_five(self, account):
        return account.getAllTransactions_as_string()
