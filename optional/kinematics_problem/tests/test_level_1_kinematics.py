import unittest
import sys, os
import math

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestKinematics(unittest.TestCase):
    def test_split_complex_mul(self):
        s1 = tasks.SplitComplex(2, 3)
        s2 = tasks.SplitComplex(4, 5)
        s3 = s1 * s2
        # (2+3j)(4+5j) = (8+15) + (10+12)j = 23 + 22j
        self.assertAlmostEqual(s3.real, 23)
        self.assertAlmostEqual(s3.j, 22)

    def test_quaternion_mul(self):
        q1 = tasks.Quaternion(1, 2, 3, 4)
        q2 = tasks.Quaternion(5, 6, 7, 8)
        q3 = q1 * q2
        self.assertAlmostEqual(q3.w, -60)
        self.assertAlmostEqual(q3.x, 12)
        self.assertAlmostEqual(q3.y, 30)
        self.assertAlmostEqual(q3.z, 24)

    def test_dual_quaternion_mul(self):
        q_r1 = tasks.Quaternion(1, 0, 0, 0)
        q_d1 = tasks.Quaternion(0, 1, 0, 0)
        dq1 = tasks.DualQuaternion(q_r1, q_d1)
        
        q_r2 = tasks.Quaternion(0, 1, 0, 0)
        q_d2 = tasks.Quaternion(0, 0, 1, 0)
        dq2 = tasks.DualQuaternion(q_r2, q_d2)
        
        dq3 = dq1 * dq2
        
        # qr3 = q_r1 * q_r2 = Q(0, 1, 0, 0)
        self.assertAlmostEqual(dq3.qr.w, 0)
        self.assertAlmostEqual(dq3.qr.x, 1)
        self.assertAlmostEqual(dq3.qr.y, 0)
        self.assertAlmostEqual(dq3.qr.z, 0)
        
        # qd3 = q_r1*q_d2 + q_d1*q_r2 = Q(0,0,1,0) + (-1,0,0,0) = Q(-1, 0, 1, 0)
        self.assertAlmostEqual(dq3.qd.w, -1)
        self.assertAlmostEqual(dq3.qd.x, 0)
        self.assertAlmostEqual(dq3.qd.y, 1)
        self.assertAlmostEqual(dq3.qd.z, 0)
        
    def test_to_translation_rotation(self):
        rot = tasks.Quaternion(1, 0, 0, 0) # identity
        trans = (10, 20, 30)
        dq = tasks.DualQuaternion.from_translation_rotation(trans, rot)
        
        out_trans, out_rot = dq.to_translation_rotation()
        self.assertAlmostEqual(out_trans[0], 10)
        self.assertAlmostEqual(out_trans[1], 20)
        self.assertAlmostEqual(out_trans[2], 30)
        self.assertAlmostEqual(out_rot.w, 1)

    def test_sclerp(self):
        dq1 = tasks.DualQuaternion.from_translation_rotation((0,0,0), tasks.Quaternion(1,0,0,0))
        dq2 = tasks.DualQuaternion.from_translation_rotation((10,0,0), tasks.Quaternion(1,0,0,0))
        
        dq_mid = tasks.sclerp(dq1, dq2, 0.5)
        t, r = dq_mid.to_translation_rotation()
        self.assertAlmostEqual(t[0], 5)
        self.assertAlmostEqual(t[1], 0)
        self.assertAlmostEqual(t[2], 0)

if __name__ == '__main__':
    unittest.main()
