"""
Ohad Omrad
Python and Git
"""

import threading
import socket

import Bank
import HandleClient
import PrintsForUser

"""
This class responsible to the client side
This client inherit the Thread class -> each client object ran on his own thread
even if we will run some client at the same program
"""
class ATMSocketClient(threading.Thread):

    _menue = """
*******************ATM MENU***********************
*                                                *
*     Enter 1 -> to deposit money                *
*     Enter 2 -> to withdraw money               *
*     Enter 3 -> to transfer money               *
*     Enter 4 -> to display account balance      *
*     Enter 5 -> to display account transactions *
*     Enter 6 -> to exit                         *
*                                                *
**************************************************
"""
    invalidInput = "INVALID INPUT"

    options_dict = {1 : Bank.Bank.optionOne, 2 : Bank.Bank.optionTwo, 3: Bank.Bank.optionThree,
                            4 : Bank.Bank.optionFour, 5 : Bank.Bank.optionFive,
                            6: HandleClient.HandleSocketClient.closeConnection}

    def __init__(self, serverIP, serverPort):
        threading.Thread.__init__(self)
        self._serverIP = serverIP
        self._serverPort = serverPort
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _send_data(self, data):
        """
        This method send a given data to a given client socket
        :return: if the send process succeed return HandleSocketClient.keepConnection
                 else return HandleSocketClient.closeConnection
        """
        try:
            self._sock.send(data.encode())
            return HandleClient.HandleSocketClient.keepConnection
        except:
            return HandleClient.HandleSocketClient.closeConnection

    def _received_data(self):
        """
        This method wait for a data from a given client socket
        :return: if the receive process succeed return the data that we got
                 else return HandleSocketClient.closeConnection
        """
        try:
            return self._sock.recv(Bank.Bank.numBytes).decode()
        except:
            return HandleClient.HandleSocketClient.closeConnection


    def run(self):
        """
        This method is the client's thread main method
        """

        # connect to the server
        try:
            self._sock.connect((self._serverIP, self._serverPort))
        except:
            PrintsForUser.printError("Can't connect to the server")
            return

        retVal = self.loginToServer()
        if not retVal:
            self.closeConnection()
            return

        PrintsForUser.printOptions(ATMSocketClient._menue)

        while True:

            # input from the user an option number
            try:
                PrintsForUser.printOptions("Enter: ", newLine=False)
                user_input = int(input())
            except:
                continue

            option = ATMSocketClient.options_dict.get(user_input)
            if option == None:
                continue

            PrintsForUser.printProcess(option)
            self._send_data(option)

            if option == HandleClient.HandleSocketClient.closeConnection:
                self.closeConnection()
                return

            if option == Bank.Bank.optionOne or option == Bank.Bank.optionTwo:
                money = self.getAmountMoney()
                self._send_data(str(money))

            if option == Bank.Bank.optionThree:
                dest_account_name = ATMSocketClient.getDestAccountName()
                self._send_data(str(dest_account_name))

                money = self.getAmountMoney()
                self._send_data(str(money))

            # a client can see his account's balance or transactions without sending his secret code
            if option != Bank.Bank.optionFour and option != Bank.Bank.optionFive:
                secret_code = ATMSocketClient.getSecretCode()
                self._send_data(str(secret_code))

            received_answer = self._received_data()
            if received_answer == HandleClient.HandleSocketClient.closeConnection:
                self.closeConnection()
                return

            PrintsForUser.printProcess(received_answer)


    def getAmountMoney(self):

        # This method input from the client a positive number (amount of money)

        money = ATMSocketClient.invalidInput
        PrintsForUser.printOptions("Enter the amount of money (a positive number): ")
        while money == ATMSocketClient.invalidInput:
            message = ATMSocketClient.invalidInput
            try:
                PrintsForUser.printOptions("Enter: ", newLine=False)
                money = input()
                money = float(money)
                if money <= 0:
                    message = "Negative Amount of money"
                    raise Exception()
            except:
                PrintsForUser.printError(message)
                money = ATMSocketClient.invalidInput
        return money

    def closeConnection(self):
        """
        This method responsible to close the client's server socket
        """
        PrintsForUser.printProcess("", newLine=False)
        print("Close Connection with the server at: ( IP = " + str(self._serverIP)+ " , Port = " + str(self._serverPort) +" )")
        self._sock.close()

    def loginToServer(self):
        """
        This method responsible for the client authentication (Client Side)
        The Protocol key strings:
            "NO ACCOUNT" -> the account name has not found
            "CONTINUE" -> GREEN LIGHT -> continue with the connection to the next step

        :return: True -> if the client login to the server properly
                 else -> return False
        """

        account_name = ATMSocketClient.getAccountName()
        ret_message = self._send_data(account_name)

        if ret_message == HandleClient.HandleSocketClient.closeConnection:
            return HandleClient.HandleSocketClient.closeConnection


        receivedAnswer = self._received_data()
        if receivedAnswer == HandleClient.HandleSocketClient.closeConnection:
            return HandleClient.HandleSocketClient.closeConnection

        if receivedAnswer == Bank.Bank.accountNotExists:
            PrintsForUser.printOptions("", newLine=False)
            answer = input("Their is no account for \"" + account_name + "\"\nDo you wont to create one? [Y,N]: ")
            answer = answer.upper()
            if answer == "Y" or answer == "YES":
                self._send_data(HandleClient.HandleSocketClient.keepConnection)
                self.createAccount()
            else:
                return False

        elif receivedAnswer == HandleClient.HandleSocketClient.keepConnection:
            key = self.getAccountKey()
            self._send_data(key)
            receivedAnswer = self._received_data()

            if receivedAnswer == HandleClient.HandleSocketClient.closeConnection:
                return HandleClient.HandleSocketClient.closeConnection

            if receivedAnswer == Bank.Bank.wrongPassword:
                PrintsForUser.printError(receivedAnswer)
                return False
        return True


    def createAccount(self):
        """
        This method input from the user the needed data to create an account and send them for the server
        if the account name or password are already exist at the bank system the method will ask for
        a new data again

        The DATA: account name, password, secret code
        """

        status = Bank.Bank.accountNameTaken

        while status != Bank.Bank.accountAdded:
            account_name = ATMSocketClient.getAccountName()
            self._send_data(account_name)
            key = ATMSocketClient.getAccountKey()
            self._send_data(key)
            secret_code = ATMSocketClient.getSecretCode()
            self._send_data(secret_code)

            status = self._received_data()
            if status == HandleClient.HandleSocketClient.closeConnection:
                return HandleClient.HandleSocketClient.closeConnection

            if status == Bank.Bank.accountAdded:
                PrintsForUser.printOptions(status)
            else:
                PrintsForUser.printError(status)


    @staticmethod
    def getDestAccountName():
        PrintsForUser.printOptions("Enter the account name that you want to transfer money to: ", newLine=False)
        return str(input())

    @staticmethod
    def getAccountName():
        PrintsForUser.printOptions("Enter your account name: ", newLine=False)
        return str(input())

    @staticmethod
    def getAccountKey():
        PrintsForUser.printOptions("Enter your passwaod: ", newLine=False)
        password = str(input())
        return str(Bank.Bank.genarateKey(password))

    @staticmethod
    def getSecretCode():
        PrintsForUser.printOptions("Enter your secret code: ", newLine=False)
        return str(input())


# Testing
def main():
    client = ATMSocketClient("127.0.0.1", 8000)
    client.start()

if __name__ == "__main__":
    main()