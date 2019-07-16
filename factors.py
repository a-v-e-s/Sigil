"""
factor.py: A function to find all factors of any given integer.
Is something like this not in the standard library somewhere???

Author: Jon David Tannehill
"""

import sys

def factors(n):
    divisors = []
    for x in range(1, n):
        if (n/2) < x:
            break
        if n % x == 0:
            divisors.append(x)

    return divisors

def factor_combinations(n):
    combinations = []
    for x in range(1, n):
        if n % x == 0:
            if int(n/x) >= x:
                combinations.append((x, int(n/x)))
            else:
                break

    return combinations

if __name__ == '__main__':
    print('Factors of ', sys.argv[1], ': ', factors(int(sys.argv[1])),
        sep='')
    print('Combinations of ', sys.argv[1], "'s factors: ",
        factor_combinations(int(sys.argv[1])), sep='')