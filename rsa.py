
import random
import math
import sys

############## Problem 1 a ##############
# Generate prime number of size n bits
def generatePrime(n, maxValue=float("inf")):
	# sample uniform number of n bits
	# use isPrimeMR() to test that the generated number is prime
    iters = 10 * 3 * n
    for i in xrange(iters):
        r = random.randint(0, min(2**n, maxValue))
        if isPrimeMR(r):
            return r
    raise 'Did not generate a prime in {} iterations.'.format(iters)

#get number p, test if it's prime using Miller-Rabin
def isPrimeMR(N, t=30):
    def _compositeCheck(a, r, u, N):
        x = pow(a, u, N)
        if x == 1 or x == N - 1:
            return True
        for i in xrange(r):
            if x == N - 1:
                return True
            x = pow(x, 2, N)
        return x == N - 1
    # ---------------------------------------------
    if N == 2:
        return True
    if N % 2 == 0:
        return False
    else:
        # now we can compute a u, r
        r = 0
        u = N - 1
        while not u % 2:
            u /= 2
            r += 1
        # and run our t iterations
    	for i in xrange(t):
    		a = random.randint(1, N - 1)
    		if not _compositeCheck(a, r, u, N):
    			return False
        return True

# primality test using the naive approach
def isPrimeNaive(p):
	for i in xrange(2, int(math.sqrt(p))+2):
		if p % i == 0:
			return False
	return True


#test for 10 small numbers, size n = 20 bits.
if len(sys.argv) > 1 and sys.argv[1] == '1.1':
    size = 20
    numPrimes = 10
    for _ in xrange(numPrimes):
        p = generatePrime(size)
        assert isPrimeNaive(p) == True
    print 'Successfully generated and validated {} primes of size {}.'.format(numPrimes, size)


############## Problem 1 b ##############
class RSA:
    # initialize RSA, generate e, d
    def __init__(self):
        self.gen()

	# Use generate_prime
    def gen(self):
		# security parameter
        self.n = 1024

		# Primes p and q
        self.p = generatePrime(self.n)
        self.q = generatePrime(self.n)

		# RSA modulus N = pq, totient_N = (p-1)(q-1)
        self.N = self.p * self.q
        self.totient_N = (self.p - 1) * (self.q - 1)

		# Public key e
        self.e = generatePrime(self.n * 2, maxValue = self.totient_N)

		# Secret key d
        self.d = self._modularInverse(self.e, self.totient_N)

    def trapdoor(self, M):
        return pow(M, self.e, self.N)

    def inverse(self, ciphertext):
        return pow(ciphertext, self.d, self.N)

    # Some internet code for modular inverse.
    def _modularInverse(self, a, m):
        def _extended_gcd(aa, bb):
            lastremainder, remainder = abs(aa), abs(bb)
            x, lastx, y, lasty = 0, 1, 1, 0
            while remainder:
                lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
                x, lastx = lastx - quotient * x, x
                y, lasty = lasty - quotient * y, y
            return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)
        g, x, y = _extended_gcd(a, m)
        if g != 1:
            raise ValueError
        return x % m

# test RSA, do it 10 times
rsa = RSA()
num = 50
print 'Finished initializing RSA.'

for i in xrange(num):
    M = random.randint(2**1023, 2**1024)
    c = rsa.trapdoor(M)
    assert c != M
    dM = rsa.inverse(c)
    assert dM == M

print 'Successfully inverted {} messages.'.format(num)
