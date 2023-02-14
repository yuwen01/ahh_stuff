from bucket import Bucket
from util import bytes_to_bitarray, bitarray_to_bytes
from samplers import discrete_sampler, distribution_sampler
import random
import hashlib

class Bitcounter_Simulator:
    def __init__(self, bitsize, sampler, m=1000, threshold=0.05):
        '''
        m - number of buckets
        sampler - function for sampling. It takes in no arguments, and returns a byte array 
            that can be represented in `bitsize` bits.  
        bitsize - number of bits per item
        threshold - percentage to be considered heavy hitter
        TODO: add k parameter for # of rows in the thing. 
        '''
        self.m = m
        self.bitsize = bitsize
        self.buckets = [Bucket(bitsize) for _ in range(m)]
        self.sampler = sampler
        self.threshold = threshold

    def _get_bucket(self, item):
        hash_result = hashlib.sha256(item).digest()
        return int.from_bytes(hash_result, "big") % self.m

    def populate(self, n):
        '''
        n: number of items to put into the data structure
        '''
        self.total_items = n
        for i in range(n):
            new_item = self.sampler()
            new_idx = self._get_bucket(new_item)
            new_item_bits = bytes_to_bitarray(new_item)
            self.buckets[new_idx].add(new_item_bits)
            if i % 1000 == 0:
                print(i)
            
    def reset(self):
        '''
        reset the buckets
        '''
        self.buckets = [Bucket(self.bitsize) for _ in range(self.m)]
        self.total_items = 0

    
    def recover(self):
        '''
        returns a list of the heavy hitters
        '''
        result = []
        for i, b in enumerate(self.buckets):
            if b.ct < self.threshold * self.total_items:
                continue
            else:
                hh = bitarray_to_bytes(b.recover())
                if i != self._get_bucket(hh): # Check to make sure recovered HH is
                    continue
                result.append(hh)
        
        return result

def discrete_sampler(probs, counts):
    '''
    probs: probability of a certain class of output. 
    counts: number of items in each probability bin. select -1 for the last count to autofill.

    ex: 
    probs = [0.2, 0.1]
    counts = [3, 4]
     
    then there are 3 objects that each appear with frequency 0.2,
        and 4 objects that each appear with frequency 0.1

    probs = [0.2, 0.1]
    counts = [3, -1]
    
    is equivalent
    '''
    assert(len(probs) == len(counts))
    if counts[-1] == -1:
        total_prob = sum(map(lambda x, y: x * y, probs[:-1], counts[:-1]))
        counts[-1] = int((1 - total_prob) // probs[-1])
    
    expanded_probs = []
    for i in range(len(probs)):
        expanded_probs.extend([probs[i]] * counts[i])
    

    items = [hashlib.sha256(bytes(i)).digest() for i in range(len(expanded_probs))]
    def sampler():
        item = random.choices(items, weights=expanded_probs)
        return bytes(item[0])

    return sampler
        



if __name__ == '__main__':
    probs = [0.1, 0.02, 0.01, 0.005, 0.0001]
    counts = [3, 10, 20, 40, -1]
    sampler = distribution_sampler('hash_freqs.csv')
    sim = Bitcounter_Simulator(hashlib.sha256().digest_size * 8, \
        sampler, \
        m = 1000)

    sim.populate(int(1e7))
    print(sim.recover())

    


                
        