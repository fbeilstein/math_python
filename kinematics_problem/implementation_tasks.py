import numpy as np
import math

class Dual:
    """Dual number: a + b*eps where eps^2 = 0."""
    def __init__(self, real, dual):
        self.real = float(real)
        self.dual = float(dual)

    def __repr__(self):
        return f"Dual({self.real}, {self.dual})"

    def __add__(self, other):
        if isinstance(other, Dual):
            return Dual(self.real + other.real, self.dual + other.dual)
        return Dual(self.real + other, self.dual)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Dual):
            return Dual(self.real - other.real, self.dual - other.dual)
        return Dual(self.real - other, self.dual)

    def __rsub__(self, other):
        return Dual(other - self.real, -self.dual)

    def __mul__(self, other):
        if isinstance(other, Dual):
            # (a + b e)(c + d e) = ac + (ad + bc)e + bd e^2
            # Since e^2 = 0: ac + (ad + bc)e
            return Dual(self.real * other.real, self.real * other.dual + self.dual * other.real)
        return Dual(self.real * other, self.dual * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Dual):
            # (a + be) / (c + de) = (a + be)(c - de) / c^2 = (ac + (bc - ad)e) / c^2
            c = other.real
            if c == 0:
                raise ZeroDivisionError("Division by zero in dual part")
            return Dual(self.real / c, (self.dual * c - self.real * other.dual) / (c * c))
        return Dual(self.real / other, self.dual / other)

    def __rtruediv__(self, other):
        c = self.real
        if c == 0:
            raise ZeroDivisionError("Division by zero in dual part")
        return Dual(other / c, (-other * self.dual) / (c * c))
        
    def __pow__(self, power):
        # (a + b e)^n = a^n + n a^{n-1} b e
        if isinstance(power, Dual):
            raise NotImplementedError("Dual to the power of Dual not implemented")
        return Dual(self.real ** power, power * (self.real ** (power - 1)) * self.dual)

# Transcendental functions for Dual Numbers
def sin(x):
    if isinstance(x, Dual):
        return Dual(math.sin(x.real), math.cos(x.real) * x.dual)
    return math.sin(x)

def cos(x):
    if isinstance(x, Dual):
        return Dual(math.cos(x.real), -math.sin(x.real) * x.dual)
    return math.cos(x)

def tan(x):
    if isinstance(x, Dual):
        cos_val = math.cos(x.real)
        return Dual(math.tan(x.real), x.dual / (cos_val * cos_val))
    return math.tan(x)

def exp(x):
    if isinstance(x, Dual):
        e_val = math.exp(x.real)
        return Dual(e_val, e_val * x.dual)
    return math.exp(x)

def log(x):
    if isinstance(x, Dual):
        return Dual(math.log(x.real), x.dual / x.real)
    return math.log(x)

class SplitComplex:
    """Split-complex number: a + b*j where j^2 = 1."""
    def __init__(self, real, j):
        self.real = float(real)
        self.j = float(j)

    def __repr__(self):
        return f"SplitComplex({self.real}, {self.j})"

    def __add__(self, other):
        if isinstance(other, SplitComplex):
            return SplitComplex(self.real + other.real, self.j + other.j)
        return SplitComplex(self.real + other, self.j)

    def __mul__(self, other): #contains solution
        if isinstance(other, SplitComplex):
            # (a + bj)(c + dj) = ac + bd + (ad + bc)j
            return SplitComplex(self.real * other.real + self.j * other.j,
                                self.real * other.j + self.j * other.real)
        return SplitComplex(self.real * other, self.j * other)

