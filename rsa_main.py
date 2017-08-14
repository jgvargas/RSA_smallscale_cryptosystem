"""
Senior Project: RSA cryptosystem
Juan Vargas Jr.
August 18th

Goals: Encrypt and decrypt any message within text file. Scales prime numbers based off
       of message decimal value

Notes:
    - July 1st: Laid pscudo code for future implementation
    - July 8th: Helper functions are not currently initalized to work
    - July 12th: Encryption/decryption implemented
    - July 22nd: Binary exponentiation tested and correctly implemented
        - See function handle_exponent
    - July 30th: Prime selection algorithm
    - August 3rd: EEA implemented and working
    - August 10th: Primality troubles, fix incoming
                   Resovled by minimizing prime canidates without
    - August 12th:
        - Primality test working without digit length implementation
    - August 13th:
        - Primality test fully operational
        - find_prime() function now returns specific length prime numbers
    - August 14th:
        - Testing handle_exponent() function, not operative efficently enough
    - August 15th:
        - Implement input from file
        - Fix handle_exponent()

    ref:
        textbook: "Understanding Cryptography : A Textbook for Students and Practitioners" Christof Paar
        https://en.wikipedia.org/wiki/Modular_exponentiation
        https://en.wikipedia.org/wiki/Exponentiation_by_squaring
        https://docs.python.org/2/library/functions.html

"""

import random
from fractions import gcd
from rsa_functions import bit_list_to_string, string_to_bits, convert_to_bits,\
    seq_to_bits, pad_bits, bits_to_string, findPrime, extended_euclidean_algorithm,\
    handle_exponent, primalityTest, eulers_phi_function, encrypt, decrypt

# ----------------------------------------------------------------------
# Setup: Convert message to: ascii characters -> binary -> decimal value
# ----------------------------------------------------------------------
plaintext = raw_input('Write your message: ')

binary_array = string_to_bits(plaintext)
binary_string = bit_list_to_string(binary_array)
plaintext_dec = int(binary_string, 2)


print ("\nEncrypting message >> %s <<" % plaintext)

print ("Plaintext binary representation >> %s <<" % binary_string)

print ("Decimal representation >> %s <<\n" % plaintext_dec)


RSA_complete = False
while not RSA_complete:
    # ---------------------------------------------------------------------------
    # Key Generation: Select two prime numbers, totient, and encryption value 'e'
    # ---------------------------------------------------------------------------

    digit_size = len(str(plaintext_dec))

    validPrimes = False
    while not validPrimes:
        # Primes p and q should be about 512 bits or 64 digits
        p = findPrime(digit_size)
        q = findPrime(digit_size)
        n = p * q

        # Primes p and q are tested for being co-primes
        if gcd(p, q) == 1:
            validPrimes = True
        if (n-1) < plaintext_dec:
            # increase digit size by one? Maybe enough
            print("Plaintext decimal value is greater than n-1: ERROR")
            validPrimes = False

    phi_n = eulers_phi_function(p, q)

    """ Selecting e value, must be co-prime with phi_n
                           and within range {1,2...,phi(n)-1} """
    validE = False
    while not validE:
        e = 65537  # random.randint(3, phi_n-1)

        # Primes p and q are tested for being co-primes
        if gcd(phi_n, e) == 1:
            validE = True

    """ From e selection, with tests applied, we assume e has inverse d.
                   fine d by running EEA on value e """

    eea_results = extended_euclidean_algorithm(phi_n, e)
    d = eea_results[1]   # Assigns second value calculated by EEA to d
    if d < 0:            # Negative value d is a problem but can be undone
        d += phi_n

    line = "----------------------"
    print("%s\nKey Generation yields:" % line)
    print("p = %d" % p)
    print("q = %d" % q)
    print("n = %d" % n)
    print("Phi(n) = %d" % phi_n)
    print("e = %d" % e)
    print("d = %d\n" % d)

    # ---------------------------------
    # Encryption = x^e (mod n)
    # ---------------------------------

    #ciphertext = encrypt(plaintext_dec, e, n)
    ciphertext = pow(plaintext_dec, e, n)

    print ("Encrypted message is >> %s <<" % ciphertext)
    # ---------------------------
    # Decryption = y^d (mod n)
    # ---------------------------

    #plaintext_dec = decrypt(ciphertext, d, n)
    plaintext_dec = pow(ciphertext, d, n)

    RSA_complete = True  # indicates RSA has concluded

bitSeq = seq_to_bits(bin(plaintext_dec)[2:])  # [2:] is needed to get rid of 0b in front
paddedString = pad_bits(bitSeq, len(bitSeq) + (8 - (len(bitSeq) % 8)))  # Need to pad because conversion from dec to bin throws away MSB's
outputString = bits_to_string(paddedString)

print ("Decrypted message is >> %s <<" % outputString)
