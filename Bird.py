import random
import pygame
import numpy as np
import math

import copy

class BIRD:
    #position
    x = 0
    y = 0
    #the distance bird fly
    distance =0
    #parameters for running the game
    birdVelY = 0

    birdFlapped = False

    output = 0.0


    '''do it by np.mat'''
    input_num     = 2
    hidden_num1   = 8
    hidden_num2   = 8
    layer_num     = 2

    input_mat      = 0.0
    hidden1_mat    = 0.0
    hidden2_mat    = 0.0
    bias1_mat      = 0.0
    bias2_mat      = 0.0

    score          = 0
    fitness        = 0


    def __init__(self):
        #self.y = random.randint(100, 300)
        self.y = 150
        #referece diffirent memory
        input         = [0.0 for i in range(self.input_num)]
        hidden1       = [0.0 for i in range(self.hidden_num1 * self.input_num)]
        hidden2       = [0.0 for i in range(self.hidden_num2 * self.hidden_num1)]
        bias1         = [0.0 for i in range(self.hidden_num1)]
        bias2         = [0.0 for i in range(self.hidden_num2)]

        #make it as Matrix
        self.input_mat      = np.mat(np.reshape(input,(self.input_num,1))) #input col Matrix
        self.hidden1_mat    = np.mat(np.reshape(hidden1,(self.hidden_num1,self.input_num)))
        self.hidden2_mat    = np.mat(np.reshape(hidden2,(self.hidden_num2,self.hidden_num1)))
        self.bias1_mat      = np.mat(np.reshape(bias1,(self.hidden_num1,1)))
        self.bias2_mat      = np.mat(np.reshape(bias2,(self.hidden_num2,1)))


    '''set up for two hidden layer neural network'''
    def set_up(self):
        '''
        #change this
        rand1              = [float(np.random.randn()) for i in range(self.layer_num)]
        rand2              = [float(np.random.randn()) for i in range(self.hidden_num1)]
        rand3              = [float(np.random.randn()) for i in range(self.hidden_num2)]
        #print(self.rand1)
        #biases
        for i in range(self.hidden_num1):
            self.bias1_mat[i,0]    = rand1[0]


        for i in range(self.hidden_num2):
            self.bias2_mat[i,0]    = rand1[1]

        #hidden layer1
        for i in range(self.hidden_num1):
            for j in range(self.input_num):
                self.hidden1_mat[i,j]    = rand2[i]

        #hidden layer2
        for i in range(self.hidden_num2):
            for j in range(self.hidden_num1):
                self.hidden2_mat[i,j]    = rand3[i]

        '''
        for i in range(self.hidden_num1):
            self.bias1_mat[i,0]    = np.random.randn()


        for i in range(self.hidden_num2):
            self.bias2_mat[i,0]    = np.random.randn()

        #hidden layer1
        for i in range(self.hidden_num1):
            for j in range(self.input_num):
                self.hidden1_mat[i,j]    = np.random.randn()

        #hidden layer2
        for i in range(self.hidden_num2):
            for j in range(self.hidden_num1):
                self.hidden2_mat[i,j]    = np.random.randn()

    '''predict the bird shoud do action or not'''
    def predict(self, input1,input2):
        norm                    = np.sqrt(input1 ** 2 + input2 ** 2)
        input1                  = input1 / norm
        input2                  = input2 / norm
        self.input_mat[0,0]   = input1
        self.input_mat[1,0]   = input2

        #calculation
        step_1    = self.hidden1_mat * self.input_mat

        step_2    = step_1 + self.bias1_mat

        step_3    = self.hidden2_mat * step_2

        step_4    = step_3 + self.bias2_mat

        total = 0
        for i in range(self.hidden_num2):
            total = step_4[i,0]
        '''
        total = 0
        for i in range(self.hidden_num1):
            total = step_2[i,0]
        '''
        self.output = self.sigmoid_fun(total)



    def fly_up(self):
        #print(self.output)
        if self.output > 0.5:
            return True
        else:
            return False


    def sigmoid_fun(self, x):

        return 1 / (1 + np.exp(-x))





