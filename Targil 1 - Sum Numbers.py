"""
By Ohad Omrad
Python and Git
"""

# Targil 1.a
def sumNumbers_Interactive():
    """
    This function get inputs and sum them
    If the user type 'stop' the function display the sum and exit
    Interactive - Each iteration of the loop the function asks for an input
    """

    sum = 0
    print("Enter a number or \'stop\' to stop the input\n")
    user_input = input("Enter: ")

    while user_input != "stop":
        try:
            sum += float(user_input)
        except:
            print("INVALID INPUT")
        user_input = input("Enter: ")
    print(f"SUM = {sum}\n")


# Targil 1.b
def sumNumbers_Uninteractive():
    """
    This function interpret the input of the users and sum its numbers tokens
    Uninteractive - the function asks for input one time
    """

    sum = 0
    print("Enter series of numbers\n")
    user_input = input("Enter: ")
    user_input = user_input.split(',')
    for num in user_input:
        try:
            sum += float(num)
        except:
            print("INVALID TOKEN")
    print(f"SUM = {sum}\n")


def main():
    sumNumbers_Interactive()
    sumNumbers_Uninteractive()

if __name__ == "__main__":
    main()