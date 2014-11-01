# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player_score = 0
dealer_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}



# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos,hide):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        if not hide:
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        str = "Hand contains"
        for card in self.cards:
           str+= " "+card.suit+card.rank
        return str
    
    def add_card(self, card):
        if isinstance(card,Card):
            self.cards.append(card)

    def get_value(self):
        hand_value = 0
        for card in self.cards:
            hand_value += VALUES[card.rank]
            
        ranks = [i.rank for i in self.cards]
        if not ("A" in ranks):
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
            
    def draw(self, canvas, pos,hide):
        self.cards[0].draw(canvas,pos,hide)
        for card in self.cards[1:]:
            pos[0] += CARD_SIZE[1] + 10
            card.draw(canvas,pos,False)
 

        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = [Card(i,j) for i in SUITS for j in VALUES]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        str = "Deck contains"
        for card in self.cards:
           str+= " "+card.suit+card.rank
        return str



#define event handlers for buttons
def deal():
    global outcome, in_play,score,dealer_score
    global game_deck,player_hand,dealer_hand

    if not in_play:
        game_deck = Deck()
        game_deck.shuffle()
        
        player_hand = Hand()
        dealer_hand = Hand()
        
        player_hand.add_card(game_deck.deal_card())
        player_hand.add_card(game_deck.deal_card())
        
        dealer_hand.add_card(game_deck.deal_card())
        dealer_hand.add_card(game_deck.deal_card())
        
        outcome = "Hit or stand?"
        
        in_play = True
    else:
        outcome = "Player surrended. New Deal?"
        score -= 1
        dealer_score += 1
        in_play = False

def hit():
    global outcome,in_play,score,dealer_score
    global player_hand,game_deck
    if in_play:
        player_hand.add_card(game_deck.deal_card())
    
        if player_hand.get_value() > 21:
            outcome = "You bust with "+str(player_hand.get_value())+". New deal?"
            in_play = False
            score -= 1
            dealer_score += 1
       
def stand():
    global outcome,in_play,score,dealer_score,player_score
    global dealer_hand,player_hand,game_deck
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(game_deck.deal_card())
            
        if dealer_hand.get_value() > 21:
            outcome = "You win! Dealer has busted with "+str(dealer_hand.get_value())+". New deal?"
            score += 1
            player_score += 1
        else:
            if player_hand.get_value() <= dealer_hand.get_value():
                outcome = "You lose! "+str(player_hand.get_value())+" vs " \
                +str(dealer_hand.get_value())+". New deal?"
                score -= 1
                dealer_score += 1
            else:
                outcome = "You win! "+str(player_hand.get_value())+" vs " \
                +str(dealer_hand.get_value())+". New deal?"
                score += 1
                player_score += 1
        in_play = False  


# draw handler    
def draw(canvas):
    global outcome
    global player_hand,dealer_hand
    global score,deal_score,player_score
    
    canvas.draw_text("Blackjack",[250,50],36,"Black")
    
    canvas.draw_text("Dealer Score = "+str(dealer_score),[100,300],24,"White")
    canvas.draw_text("Player Score = "+str(player_score),[100,330],24,"White")
    canvas.draw_text("Score = "+str(score),[100,360],24,"White")

    dealer_hand.draw(canvas,[20,150],in_play)
    player_hand.draw(canvas,[20,450],False)
    
    canvas.draw_text("Player value: "+str(player_hand.get_value()),[30,580],24,"White")
    canvas.draw_text(outcome,[50,100],24,"White")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# starting things
deal()
frame.start()