import math
from typing import List


def sieve_of_eratosthenes(n: int) -> List[int]:
    # Initialize primes
    primes = [True] * n
    primes = [True for _ in range(n + 1)]

    prime = 2
    while prime**2 <= n:
        if primes[prime]:
            for i in range(prime**2, n + 1, prime):
                primes[i] = False
        prime += 1

    return [index for index, value in enumerate(primes) if value]


def get_next_prime(n: int) -> int:
    break_condition = 2 * n - 2
    while True:
        if is_prime(n):
            return n
        n += 1
        if n == break_condition:
            # After Bertrands postulate, this should not happen.
            raise ValueError("No Prime Found!")


def is_prime(n: int) -> bool:
    for i in range(2, int(math.sqrt(n)) + 1):
        if (n % i) == 0:
            return False
    return True
