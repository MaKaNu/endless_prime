import pytest
from endless_prime.calc import (
    get_next_prime,
    is_prime,
    sieve_of_eratosthenes,
)


class TestSieveOfEratosthenes:
    def test_typical_case(self):
        assert sieve_of_eratosthenes(10) == [0, 1, 2, 3, 5, 7]

    def test_small_numbers(self):
        assert sieve_of_eratosthenes(0) == [0]
        assert sieve_of_eratosthenes(1) == [0, 1]
        assert sieve_of_eratosthenes(2) == [0, 1, 2]
        assert sieve_of_eratosthenes(3) == [0, 1, 2, 3]

    def test_prime_limit(self):
        assert sieve_of_eratosthenes(13) == [0, 1, 2, 3, 5, 7, 11, 13]

    def test_non_prime_limit(self):
        assert sieve_of_eratosthenes(20) == [0, 1, 2, 3, 5, 7, 11, 13, 17, 19]

    def test_large_number(self):
        assert sieve_of_eratosthenes(100) == [
            0,
            1,
            2,
            3,
            5,
            7,
            11,
            13,
            17,
            19,
            23,
            29,
            31,
            37,
            41,
            43,
            47,
            53,
            59,
            61,
            67,
            71,
            73,
            79,
            83,
            89,
            97,
        ]

    def test_edge_cases(self):
        # Test for a prime number that is a perfect square
        assert sieve_of_eratosthenes(49) == [
            0,
            1,
            2,
            3,
            5,
            7,
            11,
            13,
            17,
            19,
            23,
            29,
            31,
            37,
            41,
            43,
            47,
        ]

        # Test for an even number that is not prime
        assert sieve_of_eratosthenes(50) == [
            0,
            1,
            2,
            3,
            5,
            7,
            11,
            13,
            17,
            19,
            23,
            29,
            31,
            37,
            41,
            43,
            47,
        ]

        # Test for the smallest odd non-prime number
        assert sieve_of_eratosthenes(9) == [0, 1, 2, 3, 5, 7]


class TestIsPrime:
    def test_simple_primes(self):
        assert not is_prime(1)
        assert is_prime(2)
        assert is_prime(3)
        assert not is_prime(4)

    def test_larger_primes(self):
        values = list(range(5, 100))
        results = [False] * 95
        indices = [
            0,
            2,
            6,
            8,
            12,
            14,
            18,
            24,
            26,
            32,
            36,
            38,
            42,
            48,
            54,
            56,
            62,
            66,
            68,
            74,
            78,
            84,
            92,
        ]
        results = [True if i in indices else x for i, x in enumerate(results)]
        for value, result in zip(values, results):
            assert is_prime(value) == result


class TestGetNextPrime:
    def test_next_prime_after_8(self):
        assert get_next_prime(8) == 11

    def test_next_prime_after_245(self):
        assert get_next_prime(245) == 251

    def test_next_prime_after_3987(self):
        assert get_next_prime(3987) == 3989

    def test_next_prime_after_409829331(self):
        assert get_next_prime(409829331) == 409829339
