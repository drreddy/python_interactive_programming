"""
Notice:
# the game submission is incomplete
# only deal and displaying cards work 
"""

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

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

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
# create two hands one for player another for dealer
class Hand:
    def __init__(self):
        #self.cards = []
        pass	# create Hand object

    def __str__(self):
        pass	# return a string representation of a hand

    def add_card(self, card):
        # use append to add cards like tuples inside tuples
        #self.cards.append([card.get_suit,card.get_rank])
        pass	# add a card object to a hand

    def get_value(self):
        # iterate for tuples inside tuples
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        #score = 0
        #for i in range(len(self.cards)):
        #    score += VALUES[self.cards[i][1]]
        #print score
        pass	# compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        pass	# draw a hand on the canvas, use the draw method for cards
 
        
# define deck class
# deck has all the cards
# self.card_num keeps track of the card coming from the deck
class Deck:
    def __init__(self):
        #self.cards = []
        #self.card_num = 0
        pass	# create a Deck object

    def shuffle(self):
        # shuffle the deck
        #self.cards = range(53)
        #random.shuffle(self.cards)
        pass    # use random.shuffle()

    def deal_card(self):
        # card_num = self.card_num
        #print card_num
        #self.card_num += 1
        pass	# deal a card object from the deck
    
    def __str__(self):
        # print self.cards
        return str((self.cards[self.card_num])/13)+"  "+str((self.cards[self.card_num])%13)
        pass	# return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, dealer_card, player_card1, player_card2, position, player_hand, dealer_hand, card_deck
    #card_deck = Deck()
    #card_deck.shuffle
    
    outcome = range(53)
    random.shuffle(outcome)
    dealer_card = Card(SUITS[outcome[0]/13], RANKS[outcome[0]%13])
    player_card1 = Card(SUITS[outcome[1]/13], RANKS[outcome[1]%13])
    player_card2 = Card(SUITS[outcome[2]/13], RANKS[outcome[2]%13])
    
    """
    player_hand = Hand()
    dealer_hand = Hand()
    player_card = Card
    """
    """
    position = [300, 300]
    outcome = range(53)
    random.shuffle(outcome)
    card = Card(SUITS[outcome[0]/13], RANKS[outcome[0]%13])
    print SUITS[outcome[0]/13], RANKS[outcome[0]%13]    
    # print outcome
    """
    # your code goes here
    
    in_play = True

def hit():
    pass
    # replace with your code below
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    pass	# replace with your code below
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('Blackjack', (100, 90), 40, 'Aqua', 'sans-serif')
    canvas.draw_text('Dealer', (60, 150), 30, 'Black', 'sans-serif')
    canvas.draw_text('Player', (60, 300), 30, 'Black', 'sans-serif')
    #canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    canvas.draw_image(card_back, (CARD_BACK_SIZE[0]/2, CARD_BACK_SIZE[1]/2) , CARD_BACK_SIZE, [96,208], CARD_BACK_SIZE)
    dealer_card.draw(canvas, [200, 160])
    player_card1.draw(canvas, [60, 350])
    player_card2.draw(canvas, [200, 350])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric