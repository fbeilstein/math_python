import math
import random

# ==========================================
# LEVEL 1: The Basic N-Gram
# ==========================================

def update_markov_counts(history, new_char, order, counts_dict): #contains solution
    """
    Updates the N-Gram count dictionary with a new character.
    If the history is long enough, extracts the preceding state of length `order`.
    If the state is not in counts_dict, adds it. Then increments the count for `new_char`.
    """
    if len(history) >= order:
        state = history[-order:]
        if state not in counts_dict:
            counts_dict[state] = {"1": 0, "2": 0}
        counts_dict[state][new_char] += 1

def predict_fixed_order(history, order, counts_dict): #contains solution
    """
    Predicts the next character strictly using the last `order` characters.
    If the state hasn't been seen, or counts are perfectly tied, returns a random guess.
    """
    if len(history) >= order:
        state = history[-order:]
        if state in counts_dict:
            c1 = counts_dict[state]["1"]
            c2 = counts_dict[state]["2"]
            if c1 > c2:
                return "1"
            elif c2 > c1:
                return "2"
    return random.choice(["1", "2"])

# ==========================================
# LEVEL 2: Statistical Significance
# ==========================================

def calculate_p_value(correct_guesses, total_trials): #contains solution
    """
    Calculates the p-value using the standard normal approximation of the binomial distribution.
    Null hypothesis: p = 0.5 (random chance).
    Returns the p-value representing the probability of achieving `correct_guesses` or higher.
    """
    from scipy.stats import norm
    if total_trials == 0:
        return 0.5
    mu = total_trials / 2.0
    sigma = math.sqrt(total_trials) / 2.0
    
    if correct_guesses >= mu:
        p_val = norm.sf(correct_guesses, mu, sigma) # Survival function (1 - CDF)
    else:
        p_val = norm.cdf(correct_guesses, mu, sigma) # Lower tail
    return p_val

# ==========================================
# LEVEL 3: Variable-Order Fallback (Smoothing)
# ==========================================

def predict_with_fallback(history, max_order, counts_dict): #contains solution
    """
    Predicts the next character by trying the longest available context up to `max_order`.
    If a state hasn't been seen, or its counts are tied, falls back to a shorter context.
    If all fallbacks fail, guesses randomly.
    """
    for o in range(max_order, -1, -1):
        if o == 0:
            break
        if len(history) >= o:
            state = history[-o:]
            if state in counts_dict:
                c1 = counts_dict[state]["1"]
                c2 = counts_dict[state]["2"]
                
                # Tie-breaker / Smoothing logic: fall back if tied
                if c1 == c2 and c1 > 0:
                    continue
                    
                if c1 > c2: return "1"
                if c2 > c1: return "2"
                
    return random.choice(["1", "2"])

# ==========================================
# LEVEL 4: Mixture of Experts (Online Learning)
# ==========================================

def update_expert_scores(scores, expert_predictions, actual_char, decay): #contains solution
    """
    Updates the confidence scores for multiple experts based on their previous predictions.
    Applies exponential decay, then adds 1.0 if the expert was correct.
    Returns the updated scores array.
    """
    updated_scores = []
    for i in range(len(scores)):
        score = scores[i] * decay
        if expert_predictions[i] == actual_char:
            score += 1.0
        updated_scores.append(score)
    return updated_scores

def get_best_expert(scores): #contains solution
    """
    Returns the index of the expert with the highest confidence score.
    """
    import numpy as np
    return int(np.argmax(scores))

# ==========================================
# LEVEL 5: The Pi Simulator (True Randomness)
# ==========================================

def arccot(x, unity): #contains solution
    """
    Helper function to calculate arccot using integer arithmetic for arbitrary precision.
    """
    sum_val = xpower = unity // x
    n = 3
    sign = -1
    while True:
        xpower = xpower // (x * x)
        term = xpower // n
        if not term:
            break
        sum_val += sign * term
        sign = -sign
        n += 2
    return sum_val

def generate_pi_binary_digits(num_bits): #contains solution
    """
    Generates `num_bits` true binary digits of Pi using Machin's arctangent formula.
    Returns a binary string.
    """
    unity = 1 << (num_bits + 10)
    pi_scaled = 4 * (4 * arccot(5, unity) - arccot(239, unity))
    pi_scaled = pi_scaled >> 10
    frac = pi_scaled - (3 << num_bits) # Remove integer part '3'
    return bin(frac)[2:].zfill(num_bits)

# =============================================================================
#  SELF-TESTING (add your own tests below)
# =============================================================================
if __name__ == '__main__':
    import unittest
    # Add your own unittest.TestCase classes here, then run:
    #     python implementation_tasks.py
    unittest.main(verbosity=2)
