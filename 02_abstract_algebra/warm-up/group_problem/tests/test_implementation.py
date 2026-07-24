"""Tests for group_problem implementation tasks."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import implementation_tasks as tasks
import group_engine as ge

class TestLevel1Axioms(unittest.TestCase):
    def test_z4_passes(self):
        G = ge.from_Zn(4)
        self.assertTrue(tasks.check_closure(G.elements))
        self.assertTrue(tasks.check_associativity(G.elements))
        self.assertEqual(tasks.find_identity(G.elements), G.identity_element)
        self.assertTrue(tasks.check_inverses(G.elements, G.identity_element))

    def test_broken_table_closure(self):
        class MockElem(ge.GroupElement):
            def __init__(self, v): self.idx = v
            def __mul__(self, o): return MockElem(5)
            def __invert__(self): return self
            def __eq__(self, o): return isinstance(o, MockElem) and self.idx == o.idx
            def __hash__(self): return hash(self.idx)
        
        elements = {MockElem(0), MockElem(1)}
        self.assertFalse(tasks.check_closure(elements))

    def test_z6_mul_no_inverses(self):
        class MockZ6(ge.GroupElement):
            def __init__(self, v): self.idx = v
            def __mul__(self, o): return MockZ6((self.idx * o.idx) % 6)
            def __invert__(self): return MockZ6(1) # fake inverse
            def __eq__(self, o): return isinstance(o, MockZ6) and self.idx == o.idx
            def __hash__(self): return hash(self.idx)
            
        elements = {MockZ6(i) for i in range(6)}
        identity = tasks.find_identity(elements)
        self.assertEqual(identity.idx, 1)
        self.assertFalse(tasks.check_inverses(elements, identity))

class TestLevel2Permutations(unittest.TestCase):
    def test_compose(self):
        p = tasks.PermutationElement([1, 2, 0])
        q = tasks.PermutationElement([1, 0, 2])
        r = p * q
        self.assertEqual(r.mapping, (2, 1, 0))

    def test_inverse(self):
        p = tasks.PermutationElement([1, 2, 0])
        inv = ~p
        identity = p * inv
        self.assertEqual(identity.mapping, (0, 1, 2))

    def test_order(self):
        p = tasks.PermutationElement([1, 2, 0])
        elements = [tasks.PermutationElement([0, 1, 2]), p, tasks.PermutationElement([2, 0, 1])]
        
        group = ge.Group(elements=elements)
        self.assertEqual(tasks.element_order(group, p), 3)

    def test_generate_group_cyclic(self):
        gens = [tasks.PermutationElement([1, 2, 0])]
        group = tasks.generate_group(gens)
        self.assertEqual(len(group), 3)

    def test_generate_group_s3(self):
        gens = [tasks.PermutationElement([1, 2, 0]), tasks.PermutationElement([1, 0, 2])]
        group = tasks.generate_group(gens)
        self.assertEqual(len(group), 6)

class TestLevel3Cayley(unittest.TestCase):
    def test_z4(self):
        G = ge.from_Zn(4)
        g1 = None
        for g in G.elements:
            if str(g) == '1':
                g1 = g
                break
        nodes, edges = tasks.generate_cayley_graph(G, [g1])
        self.assertEqual(len(nodes), 4)
        self.assertEqual(len(edges), 4)

class TestLevel4Subgroups(unittest.TestCase):
    def test_z6_subgroups(self):
        G = ge.from_Zn(6)
        sgs = tasks.find_all_subgroups(G)
        sizes = sorted(len(sg) for sg in sgs)
        self.assertEqual(sizes, [1, 2, 3, 6])

    def test_lagrange(self):
        G = ge.from_Dn(4)
        sgs = tasks.find_all_subgroups(G)
        for sg in sgs:
            self.assertEqual(len(G) % len(sg), 0)

class TestLevel5Cosets(unittest.TestCase):
    def test_z6_cosets(self):
        G = ge.from_Zn(6)
        g2 = next(g for g in G.elements if str(g) == '2')
        H = tasks.generate_group([g2])
        cosets = tasks.compute_left_cosets(G, H)
        self.assertEqual(len(cosets), 2)
        self.assertTrue(all(len(c) == 3 for c in cosets))

    def test_normal_in_abelian(self):
        G = ge.from_Zn(6)
        g2 = next(g for g in G.elements if str(g) == '2')
        H = tasks.generate_group([g2])
        self.assertTrue(tasks.is_normal(G, H))

    def test_non_normal_in_s3(self):
        G = ge.from_Sn(3)
        g = next(g for g in G.elements if str(g) == '(0 1)')
        H = tasks.generate_group([g])
        self.assertEqual(len(H), 2)
        self.assertFalse(tasks.is_normal(G, H))

class TestLevel6Center(unittest.TestCase):
    def test_abelian_center(self):
        G = ge.from_Zn(5)
        center = tasks.compute_center(G)
        self.assertEqual(len(center), 5)

    def test_d4_center(self):
        G = ge.from_Dn(4)
        center = tasks.compute_center(G)
        self.assertEqual(len(center), 2)

    def test_conjugacy_classes_partition(self):
        G = ge.from_Dn(3)
        classes = tasks.compute_conjugacy_classes(G)
        total = sum(len(c) for c in classes)
        self.assertEqual(total, len(G))

class TestLevel7Homomorphisms(unittest.TestCase):
    def test_z6_to_z3(self):
        G = ge.from_Zn(6)
        H = ge.from_Zn(3)
        phi = {}
        for g in G.elements:
            val = int(str(g)) % 3
            for h in H.elements:
                if str(h) == str(val):
                    phi[g] = h
                    break
        self.assertTrue(tasks.is_homomorphism(G, phi))
        ker = tasks.compute_kernel(G, H, phi)
        self.assertEqual(len(ker), 2)
        img = tasks.compute_image(G, H, phi)
        self.assertEqual(len(img), 3)

    def test_bad_homomorphism(self):
        G = ge.from_Zn(4)
        H = ge.from_Zn(3)
        phi = {}
        for g in G.elements:
            val = [0, 1, 2, 0][int(str(g))]
            for h in H.elements:
                if str(h) == str(val):
                    phi[g] = h
                    break
        self.assertFalse(tasks.is_homomorphism(G, phi))

class TestGroupEngine(unittest.TestCase):
    def test_zn(self):
        G = ge.from_Zn(5)
        self.assertEqual(len(G), 5)

    def test_un(self):
        G = ge.from_Un(8)
        self.assertEqual(len(G), 4)

    def test_dn(self):
        G = ge.from_Dn(3)
        self.assertEqual(len(G), 6)

    def test_sn(self):
        G = ge.from_Sn(3)
        self.assertEqual(len(G), 6)

    def test_from_perms(self):
        gens = [(1, 2, 0), (1, 0, 2)]
        G = ge.from_permutation_generators(gens, 3)
        self.assertEqual(len(G), 6)

if __name__ == '__main__':
    unittest.main()
