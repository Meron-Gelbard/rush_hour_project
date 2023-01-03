import itertools

a = itertools.cycle([i for i in range(10)])


print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
