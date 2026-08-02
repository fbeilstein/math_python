# =============================================================================
#  STUDENT IMPLEMENTATION (TOPOLOGICAL WRAPPING)
# =============================================================================

def wrap_cylinder(nx, ny, dx, dy, width, height, out_left, out_right, out_top, out_bottom): #contains solution
    if out_top or out_bottom:
        return None
        
    wx, wy = nx, ny
    wdx, wdy = dx, dy
    
    if out_left:
        wx = width - 1
    elif out_right:
        wx = 0
        
    return wx, wy, wdx, wdy


def wrap_mobius(nx, ny, dx, dy, width, height, out_left, out_right, out_top, out_bottom): #contains solution
    if out_top or out_bottom:
        return None
        
    wx, wy = nx, ny
    wdx, wdy = dx, dy
    
    if out_left:
        wx = width - 1
        wy = (height - 1) - wy
        wdy = -wdy
    elif out_right:
        wx = 0
        wy = (height - 1) - wy
        wdy = -wdy
        
    return wx, wy, wdx, wdy


def wrap_torus(nx, ny, dx, dy, width, height, out_left, out_right, out_top, out_bottom): #contains solution
    wx, wy = nx, ny
    wdx, wdy = dx, dy
    
    if out_left:
        wx = width - 1
    elif out_right:
        wx = 0
        
    if out_top:
        wy = height - 1
    elif out_bottom:
        wy = 0
        
    return wx, wy, wdx, wdy


def wrap_klein_bottle(nx, ny, dx, dy, width, height, out_left, out_right, out_top, out_bottom): #contains solution
    wx, wy = nx, ny
    wdx, wdy = dx, dy
    
    if out_left:
        wx = width - 1
    elif out_right:
        wx = 0
        
    if out_top:
        wy = height - 1
        wx = (width - 1) - wx
        wdx = -wdx
    elif out_bottom:
        wy = 0
        wx = (width - 1) - wx
        wdx = -wdx
        
    return wx, wy, wdx, wdy


def wrap_projective_plane(nx, ny, dx, dy, width, height, out_left, out_right, out_top, out_bottom): #contains solution
    wx, wy = nx, ny
    wdx, wdy = dx, dy
    
    if out_left:
        wx = width - 1
        wy = (height - 1) - wy
        wdy = -wdy
    elif out_right:
        wx = 0
        wy = (height - 1) - wy
        wdy = -wdy
        
    if out_top:
        wy = height - 1
        wx = (width - 1) - wx
        wdx = -wdx
    elif out_bottom:
        wy = 0
        wx = (width - 1) - wx
        wdx = -wdx
        
    return wx, wy, wdx, wdy

# =============================================================================
#  TOPOLOGY DISPATCHER, IMPLEMENTATION PROVIDED
# =============================================================================

def apply_topology(topology_name, nx, ny, dx, dy, width, height):
    """
    Given a new position (nx, ny) and the direction (dx, dy),
    returns the wrapped (wx, wy) and (wdx, wdy) based on the topology.
    Returns None if the boundary is solid (death).
    """
    out_left = nx < 0
    out_right = nx >= width
    out_top = ny < 0
    out_bottom = ny >= height

    if not (out_left or out_right or out_top or out_bottom):
        return nx, ny, dx, dy

    if topology_name == "Square":
        return None  # All boundaries are solid

    elif topology_name == "Cylinder":
        return wrap_cylinder(nx, ny, dx, dy, width, height, out_left, out_right, out_top, out_bottom)

    elif topology_name == "Möbius":
        return wrap_mobius(nx, ny, dx, dy, width, height, out_left, out_right, out_top, out_bottom)

    elif topology_name == "Torus":
        return wrap_torus(nx, ny, dx, dy, width, height, out_left, out_right, out_top, out_bottom)

    elif topology_name == "Klein Bottle":
        return wrap_klein_bottle(nx, ny, dx, dy, width, height, out_left, out_right, out_top, out_bottom)

    elif topology_name == "Real Projective Plane":
        return wrap_projective_plane(nx, ny, dx, dy, width, height, out_left, out_right, out_top, out_bottom)

    return None
