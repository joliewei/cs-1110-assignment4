"""
A module to draw cool shapes with the introcs Turtle.

The module can be run as a script to show off the various functions. Unimplemented
functions will do nothing.

Jolie Wei jw2493
3/25/19
"""
from introcs.turtle import Window, Turtle, Pen
import introcs  # For the RGB and HSV objects
import math     # For the math computations


################# Helpers for Precondition Verification #################

def is_number(x):
    """
    Returns: True if value x is a number; False otherwise.

    Parameter x: the value to check
    Precondition: NONE (x can be any value)
    """
    return type(x) in [float, int]


def is_window(w):
    """
    Returns: True if w is a cornell Window; False otherwise.

    Parameter w: the value to check
    Precondition: NONE (w can be any value)
    """
    return type(w) == Window


def is_valid_color(c):
    """
    Returns: True c is a valid turtle color; False otherwise

    Parameter c: the value to check
    Precondition: NONE (c can be any value)
    """
    return (type(c) == introcs.RGB or type(c) == introcs.HSV or
            (type(c) == str and (introcs.is_tkcolor(c) or introcs.is_webcolor(c))))


def is_valid_speed(sp):
    """
    Returns: True if sp is an int in range 0..10; False otherwise.

    Parameter sp: the value to check
    Precondition: NONE (sp can be any value)
    """
    return (type(sp) == int and 0 <= sp and sp <= 10)


def is_valid_length(side):
    """
    Returns: True if side is a number >= 0; False otherwise.

    Parameter side: the value to check
    Precondition: NONE (side can be any value)
    """
    return (is_number(side) and 0 <= side)


def is_valid_iteration(n):
    """
    Returns: True if n is an int >= 1; False otherwise.

    Parameter n: the value to check
    Precondition: NONE (n can be any value)
    """
    return (type(n) == int and 1 <= n)


def is_valid_depth(d):
    """
    Returns: True if d is an int >= 0; False otherwise.

    Parameter d: the value to check
    Precondition: NONE (d can be any value)
    """
    return (type(d) == int and d >= 0)


def is_valid_turtlemode(t):
    """
    Returns: True t is a Turtle with drawmode True; False otherwise.

    Parameter t: the value to check
    Precondition: NONE (t can be any value)
    """
    return (type(t) == Turtle and t.drawmode)


def is_valid_penmode(p):
    """
    Returns: True t is a Pen with solid False; False otherwise.

    Parameter p: the value to check
    Precondition: NONE (p can be any value)
    """
    return (type(p) == Pen and not p.solid)


def report_error(message, value):
    """
    Returns: An error message about the given value.

    This is a function for constructing error messages to be used in assert statements.
    We find that students often introduce bugs into their assert statement messages, and
    do not find them because they are in the habit of not writing tests that violate
    Preconditions.

    The purpose of this function is to give you an easy way of making error messages
    without having to worry about introducing such bugs. Look at the function
    draw_two_lines for the proper way to use it.

    Parameter message: The error message to display
    Precondition: message is a string

    Parameter value: The value that caused the error
    Precondition: NONE (value can be anything)
    """
    return message+': '+repr(value)


def is_valid_angle(ang):
    """
    Returns: True if d is a number (integer or float); False otherwise.

    Parameter ang: The value to check
    Precondition: None (ang can be anything)
    """
    return (is_number(ang))


def is_valid_k(k):
    """
    Returns: True if k is an integer greater or equal to 1; False otherwise.

    Parameter k: The value to check
    Precondition: None (k can be anything)
    """
    return (type(k)==int and k>=1)


def is_valid_n(n):
    """
    Returns: True if n is an integer greater than or equal to 3; False otherwise.

    Parameter k: The value to check
    Precondition: None (n can be anything)
    """
    return (type(n)==int and n>=3)


def is_valid_number_of_lines(n):
    """
    Returns: True if n is an integer greater than or equal to 2; False otherwise.

    Parameter n: The value to check
    Precondition: None (n can be anything)
    """
    return (type(n)==int and n>=2)


def is_valid_snowflake_length(s):
    """
    Returns: True if s is an integer greater than 0; False otherwise.

    Parameter s: The value to check
    Precondition: None (s can be anything)
    """
    return (is_number(s) and s>0)


