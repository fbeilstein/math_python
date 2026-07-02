import unittest
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel6(unittest.TestCase):
    def test_linear_decoding(self):
        p, n = 2, 8
        poly = [1, 0, 0, 0, 1, 1, 1, 0, 1]
        exp_table, log_table = tasks.generate_gfpn_tables(p, n, poly)
        
        text = "Hello"
        bytes_arr = [ord(c) for c in text]
        
        gen = tasks.get_generator_poly(4, log_table, exp_table, p, n)
        rem = tasks.gfpn_poly_remainder(bytes_arr + [0]*4, gen, log_table, exp_table, p, n)
        encoded = bytes_arr + rem
        
        corrupted = list(encoded)
        corrupted[1] ^= 255 
        
        syn = tasks.calculate_syndromes(corrupted, 4, log_table, exp_table, p, n)
        err_loc = tasks.pgz_error_locator(syn, log_table, exp_table, p, n)
        
        err_pos = tasks.chien_search(err_loc, len(corrupted), log_table, exp_table, p, n)
        
        mags = tasks.linear_error_magnitudes(syn, err_pos, len(corrupted), log_table, exp_table, p, n)
        
        for p_idx, mag in mags.items():
            corrupted[p_idx] = tasks.gfpn_sub(corrupted[p_idx], mag, p, n)
            
        decoded_text = "".join(chr(c % 256) for c in corrupted[:len(text)])
        self.assertEqual(decoded_text, text)


import itertools

def poly_to_str(poly):
    if not poly or (len(poly) == 1 and poly[0] == 0): return "0"
    terms = []
    deg = len(poly) - 1
    for i, c in enumerate(poly):
        if c == 0: continue
        power = deg - i
        term = ""
        if c != 1 or power == 0: term += str(c)
        if power > 0:
            term += "x"
            if power > 1: term += f"^{power}"
        terms.append(term)
    return " + ".join(terms)

if __name__ == '__main__':
    unittest.main()
