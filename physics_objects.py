'''
physics_objects.py

Desmond Frimpong

This file describes the architecture and behaviour of the objects (block, spike, and ball) used in the game
It has a parent class Thing that the other child classes (Block, Spike, and Ball) inherit from.

'''

import graphicsPlus as gr
import math
import random

class Thing:
    ''' the parent class for simulated abjects'''

    def __init__(self, win, the_type, mass= 1, position= [0, 0], velocity= [0, 0], acceleration= [0, 0], elasticity= 0, color= (0,0,0)):
        ''' a constructor for the class Thing'''

        # A SETUP OF THE FIELDS OF THE CLASS

        self.type = the_type  # specifies the shape of the thing 

        self.position = position    # specifies the position of the thing (default position at origin [0,0])

        self.velocity = velocity    # specifies the velocity of the thing (default velocity is [0,0])

        self.acceleration = acceleration    # specifies the acceleration of the thing (default acceleration is [0,0])

        self.scale = 10      # magnifies the inputs by 10 whenever necessary

        self.win = win   # a graphical window for visualization

        self.vis = [ ]     # container for all the instants of thing

        self.color = color    # defines the color of the thing

        self.drawn = False    # specifies whether an instant of thing is drawn



    # A LIST OF ALL THE GET METHODS FOR THE FIELDS

    def getType(self):
        ''' returns the type of thing'''
        type = self.type
        return type


    def getMass(self):
        '''returns the mass of the ball '''
        mass = self.mass
        return mass
    

    def getPosition(self):
        '''returns the position of the circle'''
        return self.position[:]
    
        
    def getVelocity(self):
        '''returns the velocity of the circle '''
        return self.velocity[:]
    
        
    def getAcceleration(self):
        '''returns the acceleration of the circle'''
        return self.acceleration[:]
    

    def getElasticity(self):
        ''' returns the elasticity of the thing'''
        e = self.elasticity
        return e 


    def getColor(self):
        ''' returns the color of the thing'''
        return self.color



    # THE METHODS FOR THE CLASS 

    def draw(self):
        ''' draws the objects in the vis onto the window'''
        for object in self.vis:
            object.draw(self.win)

        self.drawn = True
    

    def undraw(self):
        ''' undraws the objects in the vis from the window'''
        for object in self.vis:
            object.undraw(self.win)

        self.drawn = False



    # A LIST OF THE SET METHODS FOR THE CLASS
    def setType(self, t):
        ''' sets the type of thing to a new one'''
        self.type = t


    def setMass(self, m):
        ''' sets the mass of the thing to a new one'''
        self.mass = m


    def setPosition(self, px, py):
        ''' changes the position of the thing
        Input: takes the two dimensional components of the new position'''

        x_old = self.position[0]
        y_old = self.position[1]
        
        # calculates the change in position in both directions
        dx = (px - x_old)*self.scale
        dy = (py - y_old)* -self.scale

        # moves each item by the change in position
        for item in self.vis:
            item.move(dx, dy)
        
        self.position = [px, py]


    def setVelocity(self, vx, vy):
        '''changes the velocity of the circle'''
        self.velocity = [vx, vy]


    def setAcceleration(self, ax, ay):
        ''' changes the acceleration of the circle'''
        self.acceleration = [ax, ay]

    
    def setElasticity(self, e):
        ''' resets the elasticity of the thing'''
        self.elasticity = e

    
    def setColor(self, c):
        ''' resets the color of the thing'''
        self.color = c

        if self.color != None:
            for object in self.vis:
                object.setFill(gr.color_rgb(c[0], c[1], c[2]))


    def update(self, dt):
        ''' updates the position of the thing
        Input: takes the time frame for the updates'''

        current_x = self.position[0]
        current_y = self.position[1]

        #updates the position in both directions
        self.position[0] += self.velocity[0]*dt + 0.5*self.acceleration[0] * (dt**2)
        self.position[1] += self.velocity[1]*dt + 0.5*self.acceleration[1] * (dt**2)

        #updates the change in position in both directions
        dx = (self.position[0] - current_x) * self.scale
        dy = (self.position[1] - current_y) * -self.scale

        # moves each item by the change in position
        for item in self.vis:
            item.move(dx, dy)

        #updates the velocity in both directions
        self.velocity[0] += self.acceleration[0]*dt
        self.velocity[1] += self.acceleration[1]*dt


    def fillColor(self, clr):
        '''fills the ball with a color 
        Input: name of color as string'''

        self.clr = clr 
        for item in self.vis:
            item.setFill(self.clr)


    def moveX(self, dx):
        ''' moves the ball horizontally by a magnitude of dx'''

        self.position[0] += dx

        for items in self.vis:
            items.move(dx*self.scale, 0)


    def fillColor(self, clr):
        '''fills the block with a color 
        Input: name of color as string'''

        self.clr = clr 
        for item in self.vis:
            item.setFill(self.clr)

    
    def collision(self, ball):
        ''' checks if there is a collision
        Input: takes a block
        Output: returns True if there is a collision'''

        dx = ball.getPosition()[0] - self.getPosition()[0]
        dy = ball.getPosition()[1] - self.getPosition()[1]

        # checks if there is collision
        if abs(dy) <= ball.getRadius() + self.getHeight()/2 and abs(dx) <= ball.getRadius() + self.getWidth()/2:
            return True
        return False



    

