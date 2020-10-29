import math
import zlib
import settings


def lsh(sig):
    """
    Given a signature matrix sig, perfroms locality sensitive hashing by dividing sig into `b` bands 
    of `r` rows each. For each band, a hash function takes vectors of `r` integers and hashes them to 
    some large number of buckets (dict). Returns these buckets. The returned buckect dict contains
    a sub-bucket for each band. Each sub bucket maps as bucket_id -> {doc_ids...}
    """
    bucket = {}  # Contains sub buckets for each band
    num_buckets = settings.num_buckets
    num_bands = settings.num_bands
    force_collision_ratio = settings.force_collision_ratio
    rows_per_band = int(math.ceil(len(sig)/num_bands))
    d = len(sig[0])  # number of documents

    for curr_band in range(0, num_bands):  # For every band calculate the hash
        local_bucket = {}
        for doc_id in range(d):
            try:
                hash_vec = [sig[row][doc_id]
                            for row in range(curr_band*rows_per_band, (curr_band+1)*rows_per_band)]
            except:
                hash_vec = [sig[row][doc_id]
                            for row in range(curr_band*rows_per_band, (curr_band)*rows_per_band)]
            hash = zlib.crc32(bytes(hash_vec)) % num_buckets
            bucket_id = int(hash/force_collision_ratio)  # Force collisions

            if(local_bucket.get(bucket_id) == None):
                local_bucket[bucket_id] = set()

            local_bucket[bucket_id].add(doc_id)
        bucket[curr_band] = local_bucket
    return bucket
