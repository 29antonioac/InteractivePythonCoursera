# implementation of card game - Memory

import simplegui
import random

"""
Card size = 70x96
Canvas size = (280+5*separation)x(386+5*separation)
"""

# constants of the game
CARD_WIDTH = 70
CARD_HEIGHT = 96

HALF_CARD_WIDTH = CARD_WIDTH / 2
HALF_CARD_HEIGHT = CARD_HEIGHT / 2

CARD_SIZE = [CARD_WIDTH, CARD_HEIGHT]
CARD_CENTER = [CARD_WIDTH / 2, CARD_HEIGHT / 2]

# supposed a square grid
CARDS_PER_SIDE = 4
SEPARATION = CARDS_PER_SIDE + 1

# canvas width and height
WIDTH = CARDS_PER_SIDE*CARD_WIDTH+(CARDS_PER_SIDE + 1)*SEPARATION
HEIGHT = CARDS_PER_SIDE*CARD_HEIGHT+(CARDS_PER_SIDE + 1)*SEPARATION

# path of the images
path = ["https://www.dropbox.com/s/gdgppm3mss3f8nx/1.png?dl=1", \
        "https://www.dropbox.com/s/g82d4hafqxu8bza/2.png?dl=1", \
        "https://www.dropbox.com/s/al802fgagf6iq3r/3.png?dl=1", \
        "https://www.dropbox.com/s/u98e62ab50ln72e/4.png?dl=1", \
        "https://www.dropbox.com/s/nqelcebaz0aqtuq/5.png?dl=1", \
        "https://www.dropbox.com/s/s1b7twzmosps34m/6.png?dl=1", \
        "https://www.dropbox.com/s/xsie0wen068yqwu/7.png?dl=1", \
        "https://www.dropbox.com/s/qoydck8787l0ejs/8.png?dl=1"]

path_hidden = "https://www.dropbox.com/s/q93yk3zehtprnba/hidden.png?dl=1"

# calculate the center of each card
card_centers = []

for i in range(CARDS_PER_SIDE):
    for j in range(CARDS_PER_SIDE):
        card_centers.append([(j+1)*SEPARATION + (j+0.5)*CARD_WIDTH, \
                             (i+1)*SEPARATION + (i+0.5)*CARD_HEIGHT ])
      
# add number card images to a dictionary. The key is the number of the card 
cards = {}

for i in range(1,len(path) + 1):
    cards[i] = simplegui.load_image(path[i-1])
 
hidden = simplegui.load_image(path_hidden)


# create index of the cards
indexes = [i for i in range(1,len(path) + 1)]
indexes.extend(indexes)

# actual cards exposed
actual_card = [-1,-1]

# I have won?
win = False
# Are hidden card image loaded?
hidden_loaded = False
# Are number card images loaded?
cards_loaded = False
            
# helper function to initialize globals
def new_game():
    global cards,hidden,exposed,state,turns,win
    
    state = 0
    turns = 0
    
    random.shuffle(indexes)
    
    exposed = [False for i in range(2*len(path))]
    
    win = False
    
def check_images():
    global hidden_loaded,cards_loaded,hidden,cards
    
    # check the hidden card
    if not hidden_loaded and not hidden.get_width() == 0:
        hidden_loaded = True
        
    # check the number cards
    cards_loaded = True
    for i in cards:
        if cards[i].get_width() == 0:
            cards_loaded = False
            break
     
