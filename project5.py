"""
implementation of card game - Memory

Submitted by:
Rajeev Reddy
website:http://drreddy.herokuapp.com
"""

import simplegui
import random	

# helper function to initialize globals
def new_game():
    global final_list,list2,exposed,turns,state
    final_list = range(8)
    list2 = range(8)
    final_list.extend(list2)
    random.shuffle(final_list)
    turns = 0
    state = 0
    label.set_text('Turns = '+str(turns))
    exposed = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]

     
# event handlers
def mouseclick(pos):
    global state,exposed,flipped1,flipped2,turns
    
    i = pos[0]/50
    # game state logic should be implemented when clicked on not exposed card
    if not exposed[i]:
        exposed[i] = True
        # game state logic
        if state == 0:
            state = 1
            flipped1 = i
            #label.set_text('Opened card = '+str(flipped1))
        elif state == 1:
            state = 2
            flipped2 = i
            turns = turns + 1
            label.set_text('Turns = '+str(turns))
            #label.set_text('Opened card 1 and 2 = '+str(flipped1)+' and '+str(flipped2))
        else:
            state = 1
            if final_list[flipped1]!= final_list[flipped2]:
                exposed[flipped1] = False
                exposed[flipped2] = False
            flipped1 = i
            #label.set_text('Opened card = '+str(flipped1))
    
                            
def draw(canvas):
    for i in range(16):
        canvas.draw_text(str(final_list[i]), (15+i*50, 60), 40, 'White', 'sans-serif')
        # if exposed is false then only show the green card on above
        if not exposed[i]:
            canvas.draw_polygon([[25+i*50, 0], [25+i*50, 100]], 48, 'Green')

# frame, button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

new_game()
frame.start()