def is_valid_x(x):
    """
    Returns: True if x is a float; False otherwise.

    Parameter s: The value to check
    Precondition: None (x can be anything)
    """
    return (type(x)==float)


def is_valid_y(y):
    """
    Returns: True if y is a float; False otherwise.

    Parameter y: The value to check
    Precondition: None (y can be anything)
    """
    return (type(y)==float)


def is_valid_height(h):
    """
    Returns: True if h is a number greater than or equal to 0; False otherwise.

    Parameter h: The value to check
    Precondition: None (h can be anything)
    """
    return (is_number(h) and h>=0)


#################### DEMO: Two lines ####################

def draw_two_lines(w, sp):
    """
    Draws two lines on to window w.

    In the middle of the window w, his function draws a green line 100 pixels to the east,
    and then a blue line 200 pixels to the north.  It uses a new turtle that moves at
    speed sp, 0 <= sp <= 10, with 1 being slowest and 10 fastest (and 0 being "instant").

    REMEMBER: You need to flush the turtle if the speed is 0.

    Parameter w: The window to draw upon.
    Precondition: w is a cornell Window object.

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_window(w), report_error('w is not a valid window', w)
    assert is_valid_speed(sp), report_error('sp is not a valid speed', sp)

    # Clear the window first!
    w.clear()

    # Create a turtle and draw
    t = Turtle(w)
    t.speed = sp
    t.color = 'green'
    t.forward(100)  # draw a line 100 pixels in the current direction
    t.left(90)     # add 90 degrees to the angle
    t.color = 'blue'
    t.forward(200)

    # This is necessary if speed is 0!
    t.flush()


#################### TASK 1: Triangle ####################

def draw_triangle(t, s, c):
    """
    Draws an equilateral triangle of side s and color c at current position.

    The direction of the triangle depends on the current facing of the turtle.
    If the turtle is facing west, the triangle points up and the turtle starts
    and ends at the east end of the base line. If the turtle facing east, the
    triangle points down and the turtle starts and ends at the west side of the
    base line.

    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    position (x and y, within round-off errors), heading, color, and drawmode.
    If you changed any of these in the function, you must change them back.

    REMEMBER: You need to flush the turtle if the speed is 0.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter s: The length of each triangle side
    Precondition: s is a valid side length (number >= 0)

    Parameter c: The triangle color
    Precondition: c is a valid turtle color (see the helper function above)
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(s), report_error('Invalid side length', s)
    assert is_valid_color(c), report_error('Invalid color', c)

    # Hint: each angle in an equilateral triangle is 60 degrees.
    # Note: In this function, DO NOT save the turtle position and heading
    # in the beginning and then restore them at the end. The turtle moves
    # should be such that the turtle ends up where it started and facing
    # in the same direction, automatically.

    # Also, 3 lines have to be drawn. Does this suggest a for loop that
    # processes the range 0..2?
    original_color = t.color
    t.color= c
    for x in range(3):
         t.forward(s)
         t.right(120)
    t.color=original_color
    t.flush()

#################### TASK 2: Hexagon ####################

