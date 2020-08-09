"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object. So technically Bolt, which has a velocity,
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you
add new features to your game, such as power-ups.  If you are unsure about whether to
make a new class or not, please ask on Piazza.

Jolie Wei jw2493 Jacob Yetter jay53
5/6/19
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.
class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,x,y):
        """
        Initializes the Ship

        Parameter x: the horizontal coordinate of the ship's center
        Precondition: x is a integer or float

        Parameter y: the vertical coordinate of the ship's center
        Precondition: y is an integer or float
        """
        super().__init__(x=x,y=y,width=SHIP_WIDTH,
        height=SHIP_HEIGHT,source='icon.png')

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides_ship(self,bolts):
        """
        Returns True if the bolt was fired by the player and collides with this
        alien

        Parameter bolts: The list of bolts to loop through
        Precondition: bolts is a bolts attribute of wave
        """
        for bolt in bolts:
            right_corner_x=bolt.x+(BOLT_WIDTH/2)
            upper_corner_y=bolt.y+(BOLT_HEIGHT/2)
            left_corner_x=bolt.x-(BOLT_WIDTH/2)
            lower_corner_y=bolt.y-(BOLT_HEIGHT/2)
            if not bolt.isPlayerBolt():
                if self.contains(((right_corner_x,upper_corner_y)) or
                self.contains((right_corner_x,lower_corner_y)) or
                self.contains((left_corner_x, upper_corner_y)) or
                self.contains((left_corner_x, lower_corner_y))):
                    bolts.remove(bolt)
                    return True
        return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GSprite):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,x,y,source):
        """
        Initializes the Alien

        Parameter x: the horizontal coordinate of the alien's center
        Precondition: x is a integer or float

        Parameter y: the vertical coordinate of the alien's center
        Precondition: y is an integer or float

        Parameter source: the image of the alien
        Precondition: the source must be a string of a valid png file
        """
        super().__init__(x=x,y=y,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,
        source=source, format=(1,2))

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides_alien(self,bolts):
        """
        Returns: True if the bolt was fired by the player and collides with this
                 alien

        Parameter bolts: The list of bolts to loop through
        Precondition: bolts is a bolts attribute of wave
        """
        for bolt in bolts:
            right_edge=bolt.x+(BOLT_WIDTH/2)
            top_edge=bolt.y+(BOLT_HEIGHT/2)
            left_edge=bolt.x-(BOLT_WIDTH/2)
            bottom_edge=bolt.y-(BOLT_HEIGHT/2)

            if bolt.isPlayerBolt():
                if (self.contains((right_edge,top_edge)) or
                self.contains((right_edge,bottom_edge)) or
                self.contains((left_edge, top_edge)) or
                self.contains((left_edge, bottom_edge))):
                    bolts.remove(bolt)
                    return True
        return False


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles.  The size of the bolt is
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.

    The class Wave will need to look at these attributes, so you will need getters for
    them.  However, it is possible to write this assignment with no setters for the
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.

    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a
    helper.

    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.

    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    def get_velocity(self):
        """Getter that returns self._velocity"""
        return self._velocity

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,fillcolor,velocity):
        """Initializes the bolt
        Parameter x: the horizontal coordinate of the bolt's center
        Precondition: x is a integer or float

        Parameter y: the vertical coordinate of the bolt's center
        Precondition: y is an integer or float

        Parameter fillcolor: color of the bolt
        Precondition: fillcolor must be a string and a valid color name

        Parameter velocity: the velocity of the bolt in the y direction
        Precondition: velocity must be an integer or float
        """
        super().__init__(x=x,y=y,width=BOLT_WIDTH,height=BOLT_HEIGHT,
        fillcolor=fillcolor)
        self._velocity=velocity

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """Checks to see if the bolt is from the player or the alien"""
        if self._velocity>0:
            return True
        return False


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
class Defense_Barrier(GRectangle):
    """
    A Class representing a defense barrier.

    It allows the ship to have something to hide behind in order to not get
    hit by the alien's bolts

    The Barrier can absorb as many hits as its health
    """
    def get_health(self):
        """Returns an int that is the amount of health that the barrier has"""
        return self._health

    def __init__(self,x,y):
        """Initializes the defense barrier and gives it an attribute health

        Parameter x: hoorizontal coordinate of the defense barrier's center
        Precondition: x must be an integer or float

        Parameter y: vertical coordinate of the defense barrier's center
        Precodition: y must be an integer or float
        """
        super().__init__(x=x,y=y,width=SHIP_WIDTH*2,height=BOLT_HEIGHT*2,
        fillcolor='blue')
        self._health=10

    def decrease_health(self):
        """Decreases health of barrier by 1"""
        self._health-=1

    def barrier_collision(self,bolts):
        """Returns True if the bolt that hit the barrier was an alien bolt.
        Returns False if the bolt was a ship bolt. Removes the bolt from the
        screen if it hits the barrier, regardless of whether it was a player or
        alien bolt.

        Parameter bolts: The list of bolts to loop through
        Precondition: bolts is a bolts attribute of wave"""
        for bolt in bolts:
            right_edge=bolt.x+(BOLT_WIDTH/2)
            top_edge=bolt.y+(BOLT_HEIGHT/2)
            left_edge=bolt.x-(BOLT_WIDTH/2)
            bottom_edge=bolt.y-(BOLT_HEIGHT/2)

            if not bolt.isPlayerBolt():
                if (self.contains((right_edge,top_edge)) or
                self.contains((right_edge,bottom_edge)) or
                self.contains((left_edge, top_edge)) or
                self.contains((left_edge, bottom_edge))):
                    bolts.remove(bolt)
                    return True
            else:
                if (self.contains((right_edge,top_edge)) or
                self.contains((right_edge,bottom_edge)) or
                self.contains((left_edge, top_edge)) or
                self.contains((left_edge, bottom_edge))):
                    bolts.remove(bolt)
                    return False
        return False
