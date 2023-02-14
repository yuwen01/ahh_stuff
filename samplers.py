import hashlib
import random
import pandas as pd 
import numpy as np
from util import *

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
    
    returns: sampler function for this discretized distribution
    '''
    assert(len(probs) == len(counts))
    if counts[-1] == -1:
        total_prob = sum(map(lambda x, y: x * y, probs[:-1], counts[:-1]))
        counts[-1] = int((1 - total_prob) // probs[-1])
    
    expanded_probs = []
    for i in range(len(probs)):
        expanded_probs.extend([probs[i]] * counts[i])

    expanded_probs[-1] += 1 - np.sum(expanded_probs)
    expanded_probs = np.array(expanded_probs)
    items = np.array([hashlib.sha256(bytes(i)).digest() for i in range(len(expanded_probs))])
    def sampler():
        item = np.random.choice(items, p=expanded_probs)
        return item

    return sampler

def distribution_sampler(fname):
    '''
    fname: csv file that contains distribution information
    returns: a sampler function for that distribution
    '''

    df = pd.read_csv(fname)

    names = df["name"]
    names = [hashlib.sha256(bytes(s, encoding='utf8')).digest() for s in names]
    freqs = df["freq"]
    def sampler():
        item = np.random.choice(names, p = freqs)
        return item

    return sampler


if __name__ == "__main__":
    # sampler = distribution_sampler('hash_freqs.csv')
    probs = [0.2, 0.1, 0.07, 0.016, 0.01, 0.005, 0.00001]
    counts = [1, 1, 1, 3, 5, 10, -1]
    sampler = discrete_sampler(probs, counts)
    b = sampler()
    print(b)
    b2 = bytes_to_bitarray(b)
    print(bitarray_to_bytes(b2))

