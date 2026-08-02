import gudhi
import gudhi.wasserstein
import numpy as np

def compute_h1_diagram(point_cloud, max_edge_length=10.0): #contains solution
    """
    Given a point cloud (N x 2 numpy array), compute its persistence diagram.
    
    Tasks:
    1. Initialize a gudhi.RipsComplex with the point cloud and max_edge_length.
    2. Create a simplex tree up to dimension 2.
    3. Compute persistence on the tree.
    4. Filter the persistence intervals to return ONLY dimension 1 (H_1) intervals.
    
    Returns:
        A list of [birth, death] pairs for all H_1 features.
        (If no H_1 features exist, return an empty list or array).
    """
    
    # 1. Initialize Rips Complex
    rips = gudhi.RipsComplex(points=point_cloud, max_edge_length=max_edge_length)
    
    # 2. Create Simplex Tree
    st = rips.create_simplex_tree(max_dimension=2)
    
    # 3. Compute Persistence
    st.persistence()
    
    # 4. Filter for H1
    h1_intervals = []
    # Note: st.persistence() returns tuples of (dimension, (birth, death))
    for dim, (birth, death) in st.persistence():
        if dim == 1:
            h1_intervals.append([birth, death])
            
    return np.array(h1_intervals) if len(h1_intervals) > 0 else np.empty((0, 2))


def classify_shape(noisy_diag, reference_diags): #contains solution
    """
    Given an H1 persistence diagram of a noisy shape, determine which of the 
    reference shapes it most closely resembles.
    
    Parameters:
    - noisy_diag: A list or array of [birth, death] intervals for the noisy shape.
    - reference_diags: A dictionary of { "label": diag_array } for the reference shapes.
    
    Task:
    Iterate over the reference_diags. Use gudhi.wasserstein.wasserstein_distance 
    (with order=1, internal_p=2, matching=False) to compute the distance from 
    noisy_diag to each reference. 
    
    Returns:
        The string label (e.g., "circle", "figure8", "cluster") of the reference 
        diagram that yields the minimum Wasserstein distance.
    """
    
    # If the noisy diagram is empty, provide a dummy point so wasserstein doesn't crash, 
    # or handle it gracefully if gudhi supports empty diagrams against non-empty ones.
    # Gudhi wasserstein_distance expects at least empty lists, but sometimes np.empty((0,2)) works best.
    if len(noisy_diag) == 0:
        noisy_diag = np.empty((0,2))
        
    min_dist = float('inf')
    best_label = None
    
    for label, ref_diag in reference_diags.items():
        if len(ref_diag) == 0:
            ref_diag = np.empty((0,2))
            
        dist = gudhi.wasserstein.wasserstein_distance(
            noisy_diag, 
            ref_diag,
            order=1,
            internal_p=2,
            matching=False
        )
        
        if dist < min_dist:
            min_dist = dist
            best_label = label
            
    return best_label
