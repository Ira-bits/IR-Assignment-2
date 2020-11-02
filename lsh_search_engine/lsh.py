import math
import zlib
from .settings import NUM_BANDS, NUM_BUCKETS, FORCE_COLLISION_RATIO


def lsh(sig):
    """
    Given a signature matrix sig, perfroms locality sensitive hashing by dividing sig into `b` bands
    of `r` rows each. For each band, a hash function takes vectors of `r` integers and hashes them to
    some large number of buckets (dict). Returns these buckets. The returned buckect dict contains
    a sub-bucket for each band. Each sub bucket maps as bucket_id -> {doc_ids...}
    """

    print("Performing LSH...")
    bucket = {}  # Contains sub buckets for each band
    rows_per_band = int(math.ceil(len(sig) / NUM_BANDS))
    d = len(sig[0])  # number of documents

    for curr_band in range(0, NUM_BANDS):  # For every band calculate the hash
        print(f"Processing Band {curr_band} of {NUM_BANDS}", end="\r")
        local_bucket = {}
        for doc_id in range(d):
            try:
                hash_vec = [
                    sig[row][doc_id]
                    for row in range(
                        curr_band * rows_per_band, (curr_band + 1) * rows_per_band
                    )
                ]
            except:
                hash_vec = [
                    sig[row][doc_id]
                    for row in range(
                        curr_band * rows_per_band, (curr_band) * rows_per_band
                    )
                ]
            bucket_id = zlib.crc32(bytes(hash_vec)) % NUM_BUCKETS
            # bucket_id = int(hash / FORCE_COLLISION_RATIO)  # Force collisions

            if local_bucket.get(bucket_id) == None:
                local_bucket[bucket_id] = set()

            local_bucket[bucket_id].add(doc_id)
        bucket[curr_band] = local_bucket

    print("Done with LSH!")
    return bucket
