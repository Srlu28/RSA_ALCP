import random

# Algorithm to generate large primes
# We are given a positive integer b which represents the number of bits the prime should be
# A positive integer n is represented with b bits if and only if 2^(b-1) <= n < 2^b
# We generate a random list of bits with the first and last bit being 1 (the first to be b bits and the last to be odd number)
# The rest of the bits are random
# This gives us a random odd number with the correct number of bits

# From the list of bits calculate the corresponding odd integer n
# Perform the Miller-Rabin primality test on n to see if it is a probable prime
# If it is, we are done, if it's not then repeat the process until a probable prime is discovered

# The miller rabin test performs like this:
#               -> If False is returned then it is False than n is prime
#               -> If True is returned then it is probably True that n is prime
#   - Step 1 of Miller-Rabin Primality Test: find n-1 = 2^k * m
#   - Step 2 Choose 'a' such that 1<a<n-1
#   - Step 3 Compute b_0 = a^m (mod n),....,b_i = b_{i-1}^2 (mod n)
#               -> b_0 = +1 Composite
#               -> b_0 = -1 Probably Prime

def miller_rabin(n,iter=40):
    """
    Algoritmo basado en el expuesto en el libro Understanding Cryptography - Paar & Pelzl chap 7.
    """
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Step 1
    k,m = 0,n-1
    while(m%2==0):
        k+=1
        m //=2

    # Step 2
    for _ in range(iter):
        a = random.randrange(2,n-1)
        x = pow(a,m,n)
        if (x != 1 and x != n-1):
            for _ in range(k-1):
                x = pow(x,2,n)
                if x == 1:
                    return False
            if x != n-1:
                return False

    return True
    

def random_odd_numer(bits):
    n = random.randint(2**(bits-1),2**bits-1)
    if n%2 == 0:
        n+=1
    return n

def generate_probable_prime(bits,iter=40):
    while True:
        n = random_odd_numer(bits)
        if miller_rabin(n,iter):
            return n
