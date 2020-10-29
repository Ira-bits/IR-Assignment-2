import random


def random_hash_funcs():
    """ Generates random linear hash functions a*x+b """
    hashfuncs = []
    for i in range(0, 100):
        pair = []
        for j in range(0, 2):
            pair.append(random.randint(1, 500))
        hashfuncs.append(tuple(pair))

    return hashfuncs


def get_signature_matrix(matrix):
    """
    Generates the similarity matrix of the document based on the technique of min-hashing

    Parameters:
    matrix: Matrix (shingles * documents) formed after the shingling process

    Returns:
    signature_matrix: signature
    """

    print("Generating Signature Matrix...")
    # Min-Hash functions are of the form a*x+b modulo 497
    min_hash_funcs = random_hash_funcs()

    # Initialize similarity matrix with very high values
    sim_matrix = []
    for i in range(100):
        row = []
        for j in range(len(matrix[0])):
            row.append(1000)
        sim_matrix.append(row)

    # Applying min-hash algorithm
    for i in range(len(matrix)):
        for j in range(100):
            a = min_hash_funcs[j][0]
            b = min_hash_funcs[j][1]
            hash_key = ((a * (i + 1)) + b) % 497
            for k in range(len(matrix[0])):
                if matrix[i][k] == 1:
                    if hash_key < sim_matrix[j][k]:
                        sim_matrix[j][k] = hash_key

    print("Done Creating Signature Matrix!")
    return sim_matrix
