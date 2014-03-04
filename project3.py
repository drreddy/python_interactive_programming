"""
Code Submitted for Stopwatch The game

Submitted by:
Rajeev Reddy
website:http://drreddy.herokuapp.com
"""
import simplegui

# global variables for time, time update string, score, score update string
time = 0
time_string = '0:00.0'
score_string = 'Your Score: 0/0'
attempts = 0
score = 0

# helper function format that converts time to specific format
def format(t):
    global time_string
    minutes = t/600
    seconds_temp = t % 600
    seconds = seconds_temp/10
    milliseconds = seconds_temp%10
    if(seconds_temp < 100):
        time_string = str(minutes)+':'+str(0)+str(seconds)+'.'+str(milliseconds)  
    else:
        time_string = str(minutes)+':'+str(seconds)+'.'+str(milliseconds)  

# helper function to update score
def update_score():
    global score_string, score, attempts, already_stopped
    if(time%10 == 0):
        score = score + 1
        attempts = attempts + 1
        score_string = 'Your Score: '+str(score)+'/'+str(attempts)
    else:
        attempts = attempts + 1
        score_string = 'Your Score: '+str(score)+'/'+str(attempts)
    # boolean to tell the program if the stopwatch is already stooped or not
    already_stopped = True
        
# event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global already_stopped
    t.start()
    # boolean to check if the stopwatch is already stooped or not
    already_stopped = False
    
def stop():
    t.stop()
    if(already_stopped):
        pass
    else:
        update_score()
    
# resetting all the variables including the strings
def reset():
    global integer, time_string, score_string, score, attempts
    t.stop()
    integer = 0
    time_string = '0:00.0'
    score_string = 'Your Score: 0/0'
    score = 0
    attempts = 0
    
# event handler for timer with 0.1 sec interval
def tick():
    global time
    time = time + 1
    format(time)

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(time_string, (85, 110), 50, 'White', 'sans-serif')
    canvas.draw_text(score_string, (145, 30), 20, 'Green', 'sans-serif')
    
# frame
f = simplegui.create_frame('Stopwatch Game',300,200)

# event handlers for drawing, blank space, timer, buttons
f.set_draw_handler(draw_handler)
blank_space = f.add_label(' ')
start_button = f.add_button('Start', start, 200)
blank_space = f.add_label(' ')
stop_button = f.add_button('Stop', stop, 200)
blank_space = f.add_label(' ')
reset_button = f.add_button('Reset', reset, 200)
t = simplegui.create_timer(100,tick)

# start frame
f.start()

# timer is started in button event handlers

