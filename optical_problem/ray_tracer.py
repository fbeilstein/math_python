import numpy as np
from implementation_tasks import trace_ray_step

EPSILON = 1e-4

class RayTracer:
    @staticmethod
    def trace(ray, lenses, max_steps=1000):
        for _ in range(max_steps): # in case students make some bug
            if ray.is_terminated:
                break
            
            best_hit = None
            best_nd = None
            best_lens = None
            min_dist = float('inf')

            # 1. Ask every lens: "Do you intersect this ray?"
            for lens in lenses:
                # Determine local n1/n2 for this specific lens
                n1 = 1.0 if ray.current_medium == 0 else lens.n
                n2 = lens.n if ray.current_medium == 0 else 1.0
                
                # Your API: Returns (hit_point, new_direction) or (None, None)
                hit, n_d = trace_ray_step(
                    ray.current_pos, 
                    ray.direction, 
                    lens.get_curves(0), 
                    n1, 
                    n2
                )

                if hit is not None:
                    dist = np.linalg.norm(hit - ray.current_pos)
                    # We only care about the CLOSEST lens hit in front of the ray
                    if dist < min_dist and dist > 0: 
                        min_dist = dist
                        best_hit = hit
                        best_nd = n_d
                        best_lens = lens

            # 2. Process the closest hit
            if best_hit is not None:
                # Update medium: 0 for Air, or a unique ID based on the lens list
                new_medium = (lenses.index(best_lens) + 1) if ray.current_medium == 0 else 0
                if best_nd is not None:
                    best_hit += EPSILON * best_nd
                ray.add_segment(best_hit, new_medium, next_direction=best_nd)
                
                # If there's no new direction (Total Internal Reflection or absorption)
                if best_nd is None:
                    ray.is_terminated = True
            else:
                # 3. No hits: Ray goes to infinity
                ray.add_segment(ray.current_pos + ray.direction * 500, ray.current_medium)
                ray.is_terminated = True
                
                
                
                
                
                
                
                
