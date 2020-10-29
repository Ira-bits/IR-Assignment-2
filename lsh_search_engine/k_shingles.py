import os
from hashlib import sha1
from .settings import SHINGLE_SIZE, DATASET_PATH


def create_shingles(document_data):
    """
    Takes in a single document/string sequence and returns it's shingles
    """
    shingles = set()
    hashed_shingles = set()
    for i in range(0, len(document_data) - SHINGLE_SIZE + 1):
        shingle = document_data[i : i + SHINGLE_SIZE]
        shingles.add(shingle)
        hashed_shingle = int(sha1(shingle.encode("utf-8")).hexdigest(), 16)
        hashed_shingles.add(hashed_shingle)
    return shingles, hashed_shingles


def create_shingles_dataset():
    """
    Returns a set of shingles and hashed shingles for all the documents in the corpus
    """
    print("Generating Shingles...")
    dir = os.listdir(DATASET_PATH)
    dir.sort()
    shingles = set()
    hashed_shingles = set()
    docs_len = len(dir)
    curr_doc = 1
    for document_name in dir:
        print(f"Parsing Document {curr_doc} out of {docs_len}", end="\r")
        with open(os.path.join(DATASET_PATH, document_name), "r") as document:
            document_data = document.read()
            doc_shingles, doc_hashed_shingles = create_shingles(document_data)
        shingles.update(doc_shingles)  # Take Union on the two sets
        hashed_shingles.update(doc_hashed_shingles)
    print("Done Generating Shingles!")
    return shingles, hashed_shingles


def create_matrix_row(shingles, document_data, single_doc=False):
    """
    Takes in shingles, document string and returns a row of shingle matrix for that document
    """
    row = []
    for shingle in shingles:
        if document_data.find(shingle) == -1:
            row.append(0)
        else:
            row.append(1)
    if single_doc:
        return [].append(row)
    return row


def create_shingle_matrix(shingles):
    """
    Takes in a set of shingles and returns a matrix Shingles x Documents, indicating the presence or absence of shingles in the documents.
    """
    print("Creating Shingle Matrix...")
    shingle_matrix = []
    dir = os.listdir(DATASET_PATH)
    dir.sort()
    docs_len = len(dir)
    curr_doc = 1
    for document_name in dir:
        print(f"Parsing Document {curr_doc} out of {docs_len}", end="\r")
        with open(os.path.join(DATASET_PATH, document_name), "r") as document:
            document_data = str(document.read())
            row = create_matrix_row(shingles, document_data)
            shingle_matrix.append(row)
    return shingle_matrix
