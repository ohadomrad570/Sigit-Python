"""
By Ohad Omrad
Python and Git
"""

def compressString(string):
    # This method get a string and compress it:
    #       each char will be present by the char itself and the number of times it has appear in a row
    # example: "aaabb" -> "a3b2"

    result = ""
    i = 0

    while i < len(string):
        ch = string[i]
        count = 1
        i+=1
        while i < len(string) and string[i] == ch:
            count +=1
            i+=1
        result = result + str(ch) + str(count)
    return result


def main():
    string = "abcaadddcc"
    print("compressString(" + string + ") = " + compressString(string))

if __name__ == "__main__":
    main()