def draw_hex(t, s):
    """
    Draws six triangles using the color 'orange' to make a hexagon.

    The triangles are equilateral triangles, using draw_triangle as a helper.
    The drawing starts at the turtle's current position and heading. The
    middle of the hexagon is the turtle's starting position.

    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    position (x and y, within round-off errors), heading, color, and drawmode.
    If you changed any of these in the function, you must change them back.

    REMEMBER: You need to flush the turtle if the speed is 0.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter s: The length of each triangle side
    Precondition: s is a valid side length (number >= 0)
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(s), report_error('Invalid side length', s)

    # Note: Do not save any of the turtle's properties and then restore them
    # at the end. Just use 6 calls on procedures drawTriangle and t.left. Test
    # the procedure to make sure that t's final location and heading are the
    # same as t's initial location and heading (except for roundoff error).

    # The procedure is supposed to draw 6 triangles. Does that suggest a loop
    # that processes the integers in 0..5?
    for x in range(6):
        draw_triangle(t,s,'orange')
        t.left(60)

    t.flush()
#################### Task 3A: Spirals ####################


def draw_spiral(w, side, ang, n, sp):
    """
    Draws a spiral using draw_spiral_helper(t, side, ang, n, sp)

    This function clears the window and makes a new turtle t.  This turtle
    starts in the middle of the canvas facing west (NOT the default east).
    It then calls draw_spiral_helper(t, side, ang, n, sp). When it is done,
    the turtle is left hidden (visible is False).

    REMEMBER: You need to flush the turtle if the speed is 0.

    Parameter w: The window to draw upon.
    Precondition: w is a Window object.

    Parameter side: The length of each spiral side
    Precondition: side is a valid side length (number >= 0)

    Parameter ang: The angle of each corner of the spiral
    Precondition: ang is a number

    Parameter n: The number of edges of the spiral
    Precondition: n is a valid number of iterations (int >= 1)

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_window(w), report_error('w is not a valid window', w)
    assert is_valid_length(side), report_error(
        'side is not a valid length', side)
    assert is_valid_iteration(n), report_error(
        'n is not a valid number of iterations', n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed', sp)
    assert is_valid_angle(ang),report_errot('ang is not a valid angle', ang)
    # HINT: w.clear() clears window.
    # HINT: set the turtle's visible attribute to False at the end.
    w.clear()
    t=Turtle(w)
    t.heading=180
    draw_spiral_helper(t, side, ang, n, sp)
    t.visible=False

    if sp==0:
        t.flush()


def draw_spiral_helper(t, side, ang, n, sp):
    """
    Draws a spiral of n lines at the current position and heading.

    The spiral begins at the current turtle position and heading, turning ang
    degrees to the left after each line.  Line 0 is side pixels long. Line 1
    is 2*side pixels long, and so on.  Hence each Line i is (i+1)*side pixels
    long. The lines alternate between green, blue, and red, in that order, with
    the first one green.

    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    color, speed, visible, and drawmode. However, the final position and
    heading may be different. If you changed any of these four in the function,
    you must change them back.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter side: The length of each spiral side
    Precondition: side is a valid side length (number >= 0)

    Parameter ang: The angle of each corner of the spiral
    Precondition: ang is a number

    Parameter n: The number of edges of the spiral
    Precondition: n is a valid number of iterations (int >= 1)

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error(
        'side is not a valid length', side)
    assert is_valid_iteration(n), report_error(
        'n is not a valid number of iterations', n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed', sp)
    assert is_valid_angle(ang), report_error('ang is not a valid angle', ang)

    # NOTE: Since n lines must be drawn, use a for loop on a range of integers.

    original_color=t.color
    original_speed=t.speed
    for x in range(n):
        if x%3==0:
            t.color='green'
        elif x%3==1:
            t.color='blue'
        elif x%3==2:
            t.color='red'
        t.forward((x+1)*(side))
        t.left(ang)
    t.color = original_color
    t.speed=original_speed

#################### TASK 3B: Polygons ####################

def multi_polygons(w, side, k, n, sp):
    """
    Draws polygons using multi_polygons_helper(t, side, k, n, sp)

    This function clears the window and makes a new turtle t. This turtle starts in the
    middle of the canvas facing north (NOT the default east). It then calls
    multi_polygons_helper(t, side, k, n, sp). When it is done, the turtle is left
    hidden (visible is False).

    REMEMBER: You need to flush the turtle if the speed is 0.

    Parameter w: The window to draw upon.
    Precondition: w is a Window object.

    Parameter side: The length of each polygon side
    Precondition: side is a valid side length (number >= 0)

    Parameter k: The number of polygons to draw
    Precondition: k is an int >= 1

    Parameter n: The number of sides of each polygon
    Precondition: n is an int >= 3

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_window(w), report_error('w is not a valid window', w)
    assert is_valid_length(side), report_error(
        'side is not a valid length', side)
    assert is_valid_speed(sp), report_error('sp is not a valid speed', sp)
    assert is_valid_k(k), report_error('k is not a valid number of polygons', k)
    assert is_valid_n(n), report_error('n is not a valid number of sides', n)

    # HINT: w.clear() clears the  window.
    # HINT: set the turtle's visible attribute to False at the end.
    w.clear()
    t=Turtle(w)
    t.heading=90
    multi_polygons_helper(t, side, k, n, sp)
    t.visible=False

    if sp == 0:
        t.flush()


def multi_polygons_helper(t, side, k, n, sp):
    """
    Draws k n-sided polygons of side length s.

    The polygons are drawn by turtle t, starting at the current position. The turtles
    alternate colors between blue and red. Each polygon is drawn starting at the same
    place (within roundoff errors), but t turns left 360.0/k degrees after each polygon.

    At the end, ALL ATTRIBUTES of the turtle are the same as they were in the beginning
    (within roundoff errors).  If you change any attributes of the turtle. then you must
    restore them.  Look at the helper draw_polygon for more information.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter side: The length of each polygon side
    Precondition: side is a valid side length (number >= 0)

    Parameter k: The number of polygons to draw
    Precondition: k is an int >= 1

    Parameter n: The number of sides of each polygon
    Precondition: n is an int >= 3

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error(
        'side is not a valid length', side)
    assert is_valid_speed(sp), report_error('sp is not a valid speed', sp)
    assert is_valid_k(k), report_error('k is not a valid number of polygons', k)
    assert is_valid_n(n), report_error('n is not a valid number of sides', n)

    # HINT:  make sure that upon termination, t's color and speed are restored
    # HINT: since k polygons should be drawn, use a for-loop on a range.
    original_color=t.color
    original_heading=t.heading
    original_speed=t.speed
    for x in range(k):
        if x%2==0:
            t.color='blue'
        elif x%2==1:
            t.color='red'
        draw_polygon(t, side, n, sp)
        t.left(360.0/k)
    t.color=original_color
    t.heading=original_heading
    original_speed=t.speed


# DO NOT MODIFY
def draw_polygon(t, side, n, sp):
    """
    Draws an n-sided polygon using of side length side.

    The polygon is drawn with turtle t using speed sp.

    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED: position
    (x and y, within round-off errors), heading, color, speed, visible, and drawmode.
    There is no need to restore these.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter side: The length of each polygon side
    Precondition: side is a valid side length (number >= 0)

    Parameter n: The number of sides of each polygon
    Precondition: n is an int >= 3

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error(
        'side is not a valid length', side)
    assert (type(n) == int and n >= 3), report_error(
        'n is an invalid # of poly sides', n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed', sp)

    # Remember old speed
    oldspeed = t.speed
    t.speed = sp
    ang = 360.0/n  # exterior angle between adjacent sides

    # t is in position and facing the direction to draw the next line.
    for _ in range(n):
        t.forward(side)
        t.left(ang)

    # Restore the speed
    t.speed = oldspeed


#################### TASK 3C: Radiating lines ####################

def radiate(w, side, n, sp):
    """
    Draws n straight radiating lines using radiate_helper(t, side, n, sp)

    This function clears the window and makes a new turtle t.  This turtle starts in
    the middle of the canvas facing west (NOT the default east). It then calls
    radiate_helper(t, side, n, sp). When it is done, the turtle is left hidden
    (visible is False).

    REMEMBER: You need to flush the turtle if the speed is 0.

    Parameter w: The window to draw upon.
    Precondition: w is a Window object.

    Parameter side: The length of each radial line
    Precondition: side is a valid side length (number >= 0)

    Parameter n: The number of lines to draw
    Precondition: n is an int >= 2

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_window(w), report_error('w is not a valid window', w)
    assert is_valid_length(side), report_error(
        'side is not a valid length', side)
    assert is_valid_speed(sp), report_error('sp is not a valid speed', sp)
    assert is_valid_number_of_lines(n), report_error(
        'n is not a valid number of lines', n)
    # HINT: w.clear() clears the window.
    # HINT: set the turtle's visible attribute to False at the end.
    w.clear()
    t=Turtle(w)
    t.heading=180
    radiate_helper(t, side, n, sp)
    t.visible=False

    if sp ==0:
        t.flush()


def radiate_helper(t, side, n, sp):
    """
    Draws n straight radiating lines of length s at equal angles.

    This lines are drawn using turtle t with the turtle moving at speed sp.
    A line drawn at angle ang, 0 <= ang < 360 has HSV color (ang % 360.0, 1, 1).

    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED: color, speed,
    visible, and drawmode. However, the final position and heading may be different. If
    you changed any of these four in the function, you must change them back.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter side: The length of each radial line
    Precondition: side is a valid side length (number >= 0)

    Parameter n: The number of lines to draw
    Precondition: n is an int >= 2

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error(
        'side is not a valid length', side)
    assert is_valid_speed(sp), report_error('sp is not a valid speed', sp)
    assert is_valid_number_of_lines(n), report_error(
        'n is not a valid number of lines', n)

    # Notes:
    # 1. Drawing n lines should be done with a loop that processes
    #    a certain range of integers.
    # 2. You should keep the heading of the turtle in the range
    #    0 <= heading < 360.
    # 3. (t.heading % 360.0, 1, 1) is an HSV representation of the color
    #    determined by turtle t's heading.
    # 4. You can use an HSV object for the turtle's color attribute,
    #    even though all the examples use strings with color names
    original_color = t.color
    original_speed = t.speed
    for x in range(n):
        t.speed = sp
        t.color = introcs.HSV(t.heading%360.0,1.0,1.0)
        t.forward(side)
        t.backward(side)
        t.right(360.0/n)
    t.color = original_color
    t.speed= original_speed


#################### TASK 4.1: Grisly Snowflake ####################


def grisly(w, d, s, sp):
    """
    Draws a grisly snowflake with the given side length and depth d.

    This function clears the window and makes a new Pen (not Turtle).
    It calls the helper function grisly_helper to draw a grisly snowflake of
    depth d, side length s, and centered at (x = 0, y = 0), using the function
    call grisly_helper(p, x, y, d, s).

    The pen should be hidden while drawing and should be left hidden at the end.
    The pen fill and edge color is "gray".

    REMEMBER: You need to flush if the speed is 0.

    Parameter w: The window to draw upon.
    Precondition: w is a Window object.

    Parameter d: the depth of the grisly snowflake.
    Precondition: d is an int >= 0

    Parameter s: the side length of the overall final snowflake.
    Precondition: s is a valid side length > 0

    Parameter sp: The pen speed.
    Precondition: sp is an int between 0 and 10.
    """
    # Are the precondition assertions complete and correct?
    assert is_window(w), report_error('w is not a valid window', w)
    assert is_valid_depth(d), report_error('d is not a valid depth', d)
    assert is_valid_snowflake_length(s), report_error(
    's is not a valid side length',s)
    assert is_valid_speed (sp), report_error('sp is not a valid speed', sp)


    w.clear()
    p=Pen(w)
    p.visible=False
    p.fillcolor='gray'
    p.edgecolor='gray'
    grisly_helper(p,0.0,0.0,d,s)
    if sp==0:
        p.flush()


def grisly_helper(p, x, y, d, s):
    """
    This function draws a grisly snowflake of depth d with side length s
    at center (x, y).

    If any of the pen attributes are altered during drawing, they must be
    restored to their initial values at the of drawing.

    Parameter p: the Pen object to draw with.
    Precondition: p is a Pen with solid attribute False.

    Parameters x and y: The coordinates of the center of snowflake.
    Precondition: x and y are floats

    Parameter d: The depth.
    Precondition: d is an int >= 0.

    Parameter s: the side length
    Precondition: s is a number > 0.
    """
    # Are the precondition assertions complete and correct?
    assert is_valid_penmode(p), report_error('p is not a valid penmode', p)
    assert is_valid_x(x), report_error('x is not a valid coordinates', x)
    assert is_valid_y(y), report_error('y is not a valid coordinate',y)
    assert is_valid_depth(d), report_error ('d is not a valid depth', d)
    assert is_valid_snowflake_length(s), report_error(
    's is not a valid side length', s)
    original_px=p.x
    original_py=p.y
    if d==0:
        fill_hex(p, s, x, y)
    else:
        grisly_helper(p, x, y, d-1, s/3.0)
        grisly_helper(p, x-2.0*s/3.0, y, d-1, s/3.0)
        grisly_helper(p, x-s/3.0, s/math.sqrt(3)+y, d-1, s/3.0)
        grisly_helper(p, x+s/3.0, s/math.sqrt(3)+y, d-1, s/3.0)
        grisly_helper(p, x+2.0*s/3.0, y, d-1, s/3.0)
        grisly_helper(p, x+s/3.0, y-(s/math.sqrt(3)), d-1, s/3.0)
        grisly_helper(p, x-s/3.0, y-(s/math.sqrt(3)), d-1, s/3.0)
    p.move(p.x,p.y)


# Useful helper function
def fill_hex(p, s, x, y):
    """
    Fill a hexagon of side length s with center at (x, y) using pen p.

    Precondition: p is a Pen with solid attribute False. s > 0 .
    x and y are numbers (ints or floats).
    """
    # assertion preconditions omitted (you do not need to add these)

    p.move(x + s, y)
    dx = s*math.cos(math.pi/3.0)
    dy = s*math.sin(math.pi/3.0)
    p.solid = True
    p.drawLine(-dx, dy)
    p.drawLine(-s, 0)
    p.drawLine(-dx, -dy)
    p.drawLine(dx, -dy)
    p.drawLine(s, 0)
    p.drawLine(dx, dy)
    p.solid = False

#################### TASK 4.2: 3-Branch Tree ####################


def threeBranchTree(w, height, d, sp):
    """
    Draws a three branch tree with the given height and depth.

    This function clears the window and makes a new turtle t.  This turtle starts
    at the bottom of the three branch tree centered at (0,0) with the given height,
    facing upwards. It draws by calling the function threeBranchHelper(t, d, hght).

    The turtle should be visible while drawing, but hidden at the end. The turtle color
    is 'blue'.

    REMEMBER: You need to flush the turtle if the speed is 0.

    Parameter w: The window to draw upon.
    Precondition: w is a Window object.

    Parameter height: The height of the overall three branch tree.
    Precondition: height is a valid side length (number >= 0)

    Parameter d: The recursive depth of the tree.
    Precondition: n is a valid depth (int >= 0)

    Parameter sp: The drawing speed for the turtle.
    Precondition: sp is a valid turtle/pen speed.
    """
    # Add the necessary assertion statements here
    assert is_window(w), report_error("w is not a valid window", w)
    assert is_valid_height(height), report_error(
    'h is not a valid height', height)
    assert is_valid_depth(d), report_error("d is a valid depth", d)
    assert is_valid_speed(sp), report_error("sp is not a valid speed", sp)

    w.clear()
    t=Turtle(w)
    t.speed=sp
    t.heading=90
    t.move(0.0,-height/2.0)
    t.visible=True
    t.color="blue"
    threeBranchHelper(t, d, height)
    t.visible=False

    if sp==0:
        t.flush()


def threeBranchHelper(t, d, hght):
    """
    Draws a three branch tree of height hght and depth d at the current
    position and angle.

    The tree is draw with the current turtle color. You should make no assumptions of
    the current angle of the turtle (e.g. use left and right to turn; do not set the
    heading).

    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    position (within round-off errors), heading, color, speed, visible, and drawmode.
    If you changed any of these four in the function, you must change them back.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter d: The recursive depth of the edge
    Precondition: d is a valid depth (int >= 0)

    Parameter hght: The side length/height of the tree.
    Precondition: hght is a valid height (number >= 0)
    """
    # Don't forget to add assertions.
    assert is_valid_turtlemode(t), report_error("t is not a valid turtlemode",t)
    assert is_valid_depth(d), report_error("d is not a valid depth", d)
    assert is_valid_height(hght), report_error(
    "hght is not a valid height", hght)

    original_tx=t.x
    original_ty=t.y

    if d==0:
        t.forward(hght)
        t.backward(hght)
    else:
        t.forward(hght/2.0)
        t.left(90)
        threeBranchHelper(t,d-1,hght/2.0)
        t.right(90)
        threeBranchHelper(t,d-1,hght/2.0)
        t.right(90)
        threeBranchHelper(t,d-1,hght/2.0)
        t.left(90)
        t.backward(hght/2.0)

    t.move(original_tx, original_ty)

#################### TASK 4.3: 3-Branch Tree ####################


def binarytree(w, height, d, sp):
    """
    Draws a binary tree with the given height and depth d.

    This function clears the window and makes a new turtle t. This turtle starts
    at the bottom of the binary tree centered at (0,0) with the given height,
    facing upwards. It draws by calling binarytree_helper(t, side, d).

    In this context, we take "centered" to mean the position at which the two
    trees connect with the trunk.

    The turtle should be visible while drawing, but hidden at the end. The turtle
    color is 'green'.

    REMEMBER: You need to flush the turtle if the speed is 0.

    Parameter w: The window to draw upon.
    Precondition: w is a Window object.

    Parameter height: The height of the binary tree.
    Precondition: height is a valid side length (number >= 0)

    Parameter d: The recursive depth of the tree.
    Precondition: n is a valid depth (int >= 0)

    Parameter sp: The drawing speed.
    Precondition: sp is a valid turtle/pen speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_window(w), report_error('w is not a valid window', w)
    assert is_valid_height(height), report_error(
    'height is not a valid height', height)
    assert is_valid_depth(d), report_error('depth is not a valid depth', d)
    assert is_valid_speed(sp), report_error('sp is not a valid speed', sp)

    w.clear()
    t=Turtle(w)
    t.visible=True
    t.color='green'
    t.speed=sp
    t.heading=90
    t.move(0.0,-2.0*height/5.0)
    binarytree_helper(t,height, d)
    t.visible=False
    if sp==0:
        t.flush()


def binarytree_helper(t, side, d):
    """
    Draws a binary tree of side length side and depth d at the current position
    and angle.

    The tree is draw with the current turtle color. You should make no assumptions
    of the current angle of the turtle (e.g. use left and right to turn; do not
    set the heading).

    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    position (within round-off errors), heading, color, speed, visible, and drawmode.
    If you changed any of these four in the function, you must change them back.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter side: The height/side length of the tree
    Precondition: side is a valid side length (number >= 0)

    Parameter d: The recursive depth of the edge
    Precondition: d is a valid depth (int >= 0)
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error(
    'Invalid side length of tree', side)
    assert is_valid_depth(d), report_error('Invalid depth', depth)

    original_tx=t.x
    original_ty=t.y
    if d==0:
        t.forward(side)
        t.backward(side)

    else:
        t.forward(2*side/5)
        t.left(30)
        binarytree_helper(t,2.0*side/3.0, d-1)
        t.right(110)
        binarytree_helper(t,2.0*side/3.0, d-1)
        t.left(80)
        t.backward(2.0*side/5.0)

    t.move(original_tx, original_ty)


################ Test Functions #################

def prompt(func):
    """
    Returns: The answer to a yes or no question.

    If the answer is invalid, it is treated as no.

    Parameter func: The function to ask about
    Precondition: func is string
    """
    ans = input('Call '+func+'? [y/n]: ')
    return ans.strip().lower() == 'y'


def depth(func):
    """
    Returns: The answer to a (recursion) depth question.

    If the anser is invalid, it is treated as -1.

    Parameter func: The function to ask about
    Precondition: func is string
    """
    ans = input('Function '+func+' depth? [-1 to skip]: ')
    try:
        return int(ans.strip())
    except:
        return -1


def main():
    """
    Runs each of the functions, allowing user to skip functions.
    """
    w = Window()

    # Change me to get different speeds
    speed = 0

    if prompt('draw_two_lines'):
        draw_two_lines(w, speed)

    if prompt('draw_triangle'):
        w.clear()
        turt = Turtle(w)
        turt.speed = speed
        draw_triangle(turt, 100, 'orange')

    if prompt('draw_hex'):
        w.clear()
        turt = Turtle(w)
        turt.speed = speed
        draw_hex(turt, 50)

    if prompt('draw_spiral'):
        draw_spiral(w, 1, 24, 64, speed)

    if prompt('multi_polygons'):
        multi_polygons(w, 100, 5, 6, speed)

    if prompt('radiate'):
        radiate(w, 150, 45, speed)

    d = depth('threebranch')
    if d >= 0:
        threeBranchTree(w, 300, d, speed)

    d = depth('binarytree')
    if d >= 0:
        binarytree(w, 300, d, speed)

    d = depth('grisly')
    if d >= 0:
        grisly(w, d, 200, speed)

    # Pause for the final image
    input('Press <return>')


# Application code
if __name__ == '__main__':
    main()
