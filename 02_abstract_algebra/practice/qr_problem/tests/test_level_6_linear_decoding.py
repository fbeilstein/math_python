import unittest
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks
import algebra_utils as utils

class TestLevel6(unittest.TestCase):
    def test_linear_decoding(self):
        poly = utils.make_poly([1, 0, 0, 0, 1, 1, 1, 0, 1], 2)
        gf = tasks.ExtensionField(poly)

        text = "Hello"
        bytes_arr = [utils.int_to_ext(ord(c), gf) for c in text]

        gen = tasks.get_generator_poly(4, gf)

        msg_poly = tasks.Polynomial([gf.zero]*4 + list(reversed(bytes_arr)))
        q, rem = divmod(msg_poly, gen)

        diff = 4 - (rem.degree() + 1)
        rem_padded = [rem[i] for i in range(rem.degree() + 1)] + [gf.zero]*diff
        encoded = rem_padded + list(reversed(bytes_arr))

        corrupted = list(encoded)
        corrupted[1] = utils.int_to_ext(utils.ext_to_int(corrupted[1]) ^ 255, gf)

        msg_poly = tasks.Polynomial(corrupted)
        syn = tasks.calculate_syndromes(msg_poly, 4, gf)
        err_loc = tasks.pgz_error_locator(syn, gf)

        err_pos = tasks.chien_search(err_loc, len(corrupted), gf)

        mags = tasks.linear_error_magnitudes(syn, err_pos, gf)

        for i, pos in enumerate(err_pos):
            corrupted[pos] = corrupted[pos] - mags[i]

        decoded_text = "".join(chr(utils.ext_to_int(c) % 256) for c in reversed(corrupted[4:]))
        self.assertEqual(decoded_text, text)

if __name__ == '__main__':
    unittest.main()
