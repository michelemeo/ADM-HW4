import numpy as np
import math


# given a number "n", this function calculates the first "last_primes" prime numbers smaller and closer to "n"
# and stores them in a list
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
    
    # the creation of a BloomFilter object defines an array of zeros of chosen size "m", the filter;
    # then the prime numbers next to "m" are automatically calculated and an empty list for duplicates is created
    def __init__(self, m):
        self.filter = np.zeros(m)
        self.primes = LastPrimes(m, 100)
        self.duplicates = []

    
    # switch the value of the indexes calculated with the hash functions from 0 to 1
    def add_to_filter(self, hash_values):
        self.filter[hash_values] = 1

        
    # the hash function is well explained in the main.ipnyb
    def hash_function(self, password, multiplier, n_char):
        mod = self.primes[0]

        value = ""
        c = str(ord(password[-1-n_char]))

        for i in range(int(c[-1]) + 10):
            value += str(ord(password[-i]))[-1]

        return (int(value) * multiplier + ord(password[n_char])) % mod

    
    # return a list of the hash values of the input password list,
    # useful for testing the uniformity of their distribution
    def testing_hash_function(self, passwords_list):
        values = []

        for password in passwords_list:
            hash_value = self.hash_function(password, self.primes[5], 0)
            values.append(hash_value)

        return values


    # the function used to apply different hash functions: as mentioned in main.ipynb, 
    # the parameters for which the functions differ are the character index, here "k",
    # and the prime multiplier number, here "self.primes [p]"
    def multi_hash_functions(self, passwords_list, n_functions):

        for password in passwords_list:
            values = []
            p = 5

            for k in range(n_functions):
                hash_value = self.hash_function(password, self.primes[p], k)
                values.append(hash_value)
                p += 15

            self.add_to_filter(values)


    # to check if the set of "hash_values" is already contained in the filter, it is enough
    # to sum the filter values contained in those "hash_values" indexes: if their sum is equal
    # to the number of hash functions, the element is a duplicate        
    def hash_values_detector(self, hash_values, n_functions):

        if np.sum(self.filter[hash_values]) == n_functions:
            return 1
        else:
            return 0


    # this function recycles the functions seen above to check for duplicates of an entire list of passwords;
    # if a duplicate is found, it stores this in a list
    def hash_searching(self, new_passwords, n_functions):
        positive_cases = 0

        for password in new_passwords:
            values = []
            p = 5

            for k in range(n_functions):
                hash_value = self.hash_function(password, self.primes[p], k)
                values.append(hash_value)
                p += 15

            if self.hash_values_detector(values, n_functions) == 1:
                positive_cases += 1
                self.duplicates.append(password)

        return positive_cases