class BEST_BIRD:
    #position
    x = 0
    y = 0
    #the distance bird fly
    distance =0
    #parameters for running the game
    birdVelY = 0
    birdFlapped = False
    output = 0.0


    '''do it by np.mat'''
    input_num     = 2
    hidden_num1   = 8
    hidden_num2   = 8
    layer_num     = 2

    input_mat      = 0.0
    hidden1_mat    = 0.0
    hidden2_mat    = 0.0
    bias1_mat      = 0.0
    bias2_mat      = 0.0

    score          = 0
    fitness        = 0


    def __init__(self):
        self.y = random.randint(100, 300)
        #self.y = 150
        #referece diffirent memory
        input         = [0.0 for i in range(self.input_num)]
        hidden1       = [0.0 for i in range(self.hidden_num1 * self.input_num)]
        hidden2       = [0.0 for i in range(self.hidden_num2 * self.hidden_num1)]
        bias1         = [0.0 for i in range(self.hidden_num1)]
        bias2         = [0.0 for i in range(self.hidden_num2)]

        #make it as Matrix
        self.input_mat      = np.mat(np.reshape(input,(self.input_num,1))) #input col Matrix

        #-7
        self.hidden1_mat    = np.mat([[-1.1006055,   1.68611828],
                                    [ 0.58244688,  1.32232458],
                                    [-1.36709868, -0.99262664],
                                    [-0.09820225, -0.65166291],
                                    [ 0.00555047,  0.36992554],
                                    [ 0.68712833,  0.59899405],
                                    [-0.66508623,  0.21805007],
                                    [-0.61897766, -0.14057781]])

        self.hidden2_mat    = np.mat([[-0.40592005,  1.24114577, -0.439257,   -1.3844009,  -0.13446789, -0.86667637,
                                    -0.23208038, -0.28774448],
                                    [ 0.22904166, -0.19770246, -1.01923846 , 1.48699355, -1.86696029,  0.95419772,
                                    -0.99559001,  0.88669873],
                                    [ 1.42441151, -0.48174647 , 0.13624514  ,1.73345187 ,-1.74980462 , 0.24993313,
                                    -0.37164299,  0.6258438 ],
                                    [ 0.39130992,  0.5588771 ,  1.70264003  ,0.03768926 ,-0.90461728 ,-0.07985956,
                                    0.61827901,  0.5596225 ],
                                    [ 0.64107738,  0.6001062 , -0.9398967   ,0.51285343 ,-1.40198313 ,-1.23854723,
                                    0.65218236,  0.1844194 ],
                                    [ 0.397864  ,  0.89155813 ,-1.43536686 ,-0.33761961  ,0.38142812, -2.56778518,
                                    0.20145048,  0.75226566],
                                    [ 0.37250409, -1.68196919 ,-0.0168179  , 2.26496997  ,0.95728919  ,0.30060659,
                                    -0.28028209, -0.17866201],
                                    [ 0.18757496,  1.14497615 ,-0.60951418 , 1.52978482  ,1.18461165  ,0.16050369,
                                    0.77068999,  2.70482301]])
        self.bias1_mat      = np.mat([[ 0.37760881],
                                    [ 0.76697618],
                                    [-0.15096613],
                                    [-1.72024613],
                                    [ 0.18510986],
                                    [-0.5280124 ],
                                    [ 2.23147291],
                                    [-0.06155905]])
        self.bias2_mat      = np.mat([[-0.41845339],
                                    [ 1.16553414],
                                    [ 0.17454144],
                                    [-0.60197645],
                                    [-1.92373374],
                                    [ 1.63557427],
                                    [ 0.87064227],
                                    [-0.06817852]])

        '''
        #-4
        self.hidden1_mat    = np.mat([[-1.65875214 ,-1.23275933],
                                    [-0.98653774, -1.18383409],
                                    [ 1.66541536,  1.36589021],
                                    [ 0.69793897,  0.55791459],
                                    [-0.43790276, -0.21970416],
                                    [ 0.82743906,  0.09587558],
                                    [-1.14562856, -1.33783167],
                                    [-0.35562154, -0.22858402]])

        self.hidden2_mat    = np.mat([[ 0.42853772,  0.53741645,  0.23003246 , 0.23578622 , 0.37023396 , 0.5212848
                                    ,0.42498436,  0.39828996],
                                    [-0.90346906, -1.16821274, -0.8565058,  -0.93396236 ,-1.12019613, -1.13782187
                                    ,-0.98033214, -0.80821664],
                                    [ 2.1197865 ,  2.43587561 , 2.14845936 , 2.16579742 , 2.33116157 , 1.79291129
                                    ,2.35203292  ,2.18836589],
                                    [-1.04846351 ,-1.41822194, -1.04159379, -1.32652281, -1.23446738 ,-1.09930452
                                    ,-1.38659942, -0.88862525],
                                    [ 1.098634 ,   1.03145274 , 1.27927999 , 1.08546469 , 0.84711654,  0.79282134
                                    ,0.47143912,  0.79135909],
                                    [ 1.45951914,  0.91690854 , 0.9215812 ,  0.97568853 , 0.78772681 , 0.63433544
                                    ,1.17557074 , 1.04614863],
                                    [-1.01315094 ,-1.29937825, -1.51770446 ,-1.3795316 , -1.51032939 ,-1.22156672
                                    ,-1.59974041 ,-1.26235239],
                                    [-0.33429798 ,-0.70560917 ,-0.90732447 ,-0.78659995, -0.40672608, -0.63310652
                                    ,-0.5746702 , -0.67317443]])
        self.bias1_mat      = np.mat([[ 0.09444711],
                                    [ 0.14169232],
                                    [ 0.07418327],
                                    [-0.22478199],
                                    [ 0.06970684],
                                    [-0.08614232],
                                    [ 0.3059406 ],
                                    [-0.26822435]])
        self.bias2_mat      = np.mat([[ 0.56179807],
                                    [ 0.22391806],
                                    [ 0.26978179],
                                    [-0.02163253],
                                    [ 0.28096522],
                                    [-0.09323822],
                                    [ 0.03068343],
                                    [-0.00414531]])
        '''

    '''predict the bird shoud do action or not'''
    def predict(self, input1,input2):
        self.input_mat[0,0]   = input1/288
        self.input_mat[1,0]   = input2/512

        #calculation
        step_1    = self.hidden1_mat * self.input_mat

        step_2    = step_1 + self.bias1_mat

        step_3    = self.hidden2_mat * step_2

        step_4    = step_3 + self.bias2_mat

        total = 0
        for i in range(self.hidden_num2):
            total = step_4[i,0]
        '''
        total = 0
        for i in range(self.hidden_num1):
            total = step_2[i,0]
        '''
        self.output = self.sigmoid_fun(total)


    #fly up if output is positive.
    def fly_up(self):
        #print(self.output)
        if self.output > 0.5:
            return True
        else:
            return False

    def sigmoid_fun(self, x):

        return 1 / (1 + np.exp(-x))
