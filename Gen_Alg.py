
import numpy as np
import random
import copy

class Gen_Alg:

    Num_birds   = 0

    parents     = 0
    child       = 0

    mutation_rate   = 0.05
    mutation_range  = 0.02


    #pick number of best birds as parents
    #Num_best_parents  = 3
    #solve the list problem
    #best_parents = [0 for i in range(Num_best_parents)]

    Num = 0

    #set up
    def __init__(self, Num_birds, parents_bird = []):
        self.Num_birds  = Num_birds
        self.parents    = parents_bird
        self.child      = [0 for i in range(Num_birds)]



    '''by matrix'''

    def new_generation(self):
        print('Next Generation')
        self.Fitness()
        for i in range(self.Num_birds):
            self.child[i]    =   copy.deepcopy(self.PickBird())

        '''
        for i in range(3):
            print(self.child[i].bias1_mat)
        '''





    def Fitness(self):
        sum     =   0.0001
        for i in range(Gen_Alg.Num_birds):
            sum     +=      self.parents[i].score

        for i in range(Gen_Alg.Num_birds):
            self.parents[i].fitness        =       self.parents[i].score   /   sum


        #self.parents[0].fitness = 1





    def PickBird(self):
        i = 0
        check_fit   =   False
        r = np.random.random(1)[0]

        while r > 0:
            r = r - self.parents[i].fitness
            i += 1
            if i >= self.Num_birds:
                check_fit   =   True
                break

        if check_fit:
            child = self.parents[random.randint(0, self.Num_birds-1)]
            self.mutate(child)
        else:
            i -= 1
            child = self.parents[i]
            self.mutate(child)

        #print(i)
        return child

    '''
    def mutate(self, child):

        #b X a matrix    hidden1_mat
        for i in range(8):
            if np.random.random(1)[0]   <   self.mutation_rate:
                num     =   random.uniform(-0.1, 0.1)
                for j in range (5):
                    child.hidden1_mat[i,j]  +=   num
        #c X b matrix    hidden2_mat
        for i in range(8):
            if np.random.random(1)[0]   <   self.mutation_rate:
                num     =   random.uniform(-0.1, 0.1)
                for j in range (8):
                    child.hidden2_mat[i,j]  +=   num
        #b X 1 matrix    bias1_mat

        if np.random.random(1)[0]   <   self.mutation_rate:
            num     =   random.uniform(-0.1, 0.1)
            for i in range(8):
                    child.bias1_mat[i,0]  +=   num
        #c X 1 matrix    bias2_mat
        if np.random.random(1)[0]   <   self.mutation_rate:
            num     =   random.uniform(-0.1, 0.1)
            for i in range(8):
                child.bias2_mat[i,0]  +=   num
    '''


    def mutate(self, child):

        for i in range(8):
            for j in range (2):
                if np.random.random(1)[0]   <   self.mutation_rate:
                    child.hidden1_mat[i,j]  +=   random.uniform(-self.mutation_range, self.mutation_range)

        for i in range(8):
            for j in range (8):
                if np.random.random(1)[0]   <   self.mutation_rate:
                    child.hidden2_mat[i,j]  +=   random.uniform(-self.mutation_range, self.mutation_range)

        for i in range(8):
            for j in range (1):
                if np.random.random(1)[0]   <   self.mutation_rate:
                    child.bias1_mat[i,j]  +=   random.uniform(-self.mutation_range, self.mutation_range)

        for i in range(8):
            for j in range (1):
                if np.random.random(1)[0]   <   self.mutation_rate:
                    child.bias2_mat[i,j]  +=   random.uniform(-self.mutation_range, self.mutation_range)
