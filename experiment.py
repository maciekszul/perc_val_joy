from psychopy import core
from psychopy import visual
from psychopy import monitors
from psychopy import gui
from psychopy import event
from psychopy import clock
from psychopy.hardware import joystick
import psychopy.tools.coordinatetools as ct
import os.path as op
import numpy as np
import pandas as pd
import misc


# display settings

background_color = "#939393"
exp_gray = "#848484"

alt_size = 2
img_size = 3
alt_loc = [6, 6]
start_loc = [0, -6]

left_loc = [-alt_loc[0], alt_loc[1]]
right_loc = [alt_loc[0], alt_loc[1]]

scale_range = [210, 330]
scale_radius = 7

# monitor settings
x230 = (28, 56, (1366, 768))
lab = (53, 65, (1920, 1080))

width, dist, res = x230

mon = monitors.Monitor("default")
mon.setWidth(width)
mon.setDistance(dist)
mon.setSizePix(res)

win = visual.Window(
    size=res,
    color=background_color,
    fullscr=True,
    allowGUI=False,
    winType="pyglet",
    units="deg",
    monitor=mon
)


# hardware settings

joyN = joystick.getNumJoysticks()
joy = joystick.Joystick(0)

# cue

sz = 0.15
th = sz/7.

circle = visual.Circle(
    win,
    radius=sz,
    edges=40,
    units='deg',
    fillColor='white',
    lineColor='white'
)

line1 = visual.ShapeStim(
    win,
    vertices=[[sz, 0 + th],
              [-sz*2, 0 + th],
              [-sz*2, 0 - th],
              [sz*2, 0 - th]],
    units='deg',
    fillColor=background_color,
    lineColor=background_color
)


line2 = visual.ShapeStim(
    win,
    vertices=[[0 - th, sz*2],
             [0 + th, sz*2],
             [0 + th, -sz*2],
             [0 - th, -sz*2]],
    units='deg',
    fillColor=background_color,
    lineColor=background_color)

circle1 = visual.Circle(
    win,
    radius=th,
    edges=40,
    units='deg',
    fillColor='white',
    lineColor='white'
)


def draw_cue():
    circle.draw()
    line1.draw()
    line2.draw()
    circle1.draw()


# stimuli

left_img = visual.ImageStim(
    win,
    image=None,
    pos=left_loc,
    size=[img_size, img_size] 
)

left_square = visual.Rect(
    win,
    width=alt_size,
    height=alt_size,
    color="blue",
    pos=left_loc,
    lineWidth=3,
    opacity=0.5
)

l_sq_loc = misc.localise_polygon(
    left_loc,
    left_square.vertices
)

right_img = visual.ImageStim(
    win,
    image=None,
    pos=right_loc,
    size=[img_size, img_size] 
)

right_square = visual.Rect(
    win,
    width=alt_size,
    height=alt_size,
    color="red",
    pos=right_loc,
    lineWidth=5,
    opacity=0.5
)

r_sq_loc = misc.localise_polygon(
    right_loc,
    right_square.vertices
)

start_zone = visual.Circle(
    win,
    radius=1,
    edges=40,
    units='deg',
    fillColor=None,
    lineColor='white',
    pos=start_loc
)

sz_loc = misc.localise_polygon(
    start_loc,
    start_zone.vertices
)

cursor = visual.Circle(
    win,
    radius=0.1,
    edges=40,
    units='deg',
    fillColor='white',
    lineColor='white'
)


# scale
scale_circle = visual.Circle(
    win,
    radius=scale_radius,
    edges=360,
    units='deg'
)

scale_vert = np.array(scale_circle.vertices)
scale_r = scale_vert[scale_range[0]:scale_range[1]+1]
scale = visual.ShapeStim(
    win,
    vertices=scale_r,
    lineColor="white",
    lineWidth=5,
    closeShape=False,
    ori=90
)

scale_cursor = visual.Circle(
    win,
    radius=0.1,
    edges=40,
    units='deg',
    fillColor='green',
    lineColor='green',
    opacity=0
)

# text

text_stim = visual.TextStim(
    win,
    text="xxx",
    height=0.5,
    color="black",
    pos=(-14, 7),
    alignHoriz="left"
)

blank = visual.TextStim(
    win,
    text="blank",
    height=0.5,
    color="black",
    pos=(0, 0),
    alignHoriz="left",
    opacity=1
)

joy_command = visual.TextStim(
    win,
    text="center the joystick",
    height=0.5,
    color="black",
    pos=(0,0),
    alignHoriz="center",
    opacity=1
)

for i in range(3):
    left_img.setImage("img/hotdog.jpg")
    right_img.setImage("img/money.jpg")
    event.clearEvents()

    while True:
        x, y = joy.getX(), -joy.getY()
        pos_x, pos_y = [x*14 + start_loc[0], y*14 + start_loc[1]]
        if not misc.point_in_poly(pos_x, pos_y, sz_loc):
            joy_command.draw()
            win.flip()
        else:
            break

    blank.draw()
    win.flip()
    core.wait(1)

    while True:
        x, y = joy.getX(), -joy.getY()
        pos_x, pos_y = [x*14 + start_loc[0], y*14 + start_loc[1]]
        
        cursor.pos = [pos_x, pos_y]
        text_stim.text = "X:{0}\nY: {1}\nPosX: {2}\nPosY: {3}".format(x,y, pos_x, pos_y)
        
        left_img.draw()
        right_img.draw()
        text_stim.draw()
        draw_cue()
        left_square.draw()
        right_square.draw()
        start_zone.draw()
        cursor.draw()
        
        if misc.point_in_poly(pos_x, pos_y, l_sq_loc) :
            left_square.lineColor = "black"
            win.flip()
            break
        else:
            left_square.lineColor = "blue"

        if misc.point_in_poly(pos_x, pos_y, r_sq_loc):
            right_square.lineColor = "black"
            win.flip()
            break
        else:
            right_square.lineColor = "red"

        win.flip()

    blank.draw()
    win.flip()
    core.wait(2)

    # scale

    while True:
        x, y = joy.getX(), -joy.getY()
        pos_x, pos_y = [x*14 + start_loc[0], y*14 + start_loc[1]]
        if not misc.point_in_poly(pos_x, pos_y, sz_loc):
            joy_command.draw()
            win.flip()
        else:
            break

    blank.draw()
    win.flip()
    core.wait(1)

    while True:
        x, y = joy.getX(), -joy.getY()
        angle, radius = ct.cart2pol(x, y, units="rad")
        scale_cursor.pos = ct.pol2cart(angle, scale_radius, units="rad")
        angle = np.abs(angle + np.pi)
        if (radius > 0.7) & (angle > np.deg2rad(scale_range[0])) & (angle < np.deg2rad(scale_range[1])):
            scale_cursor.opacity = 1
            if radius > 0.85:
                break
        else:
            scale_cursor.opacity = 0
        text_stim.text = "X:{0}\nY: {1}\nANG: {2}\nRAD: {3}".format(x,y, angle, radius)
        text_stim.draw()
        scale.draw()
        scale_cursor.draw()
        win.flip()

        if event.getKeys(keyList=['q'], timeStamped=False):
            win.close()
            core.quit()


win.close()
core.quit()