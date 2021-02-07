# create your dictionary here
import collections.abc

objects_dict = {}
for o in objects:
    if isinstance(o, collections.abc.Hashable):
        objects_dict[o] = hash(o)
