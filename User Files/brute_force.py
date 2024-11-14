import math

def prime_checker(number):
    """
    Check if a number is prime.

    :param number: The integer to check.
    :return: True if the number is prime, False otherwise.
    """
    if number < 2:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True

def count_consecutive_primes(a, b):
    """
    Count consecutive primes produced by the quadratic formula n^2 + an + b.

    :param a: The coefficient of n in the formula.
    :param b: The constant term in the formula.
    :return: The number of consecutive primes generated, starting from n = 0.
    """
    n = 0
    while True:
        result = n**2 + a * n + b
        if not prime_checker(result):
            break
        n += 1
    return n

max_primes = 0
best_a = 0
best_b = 0

for a in range(-1000, 1001):
    for b in range(-1000, 1001):
        prime_count = count_consecutive_primes(a, b)
        if prime_count > max_primes:
            max_primes = prime_count
            best_a, best_b = a, b

print(f"The coefficients a and b that produce the longest sequence of prime numbers are: a = {best_a}, b = {best_b}")
print(f"The number of consecutive prime numbers produced is: {max_primes}")
print(f"The product of the coefficients a and b is: {best_a * best_b}")
