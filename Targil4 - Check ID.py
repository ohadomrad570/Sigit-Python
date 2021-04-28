"""
By Ohad Omrad
Python and Git
"""

def checkIDFormat(full_id):
    # This method checks if the ID's format is valid

    digits = "0123456789"

    start_id, last_digit = full_id.split('-')
    # check the id parts lengths
    if len(start_id) != 8 or len(last_digit) != 1:
        print("INVALID INPUT")
        return False

    # check the id parts contents
    for i in range(8):
        if start_id[i] not in digits:
            print("INVALID INPUT")
            return False

    if last_digit not in digits:
        print("INVALID INPUT")
        return False

    return True


def cheackID(full_id):
    # This method get a full ID and return if it valid or not
    if not checkIDFormat(full_id):
        return False
    start_id, last_digit = full_id.split('-')
    flag = True
    sum = 0
    num = 0
    for i in range(8):
        if flag:
            num = int(start_id[i])
        else:
            num = 2*int(start_id[i])
            if num > 9:
                num = num%10 + (num//10)
        sum += num
        flag = not flag

    closestTenMultiple = 0

    while closestTenMultiple < sum:
        closestTenMultiple += 10

    return (closestTenMultiple - sum) == int(last_digit)


def main():
    full_id = "21233219-1"
    if cheackID(full_id):
        print("The ID: " + full_id + " is valid")
    else:
        print("The ID: " + full_id + " invalid")

if __name__ == "__main__":
    main()