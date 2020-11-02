""" Contains helper classes/functions for searching results in index """

import lsh_search_engine
import pickle
import os
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


def get_data_for_docId(docId):
    """ Given a docId returns the species type and dna sequence """
    dir = os.listdir(lsh_search_engine.DATASET_PATH)
    dir.sort()
    doc_name = dir[docId]
    document = open(lsh_search_engine.DATASET_PATH + "/" + doc_name, "r")
    dna_seq = document.read()
    return doc_name, dna_seq


def process_query(query):
    """
    Takes in a `query` string, returns the `buckets` formed by performing LSH on it.
    """
    # Create Shingle Matrix
    file_obj = open("shingles.pkl", "rb")
    shingles = pickle.load(
        file_obj
    )  # Assuming that shingles in query is a subset of shingles in entire dataset
    file_obj = open("shingle_id.pkl", "rb")
    shingles_dict = pickle.load(file_obj)
    shingle_matrix = lsh_search_engine.create_matrix_query(
        shingles, shingles_dict, query
    )

    # Create Signature Matrix by Minhashing
    signature_matrix = lsh_search_engine.get_signature_matrix(shingle_matrix)

    # Perform Locality Sensitive Hashing
    query_buckets = lsh_search_engine.lsh(signature_matrix)

    return query_buckets


def perform_lsh():
    """
    Uses LSH Search Engine Package functions to perform LSH on given dataset
    Shingles -> Minhashing -> LSH
    """
    # Create Shingle Matrix
    shingles = lsh_search_engine.create_shingles_dataset()
    shingle_matrix = lsh_search_engine.create_shingle_matrix(shingles)

    # Create Signature Matrix by Minhashing
    signature_matrix = lsh_search_engine.get_signature_matrix(shingle_matrix)

    # Perform Locality Sensitive Hashing
    docs_buckets = lsh_search_engine.lsh(signature_matrix)
    return docs_buckets


def find_similar_docs(query_buckets, docs_buckets):
    """
    Given the `docs_buckets` and the buckets `query_buckets` formed by the query
    finds all the similar documents to the ones in `query_buckets` in `docs_buckets`.
    """
    similar_docs = set()

    for q_band_key in query_buckets.keys():
        for q_bucket_idx, q_bucket_docs in query_buckets[q_band_key].items():
            if q_bucket_docs:
                if (
                    q_band_key in docs_buckets
                    and q_bucket_idx in docs_buckets[q_band_key]
                ):
                    similar_docs.update(docs_buckets[q_band_key][q_bucket_idx])
    return similar_docs


# Uncomment to test find_similar_docs
# qb = {
#     1: {1: [0], 3: [0]},
#     2: {4: [0]},
# }

# db = {
#     1: {1: [0, 1, 2], 2: [3, 4]},
#     2: {4: [6]}
# }
# print(find_similar_docs(qb, db))
