import numpy as np

def LastPrimes(n, last_primes):
    p = []

    while last_primes != len(p):
        prime = True
        for j in range(2, int(math.sqrt(n) + 1)):
            if n % j == 0:
                prime = False
                break
        if prime == True:
            p.append(n)
        n -= 1

    return p


class BloomFilter:

    def __init__(self, m):
        self.filter = np.zeros(m)
        self.primes = LastPrimes(m, 100)

    def add_to_filter(self, index):
        if self.filter[index] == 0:
            self.filter[index] = 1

    def hash_function(self, passwords_list, p):
        values = []
        mod = self.primes[0]

        for password in passwords_list:
            value = ""
            last_c = str(ord(password[-1]))

            for i in range(int(last_c[-1]) + 10):
                value += str(ord(password[-i]))[-1]

            value = (int(value) * p + ord(password[0])) % mod
            add_to_filter(value)
