import random

BITS = ('0', '1')
ASCII_BITS = 8

# -------------------------------------------------
#   Plaintext decomposition/recovery functions
# -------------------------------------------------


def bit_list_to_string(b):
    #   converts list of {0, 1}* to string
    return ''.join([BITS[e] for e in b])


def seq_to_bits(seq):
    return [0 if b == '0' else 1 for b in seq]


def pad_bits(bits, pad):
    """pads seq with leading 0s up to length pad"""
    assert len(bits) <= pad
    return [0] * (pad - len(bits)) + bits


def convert_to_bits(n):
    """converts an integer `n` to bit array"""
    result = []
    if n == 0:
        return [0]
    while n > 0:
        result = [(n % 2)] + result
        n = n / 2
    return result


def string_to_bits(s):
    def chr_to_bit(c):
        return pad_bits(convert_to_bits(ord(c)), ASCII_BITS)
    return [b for group in
            map(chr_to_bit, s)
            for b in group]


def bits_to_char(b):
    assert len(b) == ASCII_BITS
    value = 0
    for e in b:
        value = (value * 2) + e
    return chr(value)


def list_to_string(p):
    return ''.join(p)


def bits_to_string(b):
    return ''.join([bits_to_char(b[i:i + ASCII_BITS])
        for i in range(0, len(b), ASCII_BITS)])


# -----------------------------------------------------
#   Encryption/Decryption functions w/ helper functions
# -----------------------------------------------------


def handle_exponent(base, exp):
    """Scan bits from left to right
       In every iteration, the current result is squared
       If the scanned exponent bit has the value 1, a
       multiplication of the current result by x is executed following the squaring """

    new_base = 1

    if exp < 0:  # e value is negative
        base = 1 / base
        exp = - exp

    if exp == 0:  # e value is zero
        return 1

    while exp > 1:
        if exp % 2 == 0:  # If e value is even
            base = base * base
            exp = exp / 2

        else:
            new_base = base * new_base
            base = base * base
            exp = (exp - 1) / 2

    return base * new_base


def eulers_phi_function(p, q):
    a = p - 1
    b = q - 1

    phi = a * b
    return phi


def extended_euclidean_algorithm(x, y):
    """
       Term "old" referring to one iteration previous to current
       as in: s_{-1}, s,..
    """
    s = 0
    old_s = 1
    t = 1
    old_t = 0
    r = y
    old_r = x

    while r != 0:
        q = old_r // r
        (old_r, r) = (r, old_r - q * r)
        (old_s, s) = (s, old_s - q * s)
        (old_t, t) = (t, old_t - q * t)
        pass

    return old_s, old_t


def findPrime(digits):
    """
        Generates a prime based off of the size needed
    """
    num = 1
    lower = 10 ** (digits - 1)
    upper = 10 ** digits - 1

    valid = False
    while not valid:
        # generate a large number from desired length {lower, lower+1,..upper }
        num = random.randint(lower, upper)
        # print("Number tested is: %d" % num)

        if is_prime(num):
            print("Found a PRIME:\n%d" % num)
            valid = True
        else:
            pass

    return num


def is_prime(n):
    """
        Prime numbers are odd, except 2
        prime cannot be less than 2
        A prime has no factors other than 1 and itself
    """
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
                    101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193,
                    197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307,
                    311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421,
                    431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547,
                    557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
                    661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
                    809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929,
                    937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    if n < 2:
        return False

    if n in small_primes:
        return True

    for prime in small_primes:
        if n % prime == 0:
            return False

    return primalityTest(n)


def primalityTest(n):
    """" Miller-Tabin Primality test
         a^(2^s) = a^r =/ 1 (mod n)
         s will be divided until odd, acting for value 'q' = s
         'v' will take the place of a^q

         Using: s, t, a, v, i

         NIST FIPS 186-4, Appendix C, Table C.3, minimum number of
         rounds of M-R testing

         - p, q bitsize: 512; rounds: 7
         - p, q bitsize: 1024; rounds: 4
         - p, q bitsize: 1536; rounds: 3
        From: page 71 http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf
    """
    s = n - 1
    t = 0
    i = 0
    v = 0

    if n % 2 == 0:
        return False

    while s % 2 == 0:
        s = s/2
        t += 1

    for trials in range(4):
        """" Select and random a = {1 , 3, ....n-1} """
        a = random.randrange(1, n - 1)
        v = pow(a, s, n)
        if v != 1:
            i = 0
        while v != (n - 1):
            if i == t - 1:
                return False
            else:
                i += 1
                v = (v ** 2) % n
    return True


def encrypt(x, e, n):  # y = x^e (mod n)

    new_x = handle_exponent(x, e)

    return new_x % n


def decrypt(y, d, n):   # Function: x = y^d (mod n) """

    new_y = handle_exponent(y, d)
    x = new_y % n

    return x

