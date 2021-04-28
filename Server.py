"""
Ohad Omrad
Python and Git
"""
from abc import ABC, abstractmethod
from _thread import *
import threading
import socket

import HandleClient
import Bank

import PrintsForUser

"""
An abstract server
"""
class Server(ABC):
    def __init__(self, host, port):
        self._host = host   # Server IP Address
        self._port = port   # Server Port Number
        self._stop = False

    @abstractmethod
    def start(self, clientHandler: HandleClient):
        """
        This method run the server
        Get: a a client handler that responsible to handle a connection with a client
            * Injection of functionality
        """
        pass

    @abstractmethod
    def stop(self):
        pass

"""
An abstract class that inherit Server class and implement the common functionality of the both kids of servers at
this project
"""
class MyCommonServer(Server):
    def __init___(self, host: str, port: int):
        super().__init__(self, host, port)
        self._clientHandler = None


    def start(self, clientHandler: HandleClient):
        self._clientHandler = clientHandler
        self._runServer()

    @abstractmethod
    def _runServer(self):
        pass

    def stop(self):
        self._stop = True


    def _wrapper_client_handler(self, aClient: socket, addr: str):
        """
        This method wrapper the client handler's method and handle the client connection and the closer of that
        connection
        Get: aClient socket and his IP Address
        """
        self._clientHandler.handleClient(aClient)
        self._closeConnectionWithAClient(aClient, addr)


    def _closeConnectionWithAClient(self, aClient: socket, addr: str):
        """
        this method responsible to close a connection with a client and save the additional data
        """
        PrintsForUser.printProcess("", newLine=False)
        print("Close Connection with client at address" + str(addr))
        aClient.close()


"""
This class inherit MyCommonServer and implement Serial Server
"""
class MySerialServer(MyCommonServer):
    """
    *listen() method*
    defines the length of the backlog queue, which is the number of incoming connections
    that have been completed by the TCP/IP stack
    but not yet accepted by the application.
    """
    _backlog_queue_size = 1


    def __init___(self, host: str, port: int):
        super().__init__(self, host,port)

    def _runServer(self):
        """
        This method responsible to run the server
        here the server can handle one client at the time
        """

        try:
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.bind((self._host, self._port))
            serverSocket.listen(MySerialServer._backlog_queue_size)
            self._clientHandler.printAllBankAccounts()
            PrintsForUser.printProcess("\nSerial Server started and listening\n")

        except:
            PrintsForUser.printError("Server Failed")
            return

        while not self._stop:
            aClient, addr = serverSocket.accept()
            PrintsForUser.printProcess("", newLine=False)
            print('Connected by', addr)
            self._wrapper_client_handler(aClient, addr)

        serverSocket.close()
"""
This class inherit MyCommonServer and implement Parallel Server
"""
class MyParallelServer(MyCommonServer):
    """
    *listen() method*
    defines the length of the backlog queue, which is the number of incoming connections
    that have been completed by the TCP/IP stack
    but not yet accepted by the application.
    """
    _backlog_queue_size = 5

    def __init___(self, host: str, port: int):
        super().__init__(self, host,port)


    def _runServer(self):
        """
        This method responsible to run the server
        here the server can handle _max_clients clients at the time
        """

        try:
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.bind((self._host, self._port))
            serverSocket.listen(MyParallelServer._backlog_queue_size)
            self._clientHandler.printAllBankAccounts()
            PrintsForUser.printProcess("\nParallel Server is started and listening\n")

        except:
            PrintsForUser.printError("Server Failed")
            return

        while not self._stop:
            aClient, addr = serverSocket.accept()
            PrintsForUser.printProcess("", newLine=False)
            print('Connected by', addr)
            start_new_thread(self._wrapper_client_handler, (aClient, addr))


# Testing
def main():
    server = MySerialServer("127.0.0.1", 8000)
    bank = Bank.Bank.bank_from_file()
    myHandle = HandleClient.HandleSocketClient(bank)
    server.start(myHandle)

if __name__ == "__main__":
    main()