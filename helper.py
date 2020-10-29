""" Contains helper classes/functions for searching results in index """

import lsh_search_engine
import pickle
import sys
from pathlib import Path
from collections import OrderedDict


class LRUCache:
    """ Class to implement LRU Cache """

    def __init__(self, capacity: int):
        """ Initializes an Ordered Dictionary and cache capacity """
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        """
        Returns the value of the key that is queried in O(1) and return -1 if the key
        is not found in dict / cache. Moves the key to the end to mark that it
        was recently used.
        """
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: int, value: int) -> None:
        """
        Adds/Updates the key by conventional methods. Moves the key to the end to mark
        that it was recently used. Checks whether the length of our ordered dictionary
        has exceeded the cache capacity, If so then removes the first key (least recently used)
        """
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


def perform_lsh():
    """
    Uses LSH Search Engine Package functions to perform LSH on given dataset
    Shingles -> Minhashing -> LSH
    """
    # Create Shingle Matrix
    shingles, hashed_shingles = lsh_search_engine.create_shingles_dataset()
    shingle_matrix = lsh_search_engine.create_shingle_matrix(shingles)

    # Create Signature Matrix by Minhashing
    signature_matrix = lsh_search_engine.get_signature_matrix(shingle_matrix)

    # Perform Locality Sensitive Hashing
    lsh_search_engine.lsh(signature_matrix)
