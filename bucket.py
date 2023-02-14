import numpy as np
import hashlib
from util import *

class Bucket:
    def __init__(self, size):
        '''
        size - number of bit counters necessary
        '''
        self.size = size
        self.bitcounters = np.zeros((size), np.int32)
        self.ct = np.int32(0)
        
    def add(self, new_item):
        '''
        new_item - an `size` length nparray of bits.
        '''
        assert len(new_item)==self.size
        self.bitcounters += new_item
        self.ct += 1

    def recover(self): 
        result = np.zeros((self.size), np.int32)
        for i, v in enumerate(self.bitcounters):
            if v < self.ct >> 1:
                result[i] = 0
            else:
                result[i] = 1
        return result

def _hash(num):
    return hashlib.sha256(bytes(num)).digest()

if __name__ == '__main__':
    b = Bucket(hashlib.sha256().digest_size * 8)
    print(_hash(4))
    for _ in range(14):
        b.add(bytes_to_bitarray(_hash(4)))

    print(bitarray_to_bytes(b.recover()))