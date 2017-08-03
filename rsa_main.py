"""
Senior Project: RSA cryptosystem
Juan Vargas
August 18th

Goals: Given different values, which

Notes:
    - Jul 8th: Helper functions are not currently initalized to work
    - Jul 12th: Encyption/decryption implemented
    - Jul 22nd: Binary exponentiation tested and correctly implemented
        - See function handle_exponent
    - July 30th: Prime selection algorithm

"""

import math
from fractions import gcd
from rsa_functions import bit_list_to_string, string_to_bits, seq_to_bits, pad_bits,\
    bits_to_string, findPrime, extended_euclidean_algorithm, handle_exponent,\
    primalityTest, eulers_phi_function, encrypt, decrypt

# ------------------------------------
# Setup: Convert ascii characters into binary, join
# -------------------------------------
plaintext = raw_input('Write your message: ')

binary_array = string_to_bits(plaintext)
binary_string = bit_list_to_string(binary_array)
plaintext_dec = int(binary_string, 2)


#numberOutput = int(bit_list_to_string(string_to_bits(inputString)),2)

#bitSeq = seq_to_bits(bin(numberOutput)[2:])  # [2:] is needed to get rid of 0b in front
#paddedString = pad_bits(bitSeq, len(bitSeq) + (8 - (len(bitSeq) % 8)))  # Need to pad because conversion from dec to bin throws away MSB's
#outputString = bits_to_string(paddedString)  # attack at dawn

#ciphertext = bitSeq

print ("\nEncrypting message >> %s <<\n" % plaintext)

print "Plaintext binary representation >> %s <<\n" % binary_string

print ("Decimal representation >> %s <<\n" % plaintext_dec)

# ------------------------------------------------------------------
# Key Generation: Select two prime numbers, totient, and encryption value 'e'
# ------------------------------------------------------------------

validPrimes = False
while not validPrimes:
    # Select primes using Fermat's Primality Test, pg 189
    # Primes p and q should be about 512 bits long
    p = 11  # findPrime()
    q = 13  # findPrime()

    # Primes p and q are tested for being co-primes
    if gcd(p, q) == 1:
        validPrimes = True

# Since gcd(p,q) = 1, safe to continue
n = p * q

phi_n = eulers_phi_function(p, q)


""" Selecting e value, must be co-prime with phi_n
                       and within range {1,2...,phi(n)-1} """
validE = False
while not validE:
    # Select primes using Fermat's Primality Test, pg 189
    e = 65537  # = findPrime()

    # Primes p and q are tested for being co-primes
    if gcd(phi_n, e) == 1:
        validE = True

#   ______________________________
# Encryption


ciphertext = encrypt(plaintext_dec, e, n)

print ("Encrypted message is >> %s <<\n" % ciphertext)
#   ______________________________
# Decryption


