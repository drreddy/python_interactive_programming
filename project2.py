"""
Guess the number game

Submitted by:
Rajeev Reddy
website : http://drreddy.herokuapp.com
"""

import simplegui
import random
import math


# initially range is for 100
secret_num = float(random.randrange(0,100))
# range_int keeps track of what range the user wants
range_int = 100
#guess_num is the variable to keep track of available guesses
guess_num = 7
#count is the variable to keep track of no of guesses
count = 0

# helper function to start and restart the game
def new_game():
    global count
    count = 0
    print "New game. Range is from 0 to", range_int
    print "Number of remaining guesses is", guess_num
    print " "

def range100():
    # button that changes range to range [0,100) and restarts
    
    global secret_num, range_int, guess_num
    secret_num = float(random.randrange(0,100))
    range_int = 100
    guess_num = 7
    new_game()  

def range1000():    
    # button that changes range to range [0,1000) and restarts
    
    global secret_num, range_int, guess_num
    secret_num = float(random.randrange(0,1000))
    range_int = 1000
    guess_num = 10
    new_game()

def input_guess(guess):
    # range_int to check the range, guess_num to check number of guesses
    
    global range_int, count , guess_num
    count = count + 1
    guess_float = float(guess)
    #until count < number of available guess we continue the checking
    if count < guess_num: 
        if guess_float > secret_num:
            print "Your guess value was", guess_float
            print "Higher guess value !"
            print "Number of remaining guesses is", guess_num-count
            print " "
        elif guess_float < secret_num:
            print "Your guess value was", guess_float
            print "Lower guess value !"
            print "Number of remaining guesses is", guess_num-count
            print " "
        else:
            print "Your guess value was", guess_float
            print "Congrats, your guess is correct"
            print "Number of remaining guesses is", guess_num-count
            print " "
            #range_int is used to decide in which range new function must be called
            if range_int == 100:
                range100()
            else:
                range1000()
    else:
        if guess_float > secret_num:
            print "Your guess value was", guess_float
            print "Number of remaining guesses is", guess_num-count
            print "Sorry, You ran out of guesses. The number was:", secret_num
            print " "
            #range_int is used to decide in which range new function must be called
            if range_int == 100:
                range100()
            else:
                range1000()
        elif guess_float < secret_num:
            print "Your guess value was", guess_float
            print "Number of remaining guesses is", guess_num-count
            print "Sorry, You ran out of guesses. The number was:", secret_num
            print " "
            #range_int is used to decide in which range new function must be called
            if range_int == 100:
                range100()
            else:
                range1000()
        else:
            print "Your guess value was", guess_float
            print "Congrats, your guess is correct"
            print "Number of remaining guesses is", guess_num-count
            print " "
            #range_int is used to decide in which range new function must be called
            if range_int == 100:
                range100()
            else:
                range1000()
    
    
# create frame

f = simplegui.create_frame('Guess The Number', 300, 200)

# register event handlers for control elements

button_range_100 = f.add_button('Range: 0 - 100', range100, 200)
button_range_1000 = f.add_button('Range: 0 - 1000', range1000, 200)
line_break = f.add_label(' ')
guess = f.add_input('Guess: ', input_guess, 200)

# call new_game and start frame

new_game()
f.start
