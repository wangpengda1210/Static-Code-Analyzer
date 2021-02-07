# the object_list has already been defined
import collections.abc
# write your code here
hash_dict = collections.defaultdict(int)
for o in object_list:
    if isinstance(o, collections.abc.Hashable):
        hash_dict[hash(o)] += 1

count = 0
for _, value in hash_dict.items():
    if value > 1:
        count += value

print(count)
