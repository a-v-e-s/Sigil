"""
fibonacci.py:

fibonacci.make_fibonacci(num, include_F0=True) returns a series of the first num fibonacci numbers, including 0 by default.
0 can be excluded by supplying include_F0=False as the second argument.

fibonacci.is_fibonacci(num, range_=1000, include_F0=True) returns True if num is in the first 1000 fibonacci numbers.
If num is greater than the 1000th value, returns None, otherwise returns False.
0 can be excluded by supplying include_F0=False as an argument.
The number of fibonacci numbers to test against can be changed by supplying a different number as the range_ argument.

fibonacci.nth_fibonacci(num, range_=1000, include_F0=True) returns index n, where num is the nth fibonacci number.
Returns None if num is not a fibonacci number.
To compute indexes for numbers > the 1000th fibonacci number, adjust the range_ argument.
0 can be excluded by supplying include_F0=False as an argument.

If run as a standalone module, the first argument after the module name determines the function to be run:
"make" runs make_fibonacci
"is" runs is_fibonacci
"nth" runs nth_fibonacci
The second argument after the module name will be entered as the argument "num"
The range_ and include_F0 arguments cannot be changed from their default values when used in this way.
"""

from sys import argv


def make_fibonacci(num, include_F0=True):
    if include_F0:
        sequence = [0, 1]
    else:
        sequence = [1, 1]

    for x in range(3, num+1):
        sequence.append(sequence[(len(sequence)-2)] + sequence[(len(sequence)-1)])

    return sequence


def is_fibonacci(num, range_=1000, include_F0=True):
    sequence = make_fibonacci(range_, include_F0)
    if num > sequence[-1]:
        print(str(num) + ' is out of the range of the first ' + str(range_) + ' fibonacci numbers.')
        print('Try again with a higher range or reconsider whether the calculation you are requesting is reasonable.')
        return None
    elif num in sequence:
        print(str(num) + ' is a fibonacci number.')
        return True
    else:
        print(str(num) + ' is not a fibonacci number.')
        return False


def nth_fibonacci(num, range_=1000, include_F0=True):
    sequence = make_fibonacci(range_, include_F0)
    if num > sequence[-1]:
        print(str(num) + ' is out of the range of the first ' + str(range_) + ' fibonacci numbers.')
        print('Try again with a higher range or reconsider whether the calculation you are requesting is reasonable.')
        return None
    try:
        return sequence.index(num)
    except ValueError:
        print(str(num) + ' is not a fibonacci number')
        return None


if __name__ == '__main__':
    if argv[1] == 'make':
        print(str(make_fibonacci(int(argv[2]))).strip('[]'))
    elif argv[1] == 'is':
        is_fibonacci(int(argv[2]))
    elif argv[1] == 'nth':
        print(nth_fibonacci(int(argv[2])))