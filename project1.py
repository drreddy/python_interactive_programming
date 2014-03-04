"""
Rock-paper-scissors-lizard-Spock python program
using random number generator 

Developed by Rajeev Reddy
Website: http://drreddy.herokuapp.com
"""
import random

def number_to_name(number):
    #helper funtion to convert given number to name
    
    if number == 0:
        val = "rock"
    elif number == 1:
        val = "Spock"
    elif number == 2:
        val = "paper"
    elif number == 3:
        val = "lizard"
    elif number == 4:
        val = "scissors"
    else:
        # use of raise to exit further program and print error
        print ""
        print "Error : Number out of range"
        raise
    return val

    
def name_to_number(name):
    #helper funtion to convert given name to number
    
    if name == "rock":
        val = 0
    elif name == "Spock":
        val = 1
    elif name == "paper":
        val = 2
    elif name == "lizard":
        val = 3
    elif name == "scissors":
        val = 4
    else:
        # use of raise to exit further program and print error
        print ""
        print "Error : Please check the choice provided is not valid"
        raise
    return val

def rpsls(name): 
    #main funtion to check for the result
    
    player_number = name_to_number(name)

    comp_number = random.randrange(0,5)
    
    #check variable to get result using modulos
    
    check = (player_number - comp_number)%5.0

    if check == 1 or check == 2:
        result = "Player wins !"
    elif check == 3 or check == 4:
        result = "Computer wins !"
    else:
        result = "Player and computer tie!"

    comp_name = number_to_name(comp_number)

    print ""
    print "Player chooses " + name 
    print "Computer chooses " + comp_name
    print result

rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")



