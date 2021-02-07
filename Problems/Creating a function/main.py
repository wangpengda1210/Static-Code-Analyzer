import math


# Modify this function in the shell and copy the new version here
def my_sqrt(value):
    if type(value) is str:
        return "The string should be converted into a numeric data type"
    if type(value) is not int and type(value) is not float:
        return None
    else:
        return math.sqrt(value)
