# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 10:50:59 2018

@author: sinkovitsd
"""

################## http://www.pygame.org/wiki/2DVectorClass ##################
### Modified by Daniel Sinkovits ###

import operator
import math

class Vec2d(object):
    """2d vector class, supports vector and scalar operators,
       and also provides a bunch of high level functions
       """
    __slots__ = ['x', 'y']

    def __init__(self, x_or_pair, y = None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y
            
    def int(self):
        return [int(self.x), int(self.y)]

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")

    def copy(self):
        return Vec2d(self)
    
    def copy_in(self, other):
        self.x = other.x
        self.y = other.y

    def zero(self):
        self.x = 0
        self.y = 0

    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec2d(%s, %s)' % (self.x, self.y)

    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        elif other == None:
            return False
        else:
            raise TypeError("Comparison of a vector with a non-vector.")
            return False

    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        elif other == None:
            return True
        else:
            raise TypeError("Comparison of a vector with a non-vector.")
            return True

    def __nonzero__(self):
        return bool(self.x or self.y)

    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a Vec2d"
        if isinstance(other, Vec2d):
            return Vec2d(f(self.x, other.x),
                         f(self.y, other.y))
        elif (hasattr(other, "__getitem__")):
            return Vec2d(f(self.x, other[0]),
                         f(self.y, other[1]))
        else:
            return Vec2d(f(self.x, other),
                         f(self.y, other))

    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a Vec2d"
        if (hasattr(other, "__getitem__")):
            return Vec2d(f(other[0], self.x),
                         f(other[1], self.y))
        else:
            return Vec2d(f(other, self.x),
                         f(other, self.y))

    def _io(self, other, f):
        "inplace operator"
        if (hasattr(other, "__getitem__")):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self

    # Addition
    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            return Vec2d(self.x + other, self.y + other)
    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Vec2d):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self

    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        elif (hasattr(other, "__getitem__")):
            return Vec2d(self.x - other[0], self.y - other[1])
        else:
            return Vec2d(self.x - other, self.y - other)
    def __rsub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(other.x - self.x, other.y - self.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(other[0] - self.x, other[1] - self.y)
        else:
            return Vec2d(other - self.x, other - self.y)
    def __isub__(self, other):
        if isinstance(other, Vec2d):
            self.x -= other.x
            self.y -= other.y
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self

    # Multiplication
    def __mul__(self, other):
        if hasattr(other, "__getitem__"):
            raise TypeError("Multiplication of a vector by a non-scalar.")
        else:
            return Vec2d(self.x*other, self.y*other)
    __rmul__ = __mul__

    def __imul__(self, other):
        if hasattr(other, "__getitem__"):
            raise TypeError("Multiplication of a vector by a non-scalar.")
        else:
            self.x *= other
            self.y *= other
        return self

    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        raise TypeError("Cannot divide by a vector.")
    def __idiv__(self, other):
        return self._io(other, operator.div)

    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return TypeError("Cannot divide by a vector.")
    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)

    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return TypeError("Cannot divide by a vector.")
    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)

    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        raise TypeError("Cannot modulo by a vector.")
  
    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)

    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)

    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__

    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__

    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__

    # Unary operations
    def __neg__(self):
        return Vec2d(operator.neg(self.x), operator.neg(self.y))

    def __pos__(self):
        return Vec2d(operator.pos(self.x), operator.pos(self.y))

    def __abs__(self):
        return Vec2d(abs(self.x), abs(self.y))

    def __invert__(self):
        return Vec2d(-self.x, -self.y)

    # vectory functions
    def get_length_sqrd(self):
        return self.x**2 + self.y**2
    mag2 = get_length_sqrd

    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)
    mag = get_length
    def __setlength(self, value):
        length = self.get_length()
        self.x *= value/length
        self.y *= value/length
    length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")

    def rotate(self, angle_degrees): # in-place function
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y

    def rotated(self, angle_degrees): # doesn't change vector
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Vec2d(x, y)

    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))
    
    def __setangle(self, angle_degrees):
        self.x = self.length
        self.y = 0
        self.rotate(angle_degrees)
    angle = property(get_angle, __setangle, None, "gets or sets the angle of a vector")

    def get_angle_between(self, other):
        cross = self.x*other[1] - self.y*other[0]
        dot = self.x*other[0] + self.y*other[1]
        return math.degrees(math.atan2(cross, dot))

    def normalized(self): # doesn't change vector
        length = self.length
        if length != 0:
            return self/length
        return Vec2d(self)
    hat = normalized

    def normalize_return_length(self): # in-place function
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        return length

    def perpendicular(self):
        return Vec2d(-self.y, self.x)

    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return Vec2d(-self.y/length, self.x/length)
        return Vec2d(self)

    def dot(self, other):
        return float(self.x*other[0] + self.y*other[1])

    def get_distance(self, other):
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)

    def get_dist_sqrd(self, other):
        return (self.x - other[0])**2 + (self.y - other[1])**2

    def projection(self, other):
        other_length_sqrd = other[0]*other[0] + other[1]*other[1]
        projected_length_times_other_length = self.dot(other)
        return other*(projected_length_times_other_length/other_length_sqrd)

    def cross(self, other): # equivalent to self.perpendicular().dot(other)
        return self.x*other[1] - self.y*other[0]

    def interpolate_to(self, other, range):
        return Vec2d(self.x + (other[0] - self.x)*range, self.y + (other[1] - self.y)*range)

    def convert_to_basis(self, x_vector, y_vector):
        return Vec2d(self.dot(x_vector)/x_vector.get_length_sqrd(), self.dot(y_vector)/y_vector.get_length_sqrd())

    def __getstate__(self):
        return [self.x, self.y]

    def __setstate__(self, dict):
        self.x, self.y = dict

########################################################################
## Unit Testing                                                       ##
########################################################################
if __name__ == "__main__":

    import unittest
    import pickle

    ####################################################################
    class UnitTestVec2D(unittest.TestCase):

        def setUp(self):
            pass

        def testCreationAndAccess(self):
            v = Vec2d(111,222)
            self.assertTrue(v.x == 111 and v.y == 222)
            v.x = 333
            v[1] = 444
            self.assertTrue(v[0] == 333 and v[1] == 444)

        def testMath(self):
            v = Vec2d(111,222)
            self.assertEqual(v + 1, Vec2d(112,223))
            self.assertTrue(v - 2 == [109,220])
            self.assertTrue(v * 3 == (333,666))
            self.assertTrue(v / 2.0 == Vec2d(55.5, 111))
            self.assertTrue(v / 2 == (55.5, 111))
            #self.assertTrue(v ** Vec2d(2,3) == [12321, 10941048])
            self.assertTrue(v + [-11, 78] == Vec2d(100, 300))
            self.assertTrue(v / [10,2] == [11.1,111])

        def testReverseMath(self):
            v = Vec2d(111,222)
            self.assertTrue(1 + v == Vec2d(112,223))
            self.assertTrue(2 - v == [-109,-220])
            self.assertTrue(3 * v == (333,666))
            #self.assertTrue([222,888] / v == [2,4])
            #self.assertTrue([111,222] ** Vec2d(2,3) == [12321, 10941048])
            self.assertTrue([-11, 78] + v == Vec2d(100, 300))

        def testUnary(self):
            v = Vec2d(111,222)
            v = -v
            self.assertTrue(v == [-111,-222])
            v = abs(v)
            self.assertTrue(v == [111,222])

        def testLength(self):
            v = Vec2d(3,4)
            self.assertTrue(v.length == 5)
            self.assertTrue(v.get_length_sqrd() == 25)
            self.assertTrue(v.normalize_return_length() == 5)
            self.assertTrue(v.length == 1)
            v.length = 5
            self.assertTrue(v == Vec2d(3,4))
            v2 = Vec2d(10, -2)
            self.assertTrue(v.get_distance(v2) == (v - v2).get_length())

        def testAngles(self):
            v = Vec2d(0, 3)
            self.assertEqual(v.angle, 90)
            v2 = Vec2d(v)
            v.rotate(-90)
            self.assertEqual(v.get_angle_between(v2), 90)
            v2.angle -= 90
            self.assertEqual(v.length, v2.length)
            self.assertEqual(v2.angle, 0)
            self.assertEqual(v2, [3, 0])
            self.assertTrue((v - v2).length < .00001)
            self.assertEqual(v.length, v2.length)
            v2.rotate(300)
            self.assertAlmostEqual(v.get_angle_between(v2), -60)
            v2.rotate(v2.get_angle_between(v))
            angle = v.get_angle_between(v2)
            self.assertAlmostEqual(v.get_angle_between(v2), 0)

        def testHighLevel(self):
            basis0 = Vec2d(5.0, 0)
            basis1 = Vec2d(0, .5)
            v = Vec2d(10, 1)
            self.assertTrue(v.convert_to_basis(basis0, basis1) == [2, 2])
            self.assertTrue(v.projection(basis0) == (10, 0))
            self.assertTrue(basis0.dot(basis1) == 0)

        def testCross(self):
            lhs = Vec2d(1, .5)
            rhs = Vec2d(4,6)
            self.assertTrue(lhs.cross(rhs) == 4)

        def testComparison(self):
            int_vec = Vec2d(3, -2)
            flt_vec = Vec2d(3.0, -2.0)
            zero_vec = Vec2d(0, 0)
            self.assertTrue(int_vec == flt_vec)
            self.assertTrue(int_vec != zero_vec)
            self.assertTrue((flt_vec == zero_vec) == False)
            self.assertTrue((flt_vec != int_vec) == False)
            self.assertTrue(int_vec == (3, -2))
            self.assertTrue(int_vec != [0, 0])
            #self.assertTrue(int_vec != 5)
            #self.assertTrue(int_vec != [3, -2, -5])

        def testInplace(self):
            inplace_vec = Vec2d(5, 13)
            inplace_ref = inplace_vec
            inplace_src = Vec2d(inplace_vec)
            inplace_vec *= .5
            inplace_vec += .5
            inplace_vec /= (3, 6)
            inplace_vec += Vec2d(-1, -1)
            self.assertEqual(inplace_vec, inplace_ref)

        def testPickle(self):
            testvec = Vec2d(5, .3)
            testvec_str = pickle.dumps(testvec)
            loaded_vec = pickle.loads(testvec_str)
            self.assertEqual(testvec, loaded_vec)

    ####################################################################
    unittest.main()

    ########################################################################

"""
for i in range(n)
make random radius between 0.1, 0.8
mass = r * r
append circle


for i in range max collisions
collide = false
    for all particles check collision
        if collide(a, b, dt):
                collided = true
if not collided: // if collisions are false then it breaks
    break


collide(a, b, dt)
circle and circle => collide particles
circle and wall => collide wall(circle, wall)
wall and circle => collide wall(wall, circle)

t = n.perp
a.pos += d*n*m/a.mass
b.pos -= d*n*m/b.mass

d = a.radius - r.dot(n)
m = a.mass * b.mass / (a.mass + b.mass)

vel_diff = particle.vel - wall.vel
if vel_diff.dot(n) < 0:
  j = J*n
   a.mom += j
   b.mom -= j
a.update_vel()
b.update_vel()
"""