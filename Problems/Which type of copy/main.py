import copy


def detect_copy():
    obj = [[1, 2], [3, 4]]
    if id(obj[0]) == id(copying_machine(obj)[0]):
        return "shallow copy"
    else:
        return "deep copy"
