"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

Jolie Wei jw2493 Jacob Yetter jay53
5/6/19
"""
from consts import *
from game2d import *
from wave import *

# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py
class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]
    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _score_label: text displaying "Score:" and the current score of the player
                      [GLabel]
        _lives_counter: text displaying "Lives:" and the current number of lives
                        of the player [GLabel]
        _restart_text: text displayed before the second or third wave is created
                       [GLabel or None if player doesn't make it to the second
                       or third wave]
        _Defense_Barrier_health: text displaying "Barrier Health:" and the
                        current number of hits the barrier can still take[GLabel]
        _carry_over_score: the player's cumulative score for all the waves they
                           play [int]
        _wave_number: the number of waves that have been created [int]

        _volume: text displaying instructions on which button to press to mute
                 the pop and pew sounds [GLabel]
        _other_volume: text displaying instructions on which button to press to
                       unmute the pop and pew sounds [GLabel]
    """
    # DO NOT MAKE A NEW INITIALIZER!
    def get_wave_num(self):
        """A Getter to return the wave number"""
        return self._wave_number

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        self._wave=None
        self._text=GLabel(text="Press 'S' to play", font_name='RetroGame',
        x=400, y=350)
        self._state=STATE_INACTIVE
        self._score_label=GLabel(text="Score: ", font_name='RetroGame',
        font_size=20, x=100, y=650)
        self._lives_counter=GLabel(text="Lives: ", font_name='RetroGame',
        font_size=20,x=700, y=650)
        self._restart_text=GLabel(text="", font_name='RetroGame',
        x=400, y=250)
        self._Defense_Barrier_health=GLabel(text="Barrier Health: ",font_size=20,
        font_name='RetroGame', x=400, y=650)
        self._carry_over_score=0
        self._wave_number=1
        self._volume=GLabel(text="Press 0 to mute pew and pop sounds",
        font_name='RetroGame',font_size=20,x=400, y=100)
        self._other_volume=GLabel(text="Press 1 to unmute pew and pop sounds",
        font_name='RetroGame',font_size=20, x=400, y=50)

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state==STATE_INACTIVE:
            self.state_INACTIVE(input)
        elif self._state==STATE_NEWWAVE:
            self.state_NEWWAVE()
        elif self._state==STATE_ACTIVE:
            self.state_ACTIVE(input,dt)
        elif self._state==STATE_PAUSED:
            self.state_PAUSED(input)
        elif self._state==STATE_CONTINUE:
            self.state_CONTINUE()
        elif self._state==STATE_COMPLETE:
            self.state_COMPLETE(input)

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        self._score_label.draw(self.view)
        self._lives_counter.draw(self.view)
        self._Defense_Barrier_health.draw(self.view)
        if (self._state==STATE_INACTIVE or
        self._state==STATE_COMPLETE):
            self._text.draw(self.view)
            self._volume.draw(self.view)
            self._other_volume.draw(self.view)
        elif self._state==STATE_PAUSED:
            self._wave.draw(self.view)
            self._text.draw(self.view)
        else:
            if self._wave !=None:
                self._wave.draw(self.view)
        if self._state==STATE_COMPLETE and self._restart_text!=None:
            self._restart_text.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def state_INACTIVE(self,input):
        """STATE_INACTIVE is the state that the game starts out in.
        The Player has to press S to start the game

        Parameter input: the user input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        self._text=GLabel(text="Press 'S' to play", font_name='RetroGame',
        x=400, y=350)
        if self.input.is_key_down('s'):
            self._state=STATE_NEWWAVE

    def state_NEWWAVE(self):
        """STATE_NEWWAVE is the state where the wave is created.
        The speed of the wave depends on the _wave_number
        """
        self._wave=Wave(self.input)
        self._state=STATE_ACTIVE
        self._wave.set_speed(self._wave_number-1)

    def state_ACTIVE(self,input,dt):
        """STATE_ACTIVE is the state where the player is playing the game.
        The wave is constantly being updated to show what is changing.
        The player may press 'p' to pause at any time.

        Parameter input: the user input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._wave.update(self.input,dt)
        if self._wave.check_lives() and self._wave.no_ship_exists():
            self._state=STATE_PAUSED

        if self._wave.check_game_over():
            self._state=STATE_COMPLETE

        if self.input.is_key_down('p'):
            self._state=STATE_PAUSED

        self._score_label=GLabel(text="Score: " +
        str(self._carry_over_score+self._wave.get_count()),font_name='RetroGame',
        font_size=20, x=100, y=650)

        self._lives_counter=GLabel(text="Lives: " +
        str(self._wave.get_lives()), font_name='RetroGame',
        font_size=20,x=700, y=650)

        self._Defense_Barrier_health=GLabel(text="Barrier Health: " +
        str(self._wave.get_defense_barrier_health()), font_name='RetroGame',
        font_size=20, x=400, y=650)

    def state_PAUSED(self,input):
        """"In STATE_PAUSED the player must press 'S' to return to game

        Parameter input: the user input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        self._text=GLabel(text="Press 'S' to continue", font_name='RetroGame',
        x=400, y=350)
        if self.input.is_key_down('s'):
            self._state=STATE_CONTINUE

    def state_CONTINUE(self):
        """STATE_CONTINUE is a short state that is in between STATE_PAUSED
        and STATE_ACTIVE. It creates another ship if you have just been shot.
        """
        self._wave.create_another_ship()
        self._state=STATE_ACTIVE

    def state_COMPLETE(self,input):
        """In STATE_COMPLETE the player has either lost the game, is going to
        continue to the next wave, or has won the game. The screen displays
        a message according to what situation the player is in.

        Parameter input: the user input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        if self._wave.check_win():
            if self._wave_number==1:
                self.wave_1(input)
            elif self._wave_number==2:
                self.wave_2(input)
            elif self._wave_number==3:
                self.wave_3()
        else:

            self._text=GLabel(text="You Lose :(", font_name='RetroGame',
            x=400, y=350)
            self._restart_text=None

        self._score_label=GLabel(text="Score: " +
        str(self._carry_over_score+self._wave.get_count()),font_name='RetroGame',
        font_size=20, x=100, y=650)
        self._lives_counter=GLabel(text="Lives: " +
        str(self._wave.get_lives()), font_name='RetroGame', font_size=20,
        x=700, y=650)

    def wave_1(self,input):
        """When the Player beats the first wave, this method allows
        the player to press 'n' in order to create another wave of aliens,
        which will be at a faster speed. Their score from the first wave carries
        over into the next wave.

        Parameter input: the user input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        self._text=GLabel(text="You Beat First Wave!", font_name='RetroGame',
        x=400, y=350)
        self._restart_text=GLabel(text="Press 'N' to start Second Wave",
        font_name='RetroGame',x=400, y=250)
        if self.input.is_key_down('n'):
            self._carry_over_score=self._wave.get_count()
            self._wave_number+=1
            self._wave.set_speed(1)
            self._state=STATE_NEWWAVE

    def wave_2(self,input):
        """When the Player beats the second wave, this methods allows the player
        to press 'n' in order to create another wave of aliens, which will be at
        a faster speed. Their score from the first and second wave carries over
        into the third wave.

        Parameter input: the user input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        self._text=GLabel(text="You Beat Second Wave!", x=400, y=350)
        self._restart_text=GLabel(text="Press 'N' to start Thrid Wave",
        font_name='RetroGame', x=400, y=250)
        if self.input.is_key_down('n'):
            self._carry_over_score+=self._wave.get_count()
            self._wave_number+=1
            self._wave.set_speed(2)
            self._state=STATE_NEWWAVE

    def wave_3(self):
        """If the player defeats the third wave, this method displays a
        congratulatory message onto the screen"""
        self._text=GLabel(text="You Win!", font_name='RetroGame', x=400, y=350)
        self._restart_text=None
