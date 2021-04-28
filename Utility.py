"""
By Ohad Omrad
Python abd Git
"""

def integer_input(default_ret_value):
    user_input = input("Enter: ")
    try:
       n = int(user_input)
    except:
        n = default_ret_value
    finally:
        return n



def float_input(default_ret_value):
    user_input = input("Enter: ")
    try:
       f = float(user_input)
    except:
        f = default_ret_value
    finally:
        return f
