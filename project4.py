"""
Implementation of classic arcade game Pong

Submitted by:
Rajeev Reddy
website:http://drreddy.herokuapp.com
"""

#left side player is player one

import simplegui
import random

# globals - pos and vel encode vertical info for paddle
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    # randomly deciding balls initial velocity based on direction
    if direction:
        ball_vel = [random.randrange(4, 9),-random.randrange(1, 5)]
    else:
        ball_vel = [-random.randrange(4, 9),-random.randrange(1, 5)]

# event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH,HEIGHT/2 - HALF_PAD_HEIGHT]
    paddle2_pos = [WIDTH-HALF_PAD_WIDTH,HEIGHT/2 - HALF_PAD_HEIGHT]
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    if random.randrange(1, 3) == 1:
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # bouncing and checking ball position
    if(ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    elif(ball_pos[1] >= (HEIGHT - BALL_RADIUS)):
        ball_vel[1] = -ball_vel[1]
    elif(ball_pos[0] <= (PAD_WIDTH + BALL_RADIUS)):
        #checking ball position wrt paddle edge
        if((ball_pos[1] < paddle1_pos[1] - BALL_RADIUS) or (ball_pos[1] > paddle1_pos[1]+PAD_HEIGHT + BALL_RADIUS)):
            spawn_ball(RIGHT)
            score2 += 1 
        else:
            ball_vel[0] = -(ball_vel[0]-0.3)
    elif(ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS)):
        #checking ball position wrt paddle edge
        if((ball_pos[1] < paddle2_pos[1] - BALL_RADIUS) or (ball_pos[1] > paddle2_pos[1]+PAD_HEIGHT + BALL_RADIUS)):
            spawn_ball(LEFT)
            score1 += 1
        else:
            ball_vel[0] = -(ball_vel[0]+0.3)
        
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    
    if(paddle1_pos[1] > HEIGHT - PAD_HEIGHT):
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT
    elif(paddle2_pos[1] > HEIGHT - PAD_HEIGHT):
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT
    elif(paddle1_pos[1] < 0):
        paddle1_pos[1] = 0
    elif(paddle2_pos[1] < 0):
        paddle2_pos[1] = 0
       
    # paddles
    c.draw_polygon([[paddle1_pos[0],paddle1_pos[1]], [paddle1_pos[0], paddle1_pos[1]+PAD_HEIGHT]], PAD_WIDTH, 'Gray', 'white')
    c.draw_polygon([[paddle2_pos[0],paddle2_pos[1]], [paddle2_pos[0], paddle2_pos[1]+PAD_HEIGHT]], PAD_WIDTH, 'Gray', 'white')
    
    # scores
    #c.draw_text('Player-1 Score:', [WIDTH/8, HEIGHT/8], 20, 'Blue','sans-serif')
    c.draw_text(str(score1), [WIDTH/4, HEIGHT/4], 50, 'Blue','sans-serif')
    c.draw_text(str(score2), [WIDTH*0.75, HEIGHT/4], 50, 'Blue','sans-serif')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 5
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset', new_game)

# start frame
new_game()
frame.start()
