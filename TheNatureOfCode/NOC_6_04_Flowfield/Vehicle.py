class Vehicle(object):
    """ generated source for class Vehicle """
    def __init__(self, l, ms, mf):
        """ generated source for method __init__ """
        self.location = l.get()
        self.r = 3.0
        self.maxspeed = ms
        self.maxforce = mf
        self.acceleration = PVector(0, 0)
        self.velocity = PVector(0, 0)

    def run(self):
        """ generated source for method run """
        self.update()
        self.borders()
        self.display()

    #  Implementing Reynolds' flow field following algorithm
    #  http://www.red3d.com/cwr/steer/FlowFollow.html
    def follow(self, flow):
        """ generated source for method follow """
        #  What is the vector at that spot in the flow field?
        desired = flow.lookup(self.location)
        #  Scale it up by maxspeed
        desired.mult(self.maxspeed)
        #  Steering is desired minus velocity
        steer = PVector.sub(desired, self.velocity)
        steer.limit(self.maxforce)
        #  Limit to maximum steering force
        self.applyForce(steer)

    def applyForce(self, force):
        """ generated source for method applyForce """
        #  We could add mass here if we want A = F / M
        self.acceleration.add(force)

    #  Method to update location
    def update(self):
        """ generated source for method update """
        #  Update velocity
        self.velocity.add(self.acceleration)
        #  Limit speed
        self.velocity.limit(self.maxspeed)
        self.location.add(self.velocity)
        #  Reset accelertion to 0 each cycle
        self.acceleration.mult(0)

    def display(self):
        """ generated source for method display """
        #  Draw a triangle rotated in the direction of velocity
        theta = self.velocity.heading2D() + radians(90)
        fill(175)
        stroke(0)
        pushMatrix()
        translate(self.location.x, self.location.y)
        rotate(theta)
        beginShape(TRIANGLES)
        vertex(0, -self.r * 2)
        vertex(-self.r, self.r * 2)
        vertex(self.r, self.r * 2)
        endShape()
        popMatrix()

    #  Wraparound
    def borders(self):
        """ generated source for method borders """
        if self.location.x < -self.r:
            self.location.x = width + self.r
        if self.location.y < -self.r:
            self.location.y = height + self.r
        if self.location.x > width + self.r:
            self.location.x = -self.r
        if self.location.y > height + self.r:
            self.location.y = -self.r
