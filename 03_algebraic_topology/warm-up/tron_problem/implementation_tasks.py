# =============================================================================
#  STUDENT IMPLEMENTATION (TOPOLOGICAL WRAPPING)
# =============================================================================

def wrap_cylinder(x, y, dx, dy, width, height): #contains solution
    nx, ny = x + dx, y + dy
    
    if ny < 0 or ny >= height:
        return None
        
    if nx < 0:
        nx = width - 1
    elif nx >= width:
        nx = 0
        
    return nx, ny, dx, dy


def wrap_mobius(x, y, dx, dy, width, height): #contains solution
    nx, ny = x + dx, y + dy
    
    if ny < 0 or ny >= height:
        return None
        
    if nx < 0:
        nx = width - 1
        ny = (height - 1) - ny
        dy = -dy
    elif nx >= width:
        nx = 0
        ny = (height - 1) - ny
        dy = -dy
        
    return nx, ny, dx, dy


def wrap_torus(x, y, dx, dy, width, height): #contains solution
    nx, ny = x + dx, y + dy
    
    if nx < 0:
        nx = width - 1
    elif nx >= width:
        nx = 0
        
    if ny < 0:
        ny = height - 1
    elif ny >= height:
        ny = 0
        
    return nx, ny, dx, dy


def wrap_klein_bottle(x, y, dx, dy, width, height): #contains solution
    nx, ny = x + dx, y + dy
    
    if nx < 0:
        nx = width - 1
    elif nx >= width:
        nx = 0
        
    if ny < 0:
        ny = height - 1
        nx = (width - 1) - nx
        dx = -dx
    elif ny >= height:
        ny = 0
        nx = (width - 1) - nx
        dx = -dx
        
    return nx, ny, dx, dy


def wrap_projective_plane(x, y, dx, dy, width, height): #contains solution
    nx, ny = x + dx, y + dy
    
    if nx < 0:
        nx = width - 1
        ny = (height - 1) - ny
        dy = -dy
    elif nx >= width:
        nx = 0
        ny = (height - 1) - ny
        dy = -dy
        
    if ny < 0:
        ny = height - 1
        nx = (width - 1) - nx
        dx = -dx
    elif ny >= height:
        ny = 0
        nx = (width - 1) - nx
        dx = -dx
        
    return nx, ny, dx, dy

# =============================================================================
#  TOPOLOGY DISPATCHER, IMPLEMENTATION PROVIDED
# =============================================================================

def apply_topology(topology_name, x, y, dx, dy, width, height):
    """
    Given the current position (x, y) and the direction (dx, dy),
    returns the wrapped (nx, ny) and (ndx, ndy) based on the topology.
    Returns None if the boundary is solid (death).
    """
    if topology_name == "Square":
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            return None
        return nx, ny, dx, dy

    elif topology_name == "Cylinder":
        return wrap_cylinder(x, y, dx, dy, width, height)

    elif topology_name == "Möbius":
        return wrap_mobius(x, y, dx, dy, width, height)

    elif topology_name == "Torus":
        return wrap_torus(x, y, dx, dy, width, height)

    elif topology_name == "Klein Bottle":
        return wrap_klein_bottle(x, y, dx, dy, width, height)

    elif topology_name == "Real Projective Plane":
        return wrap_projective_plane(x, y, dx, dy, width, height)

    return None
