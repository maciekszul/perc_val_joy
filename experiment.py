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


# session info

subj_ID = str(1).zfill(4)
subj_file = "CB2_40_pairs.csv"
exp_cond = pd.read_csv(subj_file)
exp_cond = exp_cond.to_dict("list")
trial_am = len(exp_cond["Item1"])

timestamp = core.getAbsTime()

misc.mk_dir("data")
path_data = "data/{}".format(subj_ID)
misc.mk_dir(path_data)

# display settings

background_color = "#939393"
exp_gray = "#848484"

size_image = "img/size2.png"
pref_image = "img/heart.png"
cond_size = 2
cond_loc = [0, 0]

alt_size = 2
img_size = 6
alt_loc = [9.5, 3]
resp_size = img_size + 0.5
start_loc = [0, -6]


left_loc = [-alt_loc[0], alt_loc[1]]
right_loc = [alt_loc[0], alt_loc[1]]

scale_range = [180, 360]
scale_radius = 5

tick_size = 1

fix_time = 1
mid_time = 2
pre_scale_time = 1
iti_time = 2


# monitor settings
x230 = (28, 45, (1366, 768))
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

framerate = win.getActualFrameRate(
    nIdentical=10,
    nMaxFrames=120,
    nWarmUpFrames=10,
    threshold=1
)

framerate_r = np.round(framerate)

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
    vertices=[[sz*1.1, 0 + th],
              [-sz*1.1, 0 + th],
              [-sz*1.1, 0 - th],
              [sz*1.1, 0 - th]],
    units='deg',
    fillColor=background_color,
    lineColor=background_color
)

