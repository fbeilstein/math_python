import gudhi.wasserstein
import numpy as np

d1 = np.array([[1.0, 2.0], [1.5, 2.5]])
d2 = np.array([[1.1, 2.1]])

dist, match = gudhi.wasserstein.wasserstein_distance(d1, d2, order=1, internal_p=2, matching=True)
print("Dist:", dist)
print("Match:", match)
