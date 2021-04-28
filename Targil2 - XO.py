"""
Targil 2
By Ohad Omrad
Python and Git
"""

import Utility

class XOWinner:
    _XO_N = 3 # an a class var (the matrix size 3X3)

    def __init__(self, game):
        self._isWinner = True # is their a winner
        self._game = game # the game board

    @classmethod
    def fromStringUnput(cls):
        pass

    @classmethod
    def fromInputBoard(cls):
        # "constructor overloading" - input the board in an interactive way
        game = XOWinner.imputGameResults()
        return cls(game)

    @staticmethod
    def imputGameResults():
        # This method inputs the board from the user and return the game board
        game = []
        print("Enter a 3x3 Matrix of tic tac toe results\n")
        print("Player1 (X) = 1\nPlayer2 (O) = 2\nEmpty Cell = 0\n")
        for i in range(XOWinner._XO_N):
            a = []
            print("\nInput row " + str(i+1) + ":")

            for j in range(XOWinner._XO_N):
                user_input = Utility.integer_input(int(-1))
                while user_input != 0 and user_input != 1 and user_input != 2:
                    print("INVALID INPUT")
                    user_input = Utility.integer_input(int(-1))
                a.append(int(user_input))
            game.append(a)

        return game

    def _cheakRows(self):
        # This method check if their is a victory at one of the rows
        # if their is a winner -> return the player who has won
        # else -> return 0

        for i in range(XOWinner._XO_N):
            self._isWinner = True
            player = self._game[i][0]
            if player == 0:
                continue
            for j in range(XOWinner._XO_N):
                if self._game[i][j] != player:
                    self._isWinner = False
                    break
            if self._isWinner:
                print("Player " + str(player) +" has won at *row " + str(i+1)+"*")
                return player
        return 0


    def _cheakCols(self):
        # This method check if their is a victory at one of the cols
        # if their is a winner -> return the player who has won
        # else -> return 0

        for j in range(XOWinner._XO_N):
            self._isWinner = True
            player = self._game[0][j]
            if player == 0:
                continue
            for i in range(XOWinner._XO_N):
                if self._game[i][j] != player:
                    self._isWinner = False
                    break
            if self._isWinner:
                print("Player " + str(player) +" has won at *col " + str(j+1) + "*")
                return player
        return 0


    def _cheackDiagonal(self):
        # This method check if their is a victory at one of the diagonals
        # if their is a winner -> return the player who has won
        # else -> return 0

        self._isWinner = True
        player = self._game[0][0]

        if player != 0:
            for i in range(XOWinner._XO_N):
                if self._game[i][i] != player:
                    self._isWinner = False
                    break
            if self._isWinner:
                print("Player " + str(player) + " has won at the *Main Diagonal*")
                return player

        self. _isWinner = True
        player = self._game[0][XOWinner._XO_N-1]

        if player != 0:
            for i in range(XOWinner._XO_N):
                if (self._game[i][XOWinner._XO_N-1-i] != player):
                    self._isWinner = False
                    break
            if self._isWinner:
                print("Player " + str(player) + " has won at the *Second Diagonal*")
                return player
        return 0


    def cheakWinner(self):
        # This method use the checks methods and print the player who has won in a case of a victory
        # otherwise the method prints that its a tie
        retVal = max(self._cheakRows(), self._cheakCols(), self._cheackDiagonal())
        if retVal != 0:
            print(f"player {retVal} has won!")
        else:
            print("its a tie!")

    def printGameBoard(self):
        # This method print the board
        for i in range(XOWinner._XO_N):
            for j in range(XOWinner._XO_N):
                print(self._game[i][j], end = " ")
            print()


def main():
    object = XOWinner([[0,1,2],
                       [2,1,0],
                       [2,2,2]])
    #object = XOWinner.fromInputBoard()
    object.printGameBoard()
    object.cheakWinner()

if __name__ == "__main__":
    main()