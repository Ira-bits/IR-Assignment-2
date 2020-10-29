import os
from hashlib import sha1

SHINGLE_SIZE = 9
CORPUS_PATH = "corpus"


def create_shingles():
    """
    Returns a set of shingles and hashed shingles for all the documents in the corpus
    """
    dir = os.listdir(CORPUS_PATH)
    dir.sort()
    shingles = set()
    hashed_shingles = set()
    for document_name in dir:
        with open(os.path.join(CORPUS_PATH, document_name), "r") as document:
            document_data = document.read()
            for i in range(0, len(document_data) - SHINGLE_SIZE + 1):
                shingle = document_data[i : i + SHINGLE_SIZE]
                shingles.add(shingle)
                hashed_shingle = int(sha1(shingle.encode("utf-8")).hexdigest(), 16)
                hashed_shingles.add(hashed_shingle)
    return shingles, hashed_shingles


def create_shingle_matrix(shingles):
    """
    Takes in a set of shingles and returns a matrix Shingles x Documents, indicating the presence or absence of shingles in the documents.
    """
    shingle_matrix = []
    dir = os.listdir(CORPUS_PATH)
    dir.sort()
    for document_name in dir:
        with open(os.path.join(CORPUS_PATH, document_name), "r") as document:
            document_data = str(document.read())
            row = []
            for shingle in shingles:
                if document_data.find(shingle) == -1:
                    row.append(0)
                else:
                    row.append(1)
            shingle_matrix.append(row)
    return shingle_matrix


if __name__ == "__main__":
    shingles, hashed_shingles = create_shingles()
    shingle_matrix = create_shingle_matrix(shingles)
    for row in shingle_matrix:
        print(row)
