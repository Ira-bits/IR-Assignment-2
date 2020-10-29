""" Package containing funcions to implement Locality Sensitive Hashing """
from .k_shingles import (
    create_shingles,
    create_shingles_dataset,
    create_matrix_row,
    create_shingle_matrix,
)
from .minhash import get_signature_matrix
from .lsh import lsh