import math
from collections import defaultdict

def check_prime(n):
    """
    Check if a number is prime using Miller-Rabin primality test
    """
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19]:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def find_primitive_roots(p):
    """
    Find all primitive roots modulo a prime p
    """
    if not check_prime(p):
        return []
    phi = p - 1
    factors = defaultdict(int)
    temp = phi
    while temp % 2 == 0:
        factors[2] += 1
        temp //= 2
    i = 3
    while i * i <= temp:
        while temp % i == 0:
            factors[i] += 1
            temp //= i
        i += 2
    if temp > 2:
        factors[temp] += 1
    for g in range(2, p):
        if all(pow(g, phi // f, p) != 1 for f in factors):
            return sorted([pow(g, k, p) for k in range(1, phi) if math.gcd(k, phi) == 1])
    return []

# System parameters
p = 467  # Prime number
g = 2    # Base/Generator
a = 153  # Alice's private key
m = 331  # Bob's message
k = 197  # Bob's random number

# 1. Verify prime and primitive root
roots = find_primitive_roots(p)
print(f"1. Is {p} a prime number? {check_prime(p)}")
print(f"2. Is {g} a primitive root modulo {p}? {g in roots}")
print(f"3. All primitive roots of {p}:\n{roots}")

# 2. Key exchange and encryption
A = pow(g, a, p)
print(f"\n4. Alice's public key (A = g^a mod p): {A}")

c1 = pow(g, k, p)
shared_secret = pow(A, k, p)
c2 = (m * shared_secret) % p
print(f"5. Bob encrypts message m = {m}:")
print(f"   Ciphertext (c1, c2) = ({c1}, {c2})")

# 3. Alice decrypts the message
s = pow(c1, a, p)
m_decrypted = (c2 * pow(s, p-2, p)) % p
print(f"\n6. Alice decrypts ciphertext:")
print(f"   Decrypted message = {m_decrypted}")

# Verification
if m == m_decrypted:
    print("\n7. Verification: Decryption successful!")
else:
    print("\n7. Verification: Decryption failed!")
