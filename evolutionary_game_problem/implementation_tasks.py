import random
import numpy as np

# =====================================================================
# STUDENT IMPLEMENTATION (Evolutionary Game Theory)
# =====================================================================

class BaseStrategy:
    """
    Base class for all evolutionary strategies.
    Students can write new strategies by inheriting from this class.
    The GUI will automatically discover any subclass you define here!
    """
    def reset(self):
        """Reset any memory before a new match begins."""
        pass
        
    def get_action(self, my_history, opponent_history):
        """
        Return 'C' for Cooperate or 'D' for Defect.
        my_history: list of 'C' or 'D' (your past actions)
        opponent_history: list of 'C' or 'D' (opponent's past actions)
        """
# =====================================================================
# L0: Strategy Implementation
# =====================================================================
# Below are the stubs for four fundamental strategies. 
# You are required to implement `get_action` for each of them.
# After completing these, you can design and add your own custom strategies!
# Note: The GUI will automatically discover and load any subclass you define here.

class AlwaysCooperate(BaseStrategy):
    def get_action(self, my_history, opponent_history): #contains solution
        return 'C'

class AlwaysDefect(BaseStrategy):
    def get_action(self, my_history, opponent_history): #contains solution
        return 'D'

class TitForTat(BaseStrategy):
    def get_action(self, my_history, opponent_history): #contains solution
        if not opponent_history:
            return 'C'
        return opponent_history[-1]

class GrimTrigger(BaseStrategy):
    def get_action(self, my_history, opponent_history): #contains solution
        if 'D' in opponent_history:
            return 'D'
        return 'C'

# ---------------------------------------------------------
# L1: Match Play
# ---------------------------------------------------------

def play_match(strat_A, strat_B, matrix, rounds): #contains solution
    """
    L1: Play a match between two strategy objects for a given number of rounds.
    The `matrix` is a dict of dicts: matrix['C']['D'] gives the payoff for C against D.
    
    You must:
    1. Call strat.reset() on both strategies before starting.
    2. In each round, get their actions using strat.get_action().
    3. Update their histories.
    4. Accumulate their payoffs.
    
    Return a tuple: (total_payoff_A, total_payoff_B)
    """
    strat_A.reset()
    strat_B.reset()
    
    hist_A = []
    hist_B = []
    
    score_A = 0
    score_B = 0
    
    for _ in range(rounds):
        action_A = strat_A.get_action(hist_A, hist_B)
        action_B = strat_B.get_action(hist_B, hist_A)
        
        score_A += matrix[action_A][action_B]
        score_B += matrix[action_B][action_A]
        
        hist_A.append(action_A)
        hist_B.append(action_B)
        
    return score_A, score_B

# ---------------------------------------------------------
# L2: Spatial Fitness
# ---------------------------------------------------------

def compute_neighborhood_fitness(grid, r, c, matrix, rounds=1): #contains solution
    """
    L3: Compute the total fitness of the agent at grid[r][c].
    The agent plays a match against all valid cells in the Moore neighborhood
    (including itself).
    Use hard boundaries (do NOT wrap around the edges).
    
    Use play_match() to calculate the payoff against each neighbor.
    Return the total accumulated payoff.
    """
    rows, cols = grid.shape
    agent = grid[r, c]
    total_fitness = 0
    
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr = r + dr
            nc = c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            neighbor = grid[nr, nc]
            
            score_A, _ = play_match(agent, neighbor, matrix, rounds)
            total_fitness += score_A
            
    return total_fitness

# ---------------------------------------------------------
# L3: Spatial Chaos (Deterministic)
# ---------------------------------------------------------

def update_grid_deterministic(grid, matrix, rounds=1): #contains solution
    """
    L3: Implement the "Imitate-the-Best" spatial update rule (Nowak & May).
    For every cell, compute its fitness and the fitness of all 8 neighbors.
    In the next generation, the cell adopts the strategy class of the most 
    successful agent in that 3x3 neighborhood (including its own score).
    
    If there is a tie, keep the current strategy.
    
    Return a NEW grid of instantiated strategy objects.
    """
    rows, cols = grid.shape
    
    # Precompute all fitnesses
    fitness = np.zeros((rows, cols))
    for r in range(rows):
        for c in range(cols):
            fitness[r, c] = compute_neighborhood_fitness(grid, r, c, matrix, rounds)
            
    new_grid = np.empty((rows, cols), dtype=object)
    
    for r in range(rows):
        for c in range(cols):
            best_r, best_c = r, c
            best_fit = fitness[r, c]
            
            # Check 8 neighbors
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr = r + dr
                    nc = c + dc
                    
                    if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                        continue
                    
                    # Strict inequality ensures we keep current strategy on ties
                    if fitness[nr, nc] > best_fit:
                        best_fit = fitness[nr, nc]
                        best_r, best_c = nr, nc
                        
            # Instantiate a new copy of the best strategy
            best_strat_class = grid[best_r, best_c].__class__
            new_grid[r, c] = best_strat_class()
            
    return new_grid
