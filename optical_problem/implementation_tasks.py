import numpy as np

# =============================================================================
#  STUDENT IMPLEMENTATION (ASSIGNMENTS 1-4)
# =============================================================================

CONST_EPSILON = 0 #1e-5

def z_cross(v,u):
    return v[0] * u[1] - u[0] * v[1]


def intersect_line_infinite(ray_origin, ray_dir, p1, p2): #contains solution
    v = p2 - p1
    denom = z_cross(v, ray_dir)
    if abs(denom) <= CONST_EPSILON: 
        return None
    t = z_cross(ray_origin - p1, v) / denom
    if t <= 0:
        return None
    return ray_origin + t * ray_dir
    

def intersect_segment(ray_origin, ray_dir, p1, p2): #contains solution
    # 1. Get the intersection point with the infinite line
    intersect_p = intersect_line_infinite(ray_origin, ray_dir, p1, p2)
    if intersect_p is None:
        return None
    
    # 2. Calculate the segment parameter 'u'
    # u = (P - P1) · (P2 - P1) / |P2 - P1|^2
    v = p2 - p1
    u = np.dot(intersect_p - p1, v) / np.dot(v, v)
    
    # 3. Boundary and Direction Checks
    # Check if point is on segment (0 <= u <= 1) 
    # AND in front of the ray (dot product with direction > 0)
    if 0 <= u <= 1: 
        return intersect_p
        
    return None


def intersect_circle(ray_origin, ray_dir, center, radius): #contains solution
    OC = ray_origin - center
    b = 2 * np.dot(ray_dir, OC)
    c = np.dot(OC, OC) - radius**2
    discriminant = b**2 - 4*c
    
    if discriminant < 0: 
        return [] # Return empty list
    
    sqrt_d = np.sqrt(discriminant)
    t_vals = [(-b - sqrt_d) / 2, (-b + sqrt_d) / 2]
    
    # Return a list of coordinate arrays
    return [ray_origin + t * ray_dir  for t in t_vals if t > 0]


def intersect_arc(ray_origin, ray_dir, center, radius, axis, cos_half_angle): #contains solution
    # LEVEL 4: Angular sector check
    intersect_pts = intersect_circle(ray_origin, ray_dir, center, radius)
    
    if not intersect_pts or len(intersect_pts) == 0:
        return None

    for P in intersect_pts:
        vec_CP = (P - center) / radius
        if np.dot(vec_CP, axis) >= cos_half_angle - CONST_EPSILON: # Use a small epsilon for float stability
            return P
                
    return None

# =============================================================================
#  INTERSECTION DISPATCHER, IMPLEMENTATION PROVIDED
# =============================================================================
def intersect_curve(ray_origin, ray_dir, curve):
    if curve['type'] == 'line':
        return intersect_segment(ray_origin, ray_dir, curve['p1'], curve['p2'])
    elif curve['type'] == 'arc':
        return intersect_arc(ray_origin, ray_dir, curve['center'], 
                             curve['radius'], curve['axis'], curve['cos_half_angle'])
    return None
# =============================================================================


# =============================================================================
#  STUDENT IMPLEMENTATION (ASSIGNMENTS 5-6)
# =============================================================================


def calculate_normal_segment(ray_dir, p1, p2): #contains solution
    # LEVEL 5: Line Normal + Flip Logic
    tangent = p2 - p1
    normal = np.array([-tangent[1], tangent[0]], dtype=float)
    normal /= np.linalg.norm(normal)
    if np.dot(ray_dir, normal) > 0: normal = -normal
    return normal


def calculate_normal_arc(hit_point, ray_dir, center): #contains solution
    # LEVEL 6: Arc Normal + Flip Logic
    normal = (hit_point - center).astype(float)
    normal /= np.linalg.norm(normal)
    if np.dot(ray_dir, normal) > 0: normal = -normal
    return normal

# =============================================================================
#  NORMAL DISPATCHER, IMPLEMENTATION PROVIDED
# =============================================================================
def calculate_normal(hit_point, ray_dir, curve):
    if curve['type'] == 'line':
        return calculate_normal_segment(ray_dir, curve['p1'], curve['p2'])
    elif curve['type'] == 'arc':
        return calculate_normal_arc(hit_point, ray_dir, curve['center'])
    return None
# =============================================================================


# =============================================================================
#  STUDENT IMPLEMENTATION (ASSIGNMENT 7)
# =============================================================================


def refract_vector(ray_dir, normal, n1, n2): #contains solution
    # LEVEL 7: Snell's Law
    eta = n1 / n2
    cos_theta1 = -np.dot(ray_dir, normal)
    sin2_theta1 = 1 - cos_theta1**2
    sin2_theta2 = eta**2 * sin2_theta1
    if sin2_theta2 > 1.0: 
        return None 
    cos_theta2 = np.sqrt(1 - sin2_theta2)
    return eta * ray_dir + (eta * cos_theta1 - cos_theta2) * normal

# =============================================================================



# =============================================================================
#  RAY TRACING, IMPLEMENTATION PROVIDED
# =============================================================================

def trace_ray_step(ray_origin, ray_dir, curves, n1, n2):
    # --- 1. GEOMETRY: FIND NEAREST INTERSECTION ---
    # We iterate only through the curves of the specific lens passed in
    hits = []
    for c in curves:
        p = intersect_curve(ray_origin, ray_dir, c)
        if p is None:
            continue
        d = np.linalg.norm(p - ray_origin)
        if d > CONST_EPSILON: # Avoid self-intersection
            hits.append((d, c))
    
    # Find the closest valid hit
    if not hits:
        return None, None

    min_t, hit_curve = min(hits, key=lambda x: x[0])
    if hit_curve is None or min_t == float('inf'):
        return None, None 

    best_hit = ray_origin + min_t * ray_dir

    # --- 2. PHYSICS & 3. REFRACTION ---
    # Normal calculation remains specific to the surface geometry
    normal = calculate_normal(best_hit, ray_dir, hit_curve)
    
    # Use n1 and n2 directly from the arguments
    new_dir = refract_vector(ray_dir, normal, n1, n2)

    # Return only the point and direction; medium tracking is now the Ray's job
    return best_hit, new_dir


# =============================================================================


# =============================================================================
#  STUDENT IMPLEMENTATION (ADDITIONAL ASSIGNMENT)
# =============================================================================


def calculate_focal_length(R1, R2, d, n): #contains solution
    power = (n - 1) * (1/R1 - 1/R2 + ((n - 1) * d * 1/R1 * 1/R2) / n)
    return 1.0 / power 


def calculate_slab_displacement(d, n, theta): #contains solution
    theta_prime = np.arcsin(np.sin(theta) / n)
    h = d * np.sin(theta - theta_prime) / np.cos(theta_prime)
    return h    
    
