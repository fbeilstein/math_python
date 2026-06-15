import math
import re

# =====================================================================
# STUDENT IMPLEMENTATION (Locality Sensitive Hashing & Bloom Filters)
# =====================================================================

def get_shingles(text, k=3): #contains solution
    """
    L1: Convert text into a set of k-word shingles.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    shingles = set()
    for i in range(len(words) - k + 1):
        shingle = tuple(words[i:i+k])
        shingles.add(shingle)
    return shingles

def jaccard_similarity(set1, set2): #contains solution
    """
    L2: Calculate Jaccard similarity between two sets.
    """
    if len(set1) == 0 and len(set2) == 0:
        return 0.0
    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection
    return intersection / union

def create_signature(shingles, hash_funcs): #contains solution
    """
    L3: Create a MinHash signature for a document.
    """
    if not shingles:
        return tuple(float('inf') for _ in hash_funcs)
        
    signature = []
    for hf in hash_funcs:
        min_val = min(hf(s) for s in shingles)
        signature.append(min_val)
        
    return tuple(signature)

def minhash_similarity(sig1, sig2): #contains solution
    """
    L4: Estimate Jaccard similarity by comparing two MinHash signatures.
    """
    if len(sig1) == 0:
        return 0.0
    matches = sum(1 for a, b in zip(sig1, sig2) if a == b)
    return matches / len(sig1)

def lsh_bloom_filter(signatures, num_bands): #contains solution
    """
    L5: The Modified Bloom Filter (LSH Bucketing).
    Divide signatures into bands and hash them into buckets.
    Return a dictionary mapping a bucket_id to a list of document indices.
    """
    buckets = {}
    if not signatures:
        return buckets
        
    sig_len = len(signatures[0])
    rows_per_band = sig_len // num_bands
    
    for doc_idx, sig in enumerate(signatures):
        for band_idx in range(num_bands):
            start_row = band_idx * rows_per_band
            end_row = start_row + rows_per_band
            band_tuple = tuple(sig[start_row:end_row])
            bucket_id = (band_idx, band_tuple)
            
            if bucket_id not in buckets:
                buckets[bucket_id] = []
            buckets[bucket_id].append(doc_idx)
            
    return buckets

def bloom_false_positive(n, m, k): #contains solution
    """
    L6: Standard Bloom Filter Probability.
    Calculate the false positive probability for a standard bloom filter.
    n: number of elements inserted
    m: number of bits in the filter
    k: number of hash functions
    Formula: (1 - e^(-k * n / m))^k
    """
    if m == 0: return 1.0
    return (1.0 - math.exp(-k * n / m))**k

def collision_probability(jaccard, bands, rows): #contains solution
    """
    L8: LSH Collision Probability.
    Calculate the probability that two documents with a given Jaccard similarity
    will collide in at least one band.
    """
    return 1.0 - (1.0 - jaccard**rows)**bands

def calculate_threshold(bands, rows): #contains solution
    """
    L8: Calculate the Jaccard similarity threshold where the collision probability is 50%.
    """
    return (1.0 - (0.5)**(1.0/bands))**(1.0/rows)