line2 = visual.ShapeStim(
    win,
    vertices=[[0 - th, sz*1.1],
             [0 + th, sz*1.1],
             [0 + th, -sz*1.1],
             [0 - th, -sz*1.1]],
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

cond_img = visual.ImageStim(
    win,
    image=None,
    size=[cond_size, cond_size],
    pos=cond_loc
)

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
    pos=left_loc,
    lineWidth=3,
    fillColor=None,
    lineColor="blue",
    opacity=1
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
    pos=right_loc,
    lineWidth=3,
    fillColor=None,
    lineColor="red",
    opacity=1
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

resp_ind = visual.Rect(
    win,
    width=resp_size,
    height=resp_size,
    pos=left_loc,
    lineWidth=3,
    fillColor="green",
    lineColor="green",
    opacity=1
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
    ori=90,
    pos=start_loc
)

scale_cursor = visual.Circle(
    win,
    radius=0.5,
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

# data logging settings
columns = [
    "ID",
    "age",
    "gender",
    "trial"
]

data_dict = {i: [] for i in columns}

instructions = [
    "Instruction 1",
    "Instruction 2",
    "Instruction 3",
    "Instruction 4",
    "Instruction 5",
    "Instruction 6"
]

for text in instructions:
    text_stim.text = text
    text_stim.draw()
    win.flip()
    event.waitKeys(
        maxWait=360, 
        keyList=["space"], 
        modifiers=False, 
        timeStamped=False
    )

blank.draw()
win.flip()
core.wait(1)

# experiment clock
exp_clock = clock.MonotonicClock()

exp_start = exp_clock.getTime() ###

# for i in range(trial_am):
for i in range(9,12):
    left_img.setImage("img/{}".format(exp_cond["Item1"][i]))
    right_img.setImage("img/{}".format(exp_cond["Item2"][i]))

    if exp_cond["ratType"][i] == "rate_p":
        cond_img.setImage(size_image)
        
    elif exp_cond["ratType"][i] == "rate_v":
        cond_img.setImage(pref_image)


    event.clearEvents()

    x_dec = []
    y_dec = []
    t_dec = []

    x_scale = []
    y_scale = []
    t_scale = []

    wait_for_joy_1 = exp_clock.getTime() ###

    while True:
        x, y = joy.getX(), -joy.getY()
        pos_x, pos_y = [x*14 + start_loc[0], y*14 + start_loc[1]]
        if not misc.point_in_poly(pos_x, pos_y, sz_loc):
            joy_command.draw()
            win.flip()
        else:
            break

    
    fix_start = exp_clock.getTime() ###
    fix = core.StaticPeriod(screenHz=framerate_r)
    draw_cue()
    win.flip()
    fix.start(fix_time)
    # operations during fix
    fix.complete()
    
    stim_onset = exp_clock.getTime() ###

    while True:
        x, y = joy.getX(), -joy.getY()
        pos_x, pos_y = [x*14 + start_loc[0], y*14 + start_loc[1]]
        
        x_dec.append(x)
        y_dec.append(y)
        t_dec.append(exp_clock.getTime())

        cursor.pos = [pos_x, pos_y]
        text_stim.text = "X:{0}\nY: {1}\nPosX: {2}\nPosY: {3}".format(x,y, pos_x, pos_y)

        cond_img.draw()
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
            resp_ind.pos = left_loc
            resp_ind.opacity = 1
            resp_ind.draw()
            left_img.draw()
            right_img.draw()
            text_stim.draw()
            win.flip()
            core.wait(1)
            break
        else:
            left_square.lineColor = "blue"
            resp_ind.opacity = 0

        if misc.point_in_poly(pos_x, pos_y, r_sq_loc):
            right_square.lineColor = "black"
            resp_ind.pos = right_loc
            resp_ind.opacity = 1
            resp_ind.draw()
            left_img.draw()
            right_img.draw()
            text_stim.draw()
            win.flip()
            core.wait(1)
            break
        else:
            right_square.lineColor = "red"
            resp_ind.opacity = 0

        win.flip()

        if event.getKeys(keyList=['q'], timeStamped=False):
            win.close()
            core.quit()

    trial_end = exp_clock.getTime() ###

    mid = core.StaticPeriod(screenHz=framerate_r)
    blank.draw()
    win.flip()
    mid.start(mid_time)

    joystick_output = np.vstack([np.array(x_dec), np.array(y_dec), np.array(t_dec)])
    joy_path = op.join(path_data, "trial_{0}_{1}_{2}".format(subj_ID, str(i).zfill(4), timestamp))
    np.save(joy_path, joystick_output)

    del x_dec
    del y_dec
    del t_dec
    del joystick_output
    
    mid.complete()


    # scale

    wait_for_joy_2 = exp_clock.getTime() ###
    while True:
        x, y = joy.getX(), -joy.getY()
        pos_x, pos_y = [x*14 + start_loc[0], y*14 + start_loc[1]]
        if not misc.point_in_poly(pos_x, pos_y, sz_loc):
            joy_command.draw()
            win.flip()
        else:
            break

    pre_scale_onset = exp_clock.getTime() ###
    pre_scale = core.StaticPeriod(screenHz=framerate_r)
    blank.draw()
    win.flip()
    pre_scale.start(pre_scale_time)
    # operations during fix
    pre_scale.complete()

    scale_onset = exp_clock.getTime() ###

    while True:
        x, y = joy.getX(), -joy.getY()

        x_scale.append(x)
        y_scale.append(y)
        t_scale.append(exp_clock.getTime())

        angle, radius = ct.cart2pol(x, y, units="rad")
        s_cur_pos_x, s_cur_pos_y = ct.pol2cart(angle, scale_radius, units="rad")
        scale_cursor.pos = (s_cur_pos_x + start_loc[0], s_cur_pos_y + start_loc[1])
        angle = np.abs(angle + np.pi)
        if (radius > 0.7) & (angle > np.deg2rad(scale_range[0])) & (angle < np.deg2rad(scale_range[1])):
            scale_cursor.opacity = 1
            if radius > 0.9:
                scale.draw()
                scale_cursor.draw()
                win.flip()
                core.wait(1)
                break
        else:
            scale_cursor.opacity = 0
        text_stim.text = "X:{0}\nY: {1}\nANG: {2}\nRAD: {3}".format(x,y, angle, radius)
        text_stim.draw()
        left_img.draw()
        right_img.draw()
        scale.draw()
        scale_cursor.draw()
        win.flip()

        if event.getKeys(keyList=['q'], timeStamped=False):
            win.close()
            core.quit()
    
    iti_onset = exp_clock.getTime() ###

    iti = core.StaticPeriod(screenHz=framerate_r)
    draw_cue()
    win.flip()
    iti.start(iti_time)
    # operations during iti

    joystick_output = np.vstack([np.array(x_scale), np.array(y_scale), np.array(t_scale)])
    joy_path = op.join(path_data, "scale_{0}_{1}_{2}".format(subj_ID, str(i).zfill(4), timestamp))
    np.save(joy_path, joystick_output)

    del x_scale
    del y_scale
    del t_scale
    del joystick_output

    print(iti.complete())


win.close()
core.quit()