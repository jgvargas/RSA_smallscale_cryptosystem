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


# -------------------------------------------------
#   Encryption/Decryption functions w/ helper functions
# -------------------------------------------------


def handle_exponent(x, exp):
    """Scan bits from left to right
       In every iteration, the current result is squared
       If the scanned exponent bit has the value 1, a
       multiplication of the current result by x is executed following the squaring """

    new_x = 1

    if exp < 0:  # e value is negative
        x = 1 / x
        exp = - exp

    if exp == 0:  # e value is zero
        exp = 1

    while exp > 1:
        if exp % 2 == 0:  # If e value is even
            x = x * x
            exp = exp / 2

        else:
            new_x = x * new_x
            x = x * x
            exp = (exp - 1) / 2

    return x * new_x


def eulers_phi_function(p, q):
    a = p - 1
    b = q - 1

    phi = a * b
    return phi

def extended_euclidean_algorithm(x, y):   # NOTE: The gcd is in the standard library "from fractions import gcd"
    # Check to see if the greatest common division is 1

    # X must be greater than Y, if not, switch
    if x < y:
        temp = x
        x = y
        y = temp

    while True:
        pass

    return True


def findPrime():

    return 0


def primalityTest():
    # WHich is better: Fermat's Theorem or Miller-Tabin Primality test?

    return True


def encrypt(x, e, n):  # y = x^e (mod n)

    new_x = handle_exponent(x, e)
    y = new_x % n

    return y


def decrypt(x):
    pass