import copy


def my_copy(obj, copy_mode):
    if copy_mode == "deep copy":
        return copy.deepcopy(obj)
    else:
        return copy.copy(obj)
