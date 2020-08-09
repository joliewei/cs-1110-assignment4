"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

Jolie Wei jw2493 Jacob Yetter jay53
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary. It
    also marches the aliens back and forth across the screen until they are all
    destroyed or they reach the defense line (at which point the player loses).
    When the wave is complete, you should create a NEW instance of Wave
    (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update. See subcontrollers.py from Lecture 24 for an example. This class
    will be similar to than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien
        or None]
        _bolts:  the laser bolts currently on screen
        [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
        _direction: The direction the alien wave is moving
        [string 'right' or 'left']
        _number_of_steps: rate that the aliens should fire at the ship
        [random integer between 1 and BOLT_RATE]
        _count: This is the score which is the number of aliens you have shot
        [integer]
        muted: whether the

    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_bolts(self):
         """returns the bolts attribute"""
         return self._bolts

    def get_count(self):
        """Getter that returns self._count"""
        return self._count

    def get_lives(self):
        """Getter that returns self._lives"""
        return self._lives

    def set_speed(self,input):
        """This setter allows the aliens speed to increase
        This is called when a the next wave starts

        Parameter input: the user input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        self._speed= self._speed * (.4**input)

    def get_defense_barrier_health(self):
        """Returns the defense barrier health"""
        if self._Defense_Barrier!=None:
            return self._Defense_Barrier.get_health()

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self, input):
        """
        Initializes a wave

        Parameter input: the user input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        self._aliens=self.list_aliens()
        self._ship=Ship(x=GAME_WIDTH/2,y=SHIP_BOTTOM)
        self._dline=GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
        linewidth=2,linecolor='black')
        self._time=0
        self._direction='right'
        self._bolts=[]
        self.number_of_steps=random.randrange(1,BOLT_RATE)
        self._lives=3
        self._count=0
        self.muted=False
        self.last_key_pressed=None
        self._Defense_Barrier=Defense_Barrier(x=400,y=DEFENSE_LINE+50)
        self._speed=ALIEN_SPEED
        self.backgroundSound=Sound('FullSizeRender.wav')
        self.backgroundSound.volume=.7
        self.backgroundSound.play(loop=True)

    #creating alien list
    def list_aliens(self):
        """
        Fills _aliens attribute with aliens
        """
        final_list=[]
        for i in range(ALIEN_ROWS):
            small_list=[]
            for j in range(ALIENS_IN_ROW):
                if ((ALIEN_ROWS-i-1)//2)%3 ==0:
                    image=ALIEN_IMAGES[0]
                elif ((ALIEN_ROWS-i-1)//2)%3==1:
                    image=ALIEN_IMAGES[1]
                elif ((ALIEN_ROWS-i-1)//2)%3==2:
                    image=ALIEN_IMAGES[2]
                alien=Alien(x=(ALIEN_H_SEP+ALIEN_WIDTH)*(j+1),y=
                (GAME_HEIGHT-ALIEN_CEILING)-((ALIEN_HEIGHT+ALIEN_V_SEP)*(i+1)),
                source=image)
                small_list.append(alien)
            final_list.append(small_list)
        return final_list

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """Updates the Ship, Aliens, and Laser Bolts.

        Parameter input: the user input, used to control the ship and change state
        Precodition: instance of GInput; it is inherited from GameApp

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a number (float or int)
        """
        self.create_ship_bolt(input,self.sound_ship())
        self.create_alien_bolt()
        self.give_bolt_speed()
        self.move_ship(input)
        self.move_aliens(dt)
        self.collision_ship()
        self.collision_alien()
        if self._Defense_Barrier!=None:
            self.is_barrier_hit()
        self.score_count()
        self.stop_sound(input)

    #creating alien and ship bolts
    def create_ship_bolt(self,input,sound):
        """Creates a bolt that comes out of the ship. Only creates the bolt if
        there is no bolt on the screen that is already shooting from the ship.
        Adds bolt to the list of bolts in self._bolts. Creates pew sound after
        each bolt is created.

        Parameter input: the user input, used to control the ship and change state
        Precondition: input is an instance of GInput; it is inherited from GameApp

        Parameter sound: The different pew or pop sound that plays, depending on
        which row the alien is hit or which direction the alien is moving
        Precodition: sound is a string of a valid sound file

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a number (float or int)
        """
        if input.is_key_down('x') and self.last_key_pressed!='x':
            if self._bolts==[]:
                self._bolts+=[Bolt(x=self._ship.x,y=SHIP_HEIGHT+BOLT_HEIGHT,
                fillcolor='pink',velocity=BOLT_SPEED)]
                if self.muted==False:
                    pewSound=Sound(sound)
                    pewSound.play()
                    pewSound.volume=.4
            else:
                for bolt in self._bolts:
                    if bolt.isPlayerBolt():
                        return
                if self._ship!=None:
                    self._bolts+=[Bolt(x=self._ship.x,y=SHIP_HEIGHT+BOLT_HEIGHT,
                    fillcolor='pink',velocity=BOLT_SPEED)]
                    if self.muted==False:
                        pewSound=Sound(sound)
                        pewSound.play()
                        pewSound.volume=.4
        if input.is_key_down('x'):
            self.last_key_pressed='x'
        else:
            self.last_key_pressed=None

    def create_alien_bolt(self):
        """Creates a bolt that comes out of a random alien on the bottom row of
        the alien wave. Alien shoots randomly based on a number in between one
        and the bolt rate. Adds bolt to the list of bolts in self._bolts
        """

        if self.number_of_steps <=0:
            random_alien=self.pick_alien()
            self._bolts+=[Bolt(x=random_alien.x,
            y=random_alien.y-(ALIEN_HEIGHT/2),
            fillcolor='pink',velocity=-BOLT_SPEED)]
            self.number_of_steps=random.randrange(1,BOLT_RATE)

    def give_bolt_speed(self):
        """Moves the bolt either down or up the screen depending on whether it's
        coming from an alien or the ship"""

        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                bolt.y+=BOLT_SPEED
            else:
                bolt.y-=BOLT_SPEED

            if bolt.y>GAME_HEIGHT:
                self._bolts.remove(bolt)

    #picking random alien
    def pick_alien(self):
        """Picks a column of the alien wave randomly and chooses an alien from
        the bottom row of that column, given that the alien isn't None"""
        lst=[]
        for i in range(ALIENS_IN_ROW-1, -1, -1):
            for j in range(ALIEN_ROWS-1, -1, -1):
                if self._aliens[j][i] != None:
                    lst.append(self._aliens[j][i])
                    break
        column=random.randrange(0,len(lst))
        random_alien=lst[column]

        return random_alien

    #moves ship across screen
    def move_ship(self,input):
        """Moves the ship right if the player presses the right arrow until the
        ship reaches the edge of the game screen. Moves the ship left if the
        player presses the left arrow until the ship reaches the edge of the
        game screen.

        Parameter input: the user input, used to control the ship and change state
        Precondition: input is an instance of GInput; it is inherited from GameApp
        """
        min=0
        max=GAME_WIDTH
        if self._ship!=None:
            if input.is_key_down('left'):
                self._ship.x -= SHIP_MOVEMENT
            if input.is_key_down('right'):
                self._ship.x += SHIP_MOVEMENT
            if self._ship.x <= SHIP_WIDTH/2+min:
                self._ship.x=SHIP_WIDTH/2+min
            if self._ship.x >= max-SHIP_WIDTH/2:
                self._ship.x=max-SHIP_WIDTH/2

    def move_aliens(self,dt):
        """Moves the wave of aliens right until it hits the edge of the screen.
        Then, it moves the aliens down by ALIEN_V_WALK. Then, it moves the alien
        to the left until it hits the edge of the screen. Repeats in a zig zag

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._direction=='right':
            self.aliens_move_right(dt)
        elif self._direction=='left':
            self.aliens_move_left(dt)

    #alien helper functions
    def aliens_move_right(self,dt):
        """Helper function that moves the alien to the right until it hits
        the egde of the screen. Once the alien hits the edge of the screen,
        the wave of alien moves down and the direction is set to left.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._time >= self._speed:
            move_down=False
            self.number_of_steps-=1
            for list in self._aliens:
                for alien in reversed(list):
                    if alien!=None:
                        if move_down:
                            alien.y-=ALIEN_V_WALK
                        elif (alien.x + ALIEN_H_WALK+(ALIEN_WIDTH/2) >=
                        GAME_WIDTH-ALIEN_H_SEP):
                            alien.y-=ALIEN_V_WALK
                            move_down=True

                            self._direction='left'
                        else:
                            alien.x += ALIEN_H_WALK
                            alien.frame = (alien.frame+1) % 2
                        self.collision_alien()
                    self._time=0
        else:
            self._time+=dt

    def aliens_move_left(self,dt):
        """Helper function that moves the alien to the left until it hits
        the egde of the screen. Once the alien hits the edge of the screen,
        the wave of alien moves down and the direction is set to right.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._time >= self._speed:
            move_down=False
            self.number_of_steps-=1
            for list in self._aliens:
                for alien in list:
                    if alien!=None:
                        if move_down:
                            alien.y-=ALIEN_V_WALK
                        elif (alien.x - ALIEN_H_WALK - (ALIEN_WIDTH/2) <=
                        ALIEN_H_SEP):
                            alien.y-=ALIEN_V_WALK
                            move_down=True
                            self._direction='right'
                        else:
                            alien.x -= ALIEN_H_WALK
                            alien.frame = (alien.frame+1) % 2
                        self.collision_alien()
            self._time=0
        else:
            self._time+=dt

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the game objects to the view.

        Parameter view: the game view, used in drawing
        Precondition: instance of GView; it is inherited from GameApp
        """
        # IMPLEMENT ME
        for row in self._aliens:
            for i in row:
                if i!=None:
                    i.draw(view)

        if self._ship!=None:
            self._ship.draw(view)
        self._dline.draw(view)
        for bolt in self._bolts:
            if bolt!=None:
                bolt.draw(view)
        if self._Defense_Barrier!=None:
            self._Defense_Barrier.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def collision_alien(self):
        """
        Sets alien equal to none if hit by bolt. Also plays pop sound for each
        alien that gets set to None.
        """
        for j in range(ALIEN_ROWS):
            for i in range(len(self._aliens[j])):
                if self._aliens[j][i]!=None:
                    if self._aliens[j][i].collides_alien(self.get_bolts()):
                        self._aliens[j][i] = None
                        if self.muted==False:
                            row=j
                            popSound=Sound(self.sound_alien(row))
                            popSound.play()
                            popSound.volume=.4
                        return

    def collision_ship(self):
        """
        Sets ship equal to None if hit by bolt. Also subtracts ship lives by 1
        """
        if self._ship and self._ship.collides_ship(self.get_bolts()):
            self._ship=None
            self._lives-=1

    def create_another_ship(self):
        """Creates another ship if player still has more lives left"""
        if self._lives>0 and self._ship==None:
            self._ship=Ship(x=GAME_WIDTH/2,y=SHIP_BOTTOM)

    def check_lives(self):
        "Returns True if player has 1 or 2 lives left, returns False otherwise"
        if self._lives==1 or self._lives==2:
            return True
        else:
            return False

    def check_game_over(self):
        """Returns True if game is over, returns False otherwise.
        """
        if (self._lives<=0 or self.check_alien_wave() or
        self.alien_defense_line()):
            return True
        else:
            return False

    def check_alien_wave(self):
        """Returns True if all aliens have been killed,
        returns False otherwise"""
        for lst in self._aliens:
            for alien in lst:
                if alien!=None:
                    return False
        return True

    def alien_defense_line(self):
        """Returns True if alien wave has touched the defense line,
        returns False otherwise"""
        for lst in self._aliens:
            for alien in lst:
                if alien!=None:
                    if alien.y-(ALIEN_HEIGHT/2)<=DEFENSE_LINE:
                        return True
        return False

    def check_win(self):
        """Returns True if player has won, returns False if player has lost"""
        return self.check_alien_wave()

    def no_ship_exists(self):
        """Checks to see if the ship is None or not,
        returns True if ship is None"""
        if self._ship == None:
            return True
        else:
            return False

    def is_barrier_hit(self):
        """Checks to see if barrier is hit by a bolt. If health is 0,
        then the barrier is destroyed and removed from screen"""
        if self._Defense_Barrier.barrier_collision(self._bolts):
            self._Defense_Barrier.decrease_health()
        if self._Defense_Barrier.get_health()==0:
            self._Defense_Barrier=None

    def score_count(self):
        """Increments score everytime an alien gets shot and becomes None"""
        sum=0
        for i in range(ALIENS_IN_ROW-1, -1, -1):
            for j in range(ALIEN_ROWS-1, -1, -1):
                if self._aliens[j][i] == None:
                    sum+=1
        self._count=sum

    #fun extensions
    def stop_sound(self,input):
        """Sets mute attribute to True or False depending on if '0' or '1' is
        being pressed

        Parameter input: the user input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        if input.is_key_down('0'):
            self.muted=True
        elif input.is_key_down('1'):
            self.muted=False

    def sound_alien(self,row):
        """Returns the pop sound for when the alien gets shot.
        Different colored aliens have different pop sounds.

        Parameter row: the alien's row number
        Precodition: row must be an integer
        """
        if ((ALIEN_ROWS-row-1)//2)%3 ==0:
            sound='pop2.wav'
        elif ((ALIEN_ROWS-row-1)//2)%3==1:
            sound='pop1.wav'
        elif ((ALIEN_ROWS-row-1)//2)%3==2:
            sound='pop2.wav'
        return sound

    def sound_ship(self):
        """Returns the pew sound for when the ship fires a bolt.
        The pew sound alternates depending on which direction the aliens are
        moving. If the aliens are moving right, the sound is pew1.wav. If the
        aliens are moving left, the sound is pew2.wav.
        """
        if self._direction=='right':
            sound='pew1.wav'
        elif self._direction=='left':
            sound='pew2.wav'
        return sound