class Ball(Thing):
    '''a class for circular objects'''

    def __init__(self, win, x0= 0, y0= 0, radius= 1, color= (0, 0, 0)):
        ''' constructs a class Ball object '''

        # calls the constructor of the parent class
        Thing.__init__(self, win, 'ball')

        #set up of fields unique to the Ball class
        self.x = x0
        self.y = y0
        self.color = color
        self.radius = radius 
        self.refresh()
        self.setColor(self.color)

    
    # A LIST OF METHODS UNIQUE TO ONLY THE BALL CLASS
    def refresh(self):
        ''' redraws a ball whenever changes are made to the ball's position'''
        drawn = self.drawn
        if drawn:
            self.undraw()

        self.vis = [ gr.Circle((gr.Point(self.position[0]*self.scale,self.win.getHeight() - self.position[1]*self.scale)), self.radius*self.scale)]

        if drawn:
            self.draw()


    def getRadius(self):
        '''returns the radius of the circle'''
        radius = self.radius
        return radius
    

    def setRadius(self, r):
        ''' draws a new circle with a different radius
        Input: takes a new radius value
        Output: draws a circle with the new radius'''

        self.radius = r 
        self.refresh()


class Block(Thing):
    "class for creating rectangular objects"

    def __init__(self, win, width = 2, height = 1, x0=0, y0=0, color = None):
        ''' constructs a class Block object '''

        # calls the constructor of the parent class
        Thing.__init__(self, win, "block")

        #set up of fields unique to the Block class
        self.dx = width
        self.dy = height
        self.position = [x0, y0]
        self.reshape()
        self.setColor(color)


    # A LIST OF METHODS UNIQUE TO ONLY THE BLOCK CLASS

    def reshape(self):
        ''' redraws a ball whenever changes are made to the ball's position'''
        drawn = self.drawn

        if drawn:
            self.undraw()

        win = self.win

        self.vis = [gr.Rectangle(gr.Point((self.position[0] - (self.dx / 2)) * self.scale, win.getHeight() - ((self.position[1] - (self.dy / 2)) * self.scale)), gr.Point((self.position[0] + (self.dx / 2)) * self.scale, win.getHeight() - ((self.position[1] + (self.dy / 2)) * self.scale)))]

        if drawn:
            self.draw()
    
    def getWidth(self):
        return float(self.dx)
    
    def setWidth(self, w):
        self.dx = w
        self.reshape()

    def getHeight(self):
        return float(self.dy)
    
    def setHeight(self, h):
        '''This method makes h the new height of the object.'''
        self.dy = h
        self.reshape()

    def fillColor(self, clr):
        '''fills the block with a color 
        Input: name of color as string'''

        self.clr = clr 
        for item in self.vis:
            item.setFill(self.clr)



class Spike(Thing):
    '''creates spike objects called spike'''

    def __init__(self, win, type, side = 5):
        ''' construct the spike object
        Input: takes in a window, a type of spike to create, and the side length of the spike'''

        # call to the parent class
        Thing.__init__(self, win, "triangle")

        #sets the attributes of the class
        self.win = win
        self.side = side
        self.scale = 10
        self.pos = [win.getWidth()/(2 * self.scale), win.getHeight()/(2*self.scale)]
        self.type = type
        self.clr = ''

        #creates the spikes
        self.createSpike(self.type)


    def createSpike(self, type):
        self.type = type

        if self.type == 'up':
            ''' creates an upward facing triangular spikes'''

            self.vis = [gr.Polygon(gr.Point(self.pos[0]*self.scale, (self.pos[1]-(math.sqrt(3)/2)*self.side)*self.scale), 
                                   gr.Point((self.pos[0]-self.side/2)*self.scale, self.pos[1]*self.scale), 
                                   gr.Point((self.pos[0]+self.side/2)*self.scale, self.pos[1]*self.scale))]

        if self.type == 'down':
            '''creates a downward facing triangular spikes'''

            self.vis = [gr.Polygon(gr.Point(self.pos[0]*self.scale, (self.pos[1]+(math.sqrt(3)/2)*self.side)*self.scale), 
                                   gr.Point((self.pos[0]-self.side/2)*self.scale, self.pos[1]*self.scale), 
                                   gr.Point((self.pos[0]+self.side/2)*self.scale, self.pos[1]*self.scale))]


    def getSide(self):
        ''' returns the side lenght of the spike'''

        side = self.side

        return side
    

    def setSide(self, side):
        ''' set the side lenght to the new side provided'''

        self.side = side

        self.createSpike(self.type)

    
    def getPosition(self):
        ''' returns the position of the spike'''
        return tuple(self.pos)
    

    def setPosition(self, px, py):
        ''' changes the position of the spike
        Input: takes the two dimensional components of the new position'''

        x_old = self.pos[0]
        y_old = self.pos[1]
        
        # calculates the change in position in both directions 
        dx = (px - x_old)*self.scale
        dy = (py - y_old)* -self.scale

        # moves each item by the change in position
        for item in self.vis:
            item.move(dx, dy)
        
        self.pos = [px, py]


    def collision(self, ball):
        ''' checks if there is a collision
        Input: takes a block
        Output: returns True if there is a collision'''

        dx = ball.getPosition()[0] - self.getPosition()[0]
        dy = ball.getPosition()[1] - self.getPosition()[1]

        # checks if there is collision

        if self.type == 'up':

            if abs(dy) <= ball.getRadius() + (math.sqrt(3)/2)*self.side  and abs(dx) <= ball.getRadius() + self.getSide()/2:

                return True

        if self.type == 'down':

            if abs(dy) <= ball.getRadius() + (math.sqrt(3)/2)*self.side  and abs(dx) <= ball.getRadius() + self.getSide()/2:

                return True

        return False
        


        




