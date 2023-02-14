from bitarray import bitarray
import numpy as np

def bytes_to_bitarray(arr):
    '''
    arr - bytes
    returns the equivalent numpy bit array
    '''
    a = bitarray()
    a.frombytes(arr)
    return np.array(list(a))
    

def bitarray_to_bytes(arr):
    '''
    arr - numpy bit array
    returns the equivalent bytes. Pads with zeroes at the end? 
        In practice, padding shouldn't be necessary.
    '''
    return bytes(np.packbits(arr))

if __name__ == "__main__":
    arr = b"\x03\x01\x02\xff"
    bits = bytes_to_bitarray(arr)
    print(bits)
    arr2 = bitarray_to_bytes(bits)
    print(arr2)