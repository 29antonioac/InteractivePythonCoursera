# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [2, 2]

score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2
    
    # Supposed that SimpleGUI calls the draw handler 60 times/second,
    # for obtaining pixels/second velocity I need to divide by 60
    # the initial velocity
    
    x_vel = random.randrange(120, 240)	/ 60 	# For pixels/second
    y_vel = random.randrange(60, 180)	/ 60	# For pixels/second
    
    if direction == "RIGHT":
        ball_vel[0] = x_vel
        ball_vel[1] = -y_vel
    else:
        ball_vel[0] = -x_vel
        ball_vel[1] = -y_vel
        

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT / 2 - HALF_PAD_HEIGHT]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH + 1, HEIGHT / 2 - HALF_PAD_HEIGHT]
    
    paddle1_vel = 0
    paddle2_vel = 0
    
    score1 = 0
    score2 = 0
    
    spawn_ball("RIGHT")

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos[1] and ball_pos[1] <= paddle1_pos[1] + PAD_HEIGHT:
            ball_vel[0] *= -1.1
        else:
            score2 += 1
            spawn_ball("RIGHT")
            
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - 1 - PAD_WIDTH:
        if ball_pos[1] >= paddle2_pos[1] and ball_pos[1] <= paddle2_pos[1] + PAD_HEIGHT:
            ball_vel[0] *= -1.1
        else: 
            score1 += 1
            spawn_ball("LEFT")
        
    # Bouncing off both walls
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= HEIGHT - 1:
        ball_vel[1] *= -1
    
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, 20, 5, 'Blue', 'White')
    
    # update paddle's vertical position, keep paddle on the screen
    
    future_pos = paddle1_pos[1] + paddle1_vel
    if future_pos > 0 and future_pos + PAD_HEIGHT < HEIGHT:
        paddle1_pos[1] = future_pos
    
    future_pos = paddle2_pos[1] + paddle2_vel
    if future_pos > 0 and future_pos + PAD_HEIGHT < HEIGHT:
        paddle2_pos[1] = future_pos
        
    # draw paddles
    canvas.draw_line(paddle1_pos,[paddle1_pos[0],paddle1_pos[1]+PAD_HEIGHT],PAD_WIDTH,"White")
    canvas.draw_line(paddle2_pos,[paddle2_pos[0],paddle2_pos[1]+PAD_HEIGHT],PAD_WIDTH,"White")
    
    # draw scores
    canvas.draw_text(str(score1),[WIDTH / 2- 75, 100], 36, "Blue")
    canvas.draw_text(str(score2),[WIDTH / 2 + 50, 100], 36, "Blue")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -3
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 3
            
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 3
    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
   
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart",new_game)


# start frame
new_game()
frame.start()
