import numpy as np


class Ray:
    def __init__(self, start_pos, direction, start_medium=0):
        self.points = [np.array(start_pos)]
        self.direction = np.array(direction) / np.linalg.norm(direction)
        self.media_sequence = [start_medium]
        self.exits = {}  # {medium_id: (exit_point, exit_direction)}
        self.is_terminated = False

    def add_segment(self, hit_point, next_medium, next_direction=None):
        # If we are leaving a lens (current_medium > 0), record the exit data for THAT lens
        if self.current_medium > 0 and next_medium == 0:
            self.exits[self.current_medium] = (np.array(hit_point), np.array(next_direction) if next_direction is not None else None)
            
        self.points.append(np.array(hit_point))
        self.media_sequence.append(next_medium)
        if next_direction is not None:
            self.direction = np.array(next_direction) / np.linalg.norm(next_direction)
            
    @property
    def current_pos(self):
        return self.points[-1]

    @property
    def current_medium(self):
        return self.media_sequence[-1]