class Quaternion:
    """Standard Quaternion: q = w + xi + yj + zk."""
    def __init__(self, w, x, y, z):
        self.w, self.x, self.y, self.z = map(float, (w, x, y, z))

    def __repr__(self):
        return f"Q({self.w}, {self.x}, {self.y}, {self.z})"
        
    def __add__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)
        return Quaternion(self.w + other, self.x, self.y, self.z)

    def __mul__(self, other): #contains solution
        if isinstance(other, Quaternion):
            w1, x1, y1, z1 = self.w, self.x, self.y, self.z
            w2, x2, y2, z2 = other.w, other.x, other.y, other.z
            w = w1*w2 - x1*x2 - y1*y2 - z1*z2
            x = w1*x2 + x1*w2 + y1*z2 - z1*y2
            y = w1*y2 - x1*z2 + y1*w2 + z1*x2
            z = w1*z2 + x1*y2 - y1*x2 + z1*w2
            return Quaternion(w, x, y, z)
        return Quaternion(self.w * other, self.x * other, self.y * other, self.z * other)
        
    def __rmul__(self, other):
        return Quaternion(self.w * other, self.x * other, self.y * other, self.z * other)

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)
        
    def norm(self):
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
        
    def normalized(self):
        n = self.norm()
        if n == 0: return self
        return Quaternion(self.w/n, self.x/n, self.y/n, self.z/n)

class DualQuaternion:
    """Dual Quaternion: Q = q_r + q_d * epsilon."""
    def __init__(self, qr, qd):
        self.qr = qr
        self.qd = qd

    def __repr__(self):
        return f"DualQ({self.qr}, {self.qd})"

    def __add__(self, other):
        return DualQuaternion(self.qr + other.qr, self.qd + other.qd)

    def __mul__(self, other): #contains solution
        if isinstance(other, DualQuaternion):
            # (Ar + Ad e)(Br + Bd e) = ArBr + (ArBd + AdBr)e
            return DualQuaternion(self.qr * other.qr, self.qr * other.qd + self.qd * other.qr)
        # Scalar multiplication
        return DualQuaternion(self.qr * other, self.qd * other)
        
    def conjugate(self):
        # Q* = qr* + qd* e
        return DualQuaternion(self.qr.conjugate(), self.qd.conjugate())
        
    def normalized(self):
        mag = self.qr.norm()
        if mag == 0: return self
        # Normalization: Q / ||Q||. ||Q|| = ||qr|| + (qr . qd / ||qr||) e
        # To invert ||Q||: 1 / (a + be) = (1/a) - (b/a^2)e
        a = mag
        dot = self.qr.w * self.qd.w + self.qr.x * self.qd.x + self.qr.y * self.qd.y + self.qr.z * self.qd.z
        b = dot / a
        inv_a = 1.0 / a
        inv_b = -b / (a * a)
        
        # (qr + qd e) * (inv_a + inv_b e) = qr * inv_a + (qr * inv_b + qd * inv_a) e
        new_qr = self.qr * inv_a
        new_qd = self.qr * inv_b + self.qd * inv_a
        return DualQuaternion(new_qr, new_qd)

    @staticmethod
    def from_translation_rotation(translation, rotation_quat):
        """
        Create a Dual Quaternion from a 3D translation vector (tx, ty, tz) and a rotation quaternion.
        qd = 0.5 * (0, tx, ty, tz) * qr
        """
        tx, ty, tz = translation
        t_quat = Quaternion(0, tx, ty, tz)
        qd = (t_quat * rotation_quat) * 0.5
        return DualQuaternion(rotation_quat, qd)

    def to_translation_rotation(self): #contains solution
        """Returns (translation, rotation_quat)"""
        # translation: t = 2 * qd * qr*
        t_quat = self.qd * self.qr.conjugate() * 2.0
        return (t_quat.x, t_quat.y, t_quat.z), self.qr

def sclerp(dq1, dq2, t): #contains solution
    """
    Screw Linear Interpolation between two unit Dual Quaternions.
    dq(t) = dq1 * (dq1^-1 * dq2)^t
    For simpler calculation (when angles are small and shortest path is fine):
    dq(t) = normalize(dq1 * (1-t) + dq2 * t)
    """
    # Using shortest path iterative blending for visual demonstration
    dot = dq1.qr.w * dq2.qr.w + dq1.qr.x * dq2.qr.x + dq1.qr.y * dq2.qr.y + dq1.qr.z * dq2.qr.z
    if dot < 0:
        dq2 = DualQuaternion(dq2.qr * -1.0, dq2.qd * -1.0)
    
    res = dq1 * (1.0 - t) + dq2 * t
    return res.normalized()
