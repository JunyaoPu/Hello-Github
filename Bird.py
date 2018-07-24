import random
import pygame
import numpy
import math

class BIRD:
    #position
    x = 0
    y = 0
    #the distance bird fly
    distance =0
    #parameters for running the game
    score =0
    birdVelY = 0
    birdFlapped = False
    xMidPos = 0
    #neural network
    w1 = 0.0
    w2 = 0.0
    b  =0.0

    input1 = 0.0      #x
    input2 = 0.0      #y
    output = 0.0

    def __init__(self):
        self.y = random.randint(100, 300)
        self.w1 = numpy.random.randn()
        self.w2 = numpy.random.randn()
        self.b = 0#numpy.random.randn()

    #send inputs to the class
    def input(self, input1, input2):
        self.input1 = input1
        self.input2 = input2

    #was tring to do the sigmoid function
    def Sigmoid(self):
        w1 = self.w1
        w2 = self.w2
        I1 = self.input1
        I2 = self.input2
        #total = self.input1*self.w1 + self.input2 *self.w2 + self.b
        total = I1 * w1 + I2 * w1 + I2 * w2
        self.output = total
        #self.output = 1/(1 + math.exp(-total))
    #fly up if output is positive.
    def fly_up(self):
        #print(self.output)
        if self.output > 0.0:
            return True
        else:
            return False
    #random output
    def fly_up_random(self):
        output = random.randint(1, 6)/10
        #print(output)

        if output >0.5:
            return True
        else:
            return False
