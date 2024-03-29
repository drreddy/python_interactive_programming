"""
Implementation of Spaceship Arcade game RiceRocks
Developed by: Rajeev Reddy
http://drreddy.herokuapp.com
"""

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

max_rocks = 12
no_rocks = 0

rock_group = set()
missile_group = set()
explosion_group = set()
soundtrack_time = 0 

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # print self.pos
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global a_missile, missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            
            explosion_index = (self.age - 1)
            
            image_center = [self.image_center[0] + explosion_index * self.image_size[0], 
                     self.image_center[1]]
            
            canvas.draw_image(self.image, image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
            
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        if self.age >= self.lifespan:
            return False
        else:
            self.age += 1
            
            # update angle
            self.angle += self.angle_vel
            
            # update position
            self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
            self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
            
            return True
        
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def collide(self, other_object):
        distance = dist(self.get_position(), other_object.get_position())
        if distance <= self.radius + other_object.get_radius():
            return True
  
        
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, score, lives, soundtrack
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        score = 0
        lives = 3
        soundtrack.play()
        

def draw(canvas):
    global time, started, lives, rock_group, no_rocks, score, soundtrack_time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)   
    
    # update ship and sprites
    my_ship.update()
    
    
    # test cases
    #a_rock.draw(canvas)
    #a_missile.draw(canvas)
    #a_explosion.draw(canvas)
    #a_explosion.update()
    #a_rock.update()
    #a_missile.update()

    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    
    if group_collide(rock_group, my_ship):
        lives -= collide_no
        no_rocks -= collide_no
        
    if group_group_collide(rock_group, missile_group):
        score += score_update
        no_rocks -= score_update
    
    process_sprite_group(canvas, explosion_group)
        
    if lives == 0:
        rock_group = set()
        started = False
        soundtrack_time = 0
        soundtrack.rewind()
    
    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

# timer handler that spawns a rock    
def rock_spawner():
    
    global max_rocks, no_rocks, rock_group
    
    if (no_rocks < max_rocks) and started:
       
        """
        randomness = random.choice([1, 2, 3, 4])
        if randomness == 1:
            rock_pos = [random.randrange(0, WIDTH/4), random.randrange(0, HEIGHT)]    
        elif randomness == 2:
            rock_pos = [random.randrange(3*WIDTH/4, WIDTH), random.randrange(0, HEIGHT)]
        elif randomness == 3:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT/5)]
        else:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(4*HEIGHT/5, HEIGHT)]
        """
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        
        rock_vel = [random.random() * .7 - .3, random.random() * .7 - .3]
        rock_avel = random.random() * .2 - .1
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        
        if dist(rock_pos, my_ship.pos) >= 80:
            rock_group.add(a_rock)
            no_rocks += 1
    else:
        # print len(rock_group)
        pass      

# sountrack helper function
def soundtrack_helper():
    global started, soundtrack_time, soundtrack
    
    if started:
        soundtrack_time += 1
        
    if started and (soundtrack_time >= 175):
        soundtrack_time = 0 
        soundtrack.rewind()
        soundtrack.play()
    
    
# to update the sprite
def process_sprite_group(canvas, set_to_process):
    remove_group = set()
    if len(set_to_process) != 0:
        for things in set_to_process:
            # to check if the age exceeded life span
            if things.update():
                things.draw(canvas)
            else:
                remove_group.add(things)
    
    set_to_process.difference_update(remove_group)

# group collide function
def group_collide(group, other_object):
    global collide_no, explosion_group
    remove_list = set()
    for sprite in group:
        if sprite.collide(other_object):
            remove_list.add(sprite)
            explosion_pos = sprite.get_position()
            new_explosion = Sprite(explosion_pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(new_explosion)

    if len(remove_list) == 0:
        return False
    else:
        group.difference_update(remove_list)
        collide_no = len(remove_list)
        return True
    
# group group collide for two sprites
def group_group_collide(first_group, second_group):
    global score_update
    remove_list=set()
    for sprite in first_group:
        if group_collide(second_group, sprite):
            remove_list.add(sprite)
            
    if len(remove_list) != 0:
        first_group.difference_update(remove_list)
        score_update = len(remove_list)
        return True
    else:
        return False

# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
global my_ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# test cases
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
#a_explosion = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)


# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)	

rock_timer = simplegui.create_timer(1000.0, rock_spawner)
soundtrack_timer = simplegui.create_timer(1000.0, soundtrack_helper)

# get things rolling
rock_timer.start()
soundtrack_timer.start()
frame.start()
