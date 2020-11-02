import random
from .settings import MOD, HASH_NUM


def random_hash_funcs():
    """ Generates random linear hash functions a*x+b """
    hashfuncs = []
    # Assign a seed to get same random numbers for query and dataset
    random.seed(10)
    for _i in range(0, 100):
        pair = []
        for _j in range(0, 2):
            pair.append(random.randint(1, 500))
        hashfuncs.append(tuple(pair))

    return hashfuncs


def get_signature_matrix(matrix):
    """
    Generates the similarity matrix of the document based on the technique of min-hashing

    Parameters:
    matrix: Matrix (documents * shingle_id) formed after the shingling process

    Returns:
    signature_matrix: signature
    """

    print("Generating Signature Matrix...")

    # Min-Hash functions are of the form a*x+b modulo MOD
    min_hash_funcs = random_hash_funcs()  # Generate hash function random constants
    num_docs = len(matrix)

    # Initializing signature matrix
    sig_matrix = []
    for i in range(HASH_NUM):
        row = []
        for j in range(num_docs):
            row.append(MOD)  # Assigning a value for comparison
        sig_matrix.append(row)  # Taking hash_fn as row and doc as column

    # Applying min-hash algorithm
    for i in range(len(matrix)):
        print(f"Processing Row {i} out of {len(matrix)}", end="\r")
        for j in range(100):
            a = min_hash_funcs[j][0]
            b = min_hash_funcs[j][1]
            for k in matrix[i]:
                hash_key = ((a * (k + 1)) + b) % MOD
                if hash_key < sig_matrix[j][i]:
                    sig_matrix[j][i] = hash_key

    print("Done Creating Signature Matrix!")
    return sig_matrix
