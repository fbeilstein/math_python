def apply_topology(topology_name, nx, ny, dx, dy, width, height):
    """
    Given a new position (nx, ny) and the direction (dx, dy),
    returns the wrapped (wx, wy) and (wdx, wdy) based on the topology.
    Returns None if the boundary is solid (death).
    """
    wrapped = False
    wx, wy = nx, ny
    wdx, wdy = dx, dy
    
    out_left = nx < 0
    out_right = nx >= width
    out_top = ny < 0
    out_bottom = ny >= height

    if not (out_left or out_right or out_top or out_bottom):
        return wx, wy, wdx, wdy

    if topology_name == "Square":
        return None  # All boundaries are solid

    elif topology_name == "Cylinder":
        if out_top or out_bottom:
            return None
        if out_left:
            wx = width - 1
        elif out_right:
            wx = 0

    elif topology_name == "Möbius":
        if out_top or out_bottom:
            return None
        if out_left:
            wx = width - 1
            wy = (height - 1) - wy
        elif out_right:
            wx = 0
            wy = (height - 1) - wy

    elif topology_name == "Torus":
        if out_left:
            wx = width - 1
        elif out_right:
            wx = 0
        if out_top:
            wy = height - 1
        elif out_bottom:
            wy = 0

    elif topology_name == "Klein Bottle":
        if out_left:
            wx = width - 1
        elif out_right:
            wx = 0
        if out_top:
            wy = height - 1
            wx = (width - 1) - wx
        elif out_bottom:
            wy = 0
            wx = (width - 1) - wx

    elif topology_name == "Real Projective Plane":
        if out_left:
            wx = width - 1
            wy = (height - 1) - wy
        elif out_right:
            wx = 0
            wy = (height - 1) - wy
            
        if out_top:
            wy = height - 1
            wx = (width - 1) - wx
        elif out_bottom:
            wy = 0
            wx = (width - 1) - wx

    return wx, wy, wdx, wdy
