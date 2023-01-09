from psychopy import gui, visual, core, data, event, logging
from psychopy.hardware import keyboard

# Setup the Window
win = visual.Window(
    size=(1024, 768), fullscr=True, screen=0, 
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='pix')

image = visual.ImageStim(
    win=win,
    name='image', 
    image=None, mask=None,
    ori=0.0, pos=(0, 100), size=(200),
    color=[1,1,1], colorSpace='rgb',
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

slider = visual.Slider(win=win, name='slider',
    size=(400, 40), pos=(0, -100), units=None,
    labels=[1,2,3,4,5,6,7,8], ticks=(1, 2, 3, 4, 5, 6, 7, 8), 
    granularity=1.0,
    style=('rating', 'whiteOnBlack'),
    color='black', font='HelveticaBold', labelHeight=20,
    flip=False, depth=-1, readOnly=False)
slider.markerPos = None
slider.marker.fillColor='Red'
slider.marker.lineColor='Red'
slider.marker.size=[30,30]

Text_notAttractive = visual.TextStim(win=win, name='notAttractive', ori=0, 
    color='black', font='HelveticaBold',pos=(-520,-100), height=26, wrapWidth=None,
    colorSpace='rgb', opacity=1, text='Not Attractive',languageStyle='LTR', depth=-4.0, 
    alignText='right')

Text_Attractive = visual.TextStim(win=win, name='Attractive', ori=0, 
    color='black', font='HelveticaBold',pos=(520, -100), height=26, wrapWidth=None,
    colorSpace='rgb', opacity=1,  text='Attractive',languageStyle='LTR', depth=-4.0, 
    alignText='left')

button = visual.ImageStim(
    win=win,
    name='OK_Choice', 
    image='./ratingRoutines/buttonOK.png', mask=None,
    ori=0, pos=(0, -200), size=(120,62), #120,62
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)

text_wait = visual.ImageStim(win=win, name='wait',
    image='./ratingRoutines/StartInterface.png', mask=None, pos = (0,100), size = (2680/2,271/2))

text_end = visual.TextStim(win=win, name='end',
    text='', font='Calibri', height=25, wrapWidth=1000,
    color='black', pos = (0,100))

text_rest = visual.TextStim(win=win, name='end',
    text='休息時間，按OK以繼續', font='Calibri',
    color='black', pos = (0,100))

text_instruction = visual.ImageStim(win=win, name='ins', 
    mask=None, pos = (0,100), size=(2725/2, 424/2))

cross = visual.ShapeStim(
    win=win, name='cross', vertices='cross',
    size=(45,45),#30,30
    ori=0.0, pos=(0, 0),
    lineWidth=1.0,  lineColor='black', fillColor='black',
    opacity=1, depth=0.0, interpolate=True)

leftImg = visual.ImageStim(
    win=win,
    name='leftImage', 
    image=None, mask=None,
    ori=0.0, pos=(-180, 100), size=(180),
    color=[1,1,1], colorSpace='rgb',
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

rightImg = visual.ImageStim(
    win=win,
    name='rightImage', 
    image=None, mask=None,
    ori=0.0, pos=(180, 100), size=(180),
    color=[1,1,1], colorSpace='rgb',
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

key_Choice = keyboard.Keyboard()

def StartInterface():
    text_wait.draw()
    button.draw()
    win.flip()
    gotValidClick = False
    prevButtonState = mouse.getPressed()
    keys = ['placeholder']
    while not gotValidClick:
        buttons = mouse.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                if button.contains(mouse):
                    gotValidClick = True
        theseKeys = defaultKeyboard.getKeys(keyList=['escape'], waitRelease=True)
        keys.extend(theseKeys)
        if  keys[-1] == 'escape':
            core.quit()
    win.flip()


def EndInterface(accuracy):
    text_end.text=f'實驗結束\n你在這800回合中的正確率是: {accuracy*100}%\n你的受試者費是 300 + 150x{accuracy}={300 + 150*accuracy}'
    text_end.draw()
    button.draw()
    win.flip()
    gotValidClick = False
    prevButtonState = mouse.getPressed()
    keys = ['placeholder']
    while not gotValidClick:
        buttons = mouse.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                if button.contains(mouse):
                    gotValidClick = True
        theseKeys = defaultKeyboard.getKeys(keyList=['escape'], waitRelease=True)
        keys.extend(theseKeys)
        if  keys[-1] == 'escape':
            core.quit()
    win.flip()

def restInterface():
    text_rest.draw()
    button.draw()
    win.flip()
    gotValidClick = False
    prevButtonState = mouse.getPressed()
    keys = ['placeholder']
    while not gotValidClick:
        buttons = mouse.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                if button.contains(mouse):
                    gotValidClick = True
        theseKeys = defaultKeyboard.getKeys(keyList=['escape'], waitRelease=True)
        keys.extend(theseKeys)
        if  keys[-1] == 'escape':
            core.quit()
    win.flip()

def InstructionInterface(instructionImg):
    text_instruction.image = instructionImg
    text_instruction.draw()
    button.draw()
    win.flip()
    gotValidClick = False
    prevButtonState = mouse.getPressed()
    keys = ['placeholder']
    while not gotValidClick:
        buttons = mouse.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                if button.contains(mouse):
                    gotValidClick = True
        theseKeys = defaultKeyboard.getKeys(keyList=['escape'], waitRelease=True)
        keys.extend(theseKeys)
        if  keys[-1] == 'escape':
            core.quit()
    win.flip()

def Interval(second):
    routineTimer.reset()
    cross.draw()
    win.flip()
    routineTimer.add(second)
    while routineTimer.getTime() > 0:
        pass
    win.flip()
    routineTimer.reset()

routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started

# Initialize components for Routine "trial"
trialClock = core.Clock()
button.buttonClock = core.Clock()
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()



