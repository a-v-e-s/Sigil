"""
factor.py: A function to find all factors of any given integer.
Is something like this not in the standard library somewhere???

Author: Jon David Tannehill
"""

import math, sys


def factors(n):
    combinations = []
    for x in range(1, n):
        if n % x == 0:
            if int(n/x) >= x:
                combinations.append((x, int(n/x)))
            else:
                break

    return combinations

if __name__ == '__main__':
    print(factors(int(sys.argv[1])))