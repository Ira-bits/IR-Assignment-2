import os
import pickle
from hashlib import sha1
from .settings import SHINGLE_SIZE, DATASET_PATH


def create_shingles(document_data):
    """
    Takes in a single document/string sequence and returns it's shingles
    """
    shingles = set()
    for i in range(0, len(document_data) - SHINGLE_SIZE + 1):
        shingle = document_data[i : i + SHINGLE_SIZE]
        shingles.add(shingle)
    return shingles


def create_shingles_dataset():
    """
    Returns a set of shingles for all the documents in the dataset
    """
    print("Generating Shingles...")
    dir = os.listdir(DATASET_PATH)
    dir.sort()
    shingles = set()
    docs_len = len(dir)
    curr_doc = 1
    for document_name in dir:
        print(f"Parsing Document {curr_doc} out of {docs_len}", end="\r")
        curr_doc += 1
        with open(os.path.join(DATASET_PATH, document_name), "r") as document:
            document_data = document.read()
            doc_shingles = create_shingles(document_data)
        shingles.update(doc_shingles)  # Take Union on the two sets

    # Storing shingles in file
    file_obj = open("shingles.pkl", "wb")
    pickle.dump(shingles, file_obj)

    print("Done Generating Shingles!")
    return shingles


def create_matrix_query(shingles, shingles_dict, document_data):
    """
    Takes in shingles, query string and returns the shingle matrix for the query
    """
    query_shingles = set()
    for i in range(0, len(document_data) - SHINGLE_SIZE + 1):
        shingle = document_data[i : i + SHINGLE_SIZE]
        query_shingles.add(shingles_dict[shingle])  # Store shingle id in the set

    # Convert set to a list
    row = []
    for shingle_id in query_shingles:
        row.append(shingle_id)
    row.sort()

    # Generate Matrix
    matrix = []
    matrix.append(row)
    return matrix


def create_shingle_matrix(shingles):
    """
    Takes in a set of shingles and returns a matrix containing the shingles present in each document
    """
    print("Creating Shingle Matrix...")
    shingle_matrix = []
    shingles_dict = {}

    # Assign id to each shingle
    shingle_id = 0
    for shingle in shingles:
        shingles_dict[shingle] = shingle_id
        shingle_id += 1

    # Store shingle ids
    file_obj = open("shingle_id.pkl", "wb")
    pickle.dump(shingles_dict, file_obj)

    dir = os.listdir(DATASET_PATH)
    dir.sort()  # doc_id is taken as the index in the sorted doc_list
    docs_len = len(dir)
    curr_doc = 1
    for document_name in dir:
        print(f"Processing Document {curr_doc} out of {docs_len}", end="\r")
        curr_doc += 1
        with open(os.path.join(DATASET_PATH, document_name), "r") as document:
            document_data = str(document.read())
            row = []
            doc_shingles = set()
            for i in range(0, len(document_data) - SHINGLE_SIZE + 1):
                shingle = document_data[i : i + SHINGLE_SIZE]
                doc_shingles.add(shingles_dict[shingle])  # Store shingle id in the set
            # Convert set to a list
            for shingle_id in doc_shingles:
                row.append(shingle_id)
            row.sort()
            shingle_matrix.append(row)
    print("Done Generating Shingle Matrix!")
    return shingle_matrix
