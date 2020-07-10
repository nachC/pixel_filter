import numpy as np
import cv2 as cv
import random
import math

# moving particle Class
class Particle:
    def __init__(self, img, position, color):
        self.img = img
        self.position = list(position)
        self.color = color
        self.color.append(0)
        self.thickness = 1
        self.ang = random.random() * 0.25 * math.pi * random.choice([-1, 1])
        self.vel = 1.6
        self.alive = True
        #self.count = 0
    
    def display(self):
        cv.circle(self.img, tuple(self.position), self.thickness, tuple(self.color), -1)

    def move(self):
        self.ang = self.ang + math.radians(random.randint(-10, 10))
        self.dx = self.vel * math.cos(self.ang)
        self.dy = self.vel * math.sin(self.ang)
        self.position[0] = self.position[0] + int(self.dx)
        self.position[1] = self.position[1] + int(self.dy)

        #self.count = self.count + 1
        self.prob = random.randint(0,99)
        if self.prob < 10:
            self.alive = False

    def updateImage(self, new_image):
        self.img = new_image
    
    def isAlive(self):
        return self.alive
        
    
# MAIN
particles = [] # array holding all the particles created
selecting_pixels = False # true if mouse is pressed
done_selecting = False
pixels_dict = {} # dict holding the pixels selected by the user. Pixel coordinates as keys, pixel color as value
img = cv.imread('state.jpg') # loading the image from the root folder
img_copy = img.copy() # copy the original image to work on the copy and keep the original intact to refresh the screen

# mouse callback function
def select_pixels(event,x,y,flags,param):
    global selecting_pixels, done_selecting
    if event == cv.EVENT_LBUTTONDOWN:
        selecting_pixels = True
    elif event == cv.EVENT_MOUSEMOVE:
        if selecting_pixels == True:
            for i in range(-2, 2):
                pixels_dict[(x+i,y+i)] = [img_copy.item(y+i,x+i,0), img_copy.item(y+i,x+i,1), img_copy.item(y+i,x+i,2)]
    elif event == cv.EVENT_LBUTTONUP:
        selecting_pixels = False
        done_selecting = True

cv.namedWindow('image')
cv.setMouseCallback('image',select_pixels)

while(True):
    img_copy = img.copy()
    if done_selecting:
        for key in pixels_dict:
            particles.append(Particle(img_copy, key, [int(x) for x in pixels_dict[key]]))

    for particle in particles:
        if particle.isAlive():
            particle.updateImage(img_copy)
            particle.move()
            particle.display()
        else:
            particles.remove(particle)

    cv.imshow('image', img_copy)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()
