from vpython import cos, sin, vector

# To avoid having VPython visualisations when testing other functions,
# we define these fake objects with the same attributes
class FakeAxle:
    def __init__(self, axle_pos):
        self.pos = axle_pos

class FakeBob:
    def __init__(self, bob_pos, bob_rad, bob_color, bob_texture):
        self.pos = bob_pos
        self.radius = bob_rad
        self.color = bob_color
        self.texture = bob_texture

class FakeCord:
    def __init__(self, cord_pos, cord_axis):
        self.pos = cord_pos
        self.axis = cord_axis

class FakePend:
    def __init__(self, axle_pos, r_param, theta, bob_color, bob_texture):
        self.axle = FakeAxle(axle_pos)
        
        bob_pos = self.axle.pos + r_param * vector(sin(theta), -cos(theta), 0)
        self.bob = FakeBob(bob_pos, r_param/15, bob_color, bob_texture)

        cord_axis = bob_pos - axle_pos
        self.cord = FakeCord(axle_pos, cord_axis)

        self.pendulum = (self.axle, self.bob, self.cord)