# define event handlers
def mouseclick(pos):
    global state,turns,actual_card,win,hidden_loaded,hidden
    
    # check if the images are loaded
    check_images()
    
    # add game state logic here
    if not win:
        for i in range(len(card_centers)):
            # check if the clicked position is in the "i" card
            if pos[0] <= card_centers[i][0] + HALF_CARD_WIDTH \
                and pos[0] >= card_centers[i][0] - HALF_CARD_WIDTH  \
                and pos[1] <= card_centers[i][1] + HALF_CARD_HEIGHT \
                and pos[1] >= card_centers[i][1] - HALF_CARD_HEIGHT:
                    if not exposed[i]:
                        exposed[i] = True
                        # if we're in the initial state, we expose the first card
                        if state == 0:
                            state = 1
                            actual_card[0] = i
                        # if there is a card exposed, we expose the second card
                        # and check if I win
                        elif state == 1:
                            state = 2
                            actual_card[1] = i
                            turns += 1
                            
                            # check if I win
                            win = True
                            for j in range(len(exposed)):
                                if exposed[j] == False:
                                    win = False
                                    break
                        else:
                            # when I flip a third card we check the last 2 exposed
                            # and expose one more
                            state = 1
                            # check if the cards are paired
                            if indexes[actual_card[0]] != indexes[actual_card[1]]:
                                exposed[actual_card[0]] = False
                                exposed[actual_card[1]] = False
                                actual_card[0] = actual_card[1] = -1
                                
                            actual_card[0] = i
                    # if clicked inside a card, break
                    # we can't click two cards togheter
                    break
                       
# cards are 70x96 pixels in size    
def draw(canvas):
    for i in range(2*len(path)):
        
        if exposed[i]:
            # if I have images, I show them
            if cards_loaded:
                canvas.draw_image(cards[indexes[i]],CARD_CENTER, CARD_SIZE, \
                                  card_centers[i], CARD_SIZE)
            # else I show text
            else:
                C_width = frame.get_canvas_textwidth(str(indexes[i]), 24)
                upper_left_corner = [card_centers[i][0] - HALF_CARD_WIDTH, card_centers[i][1] - HALF_CARD_HEIGHT]
                upper_right_corner = [card_centers[i][0] + HALF_CARD_WIDTH, card_centers[i][1] - HALF_CARD_HEIGHT]
                down_left_corner = [card_centers[i][0] - HALF_CARD_WIDTH, card_centers[i][1] + HALF_CARD_HEIGHT]
                down_right_corner = [card_centers[i][0] + HALF_CARD_WIDTH, card_centers[i][1] + HALF_CARD_HEIGHT]
                
                canvas.draw_polygon([upper_left_corner, down_left_corner, down_right_corner,upper_right_corner], 1, 'Black','White')
                canvas.draw_text(str(indexes[i]),[card_centers[i][0] - C_width / 2,card_centers[i][1]], 24, \
                                  "Black")
        else:
            # if I have the hidden card image, I show it
            if hidden_loaded:
                canvas.draw_image(hidden,CARD_CENTER, CARD_SIZE, \
                                  card_centers[i], CARD_SIZE)
            # else I show text    
            else:
                H_width = frame.get_canvas_textwidth("H", 24)
                upper_left_corner = [card_centers[i][0] - HALF_CARD_WIDTH, card_centers[i][1] - HALF_CARD_HEIGHT]
                upper_right_corner = [card_centers[i][0] + HALF_CARD_WIDTH, card_centers[i][1] - HALF_CARD_HEIGHT]
                down_left_corner = [card_centers[i][0] - HALF_CARD_WIDTH, card_centers[i][1] + HALF_CARD_HEIGHT]
                down_right_corner = [card_centers[i][0] + HALF_CARD_WIDTH, card_centers[i][1] + HALF_CARD_HEIGHT]
                
                canvas.draw_polygon([upper_left_corner, down_left_corner, down_right_corner,upper_right_corner], 1, 'White','Black')
                canvas.draw_text("H",[card_centers[i][0] - H_width / 2,card_centers[i][1]], 24, \
                                  "White")
        # if I win show VICTORY! in the canvas               
        if win:
            canvas.draw_polygon([card_centers[4], card_centers[8], card_centers[11],card_centers[7]], 12, 'Black','Black')
            canvas.draw_text('VICTORY!', (card_centers[8][0]+7, card_centers[8][1]-35), 45, 'White')
    
    # update the turns label
    label.set_text("Turns = "+str(turns))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
frame.set_canvas_background("Green")

# get things rolling
new_game()
check_images()
frame.start()