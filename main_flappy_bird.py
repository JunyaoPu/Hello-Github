from itertools import cycle
import random
import sys
import pygame
from pygame.locals import *


import copy
from Bird import *
from Gen_Alg import *
'''note
    #playerVelY    #playerFlapAcc   are changed to -4 for more stable one
'''

#number of birds
Num_birds = 5
last_generation = [0 for i in range(Num_birds)]
Num_generation  = 0

#show the best bird
SHOW_BEST_BIRD  = True

#set up the screen
FPS = 30*4
SCREENWIDTH  = 288
SCREENHEIGHT = 512
# gap between upper and lower part of pipe
PIPEGAPSIZE = 100           #100*1.2
#the location of the ground
BASEY       = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

#on ubuntu
address_assets = '/home/junyao/Documents/Neural_Network/Flappy_Bird/Flappy_Bird/assets/sprites/'

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        address_assets +'redbird-upflap.png',
        address_assets +'redbird-midflap.png',
        address_assets +'redbird-downflap.png',
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        address_assets +'bluebird-upflap.png',
        address_assets +'bluebird-midflap.png',
        address_assets +'bluebird-downflap.png',
    ),
    # yellow bird
    (
        address_assets +'yellowbird-upflap.png',
        address_assets +'yellowbird-midflap.png',
        address_assets +'yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    address_assets +'background-day.png',
    address_assets +'background-night.png',
)

# list of pipes
PIPES_LIST = (
    address_assets +'pipe-green.png',
    address_assets +'pipe-red.png',
)

try:
    xrange
except NameError:
    xrange = range


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    #set the pygame mode
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    #give a name to the title
    pygame.display.set_caption('Flappy Bird-CUDA_RUNNER')
    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load(address_assets +'0.png').convert_alpha(),
        pygame.image.load(address_assets +'1.png').convert_alpha(),
        pygame.image.load(address_assets +'2.png').convert_alpha(),
        pygame.image.load(address_assets +'3.png').convert_alpha(),
        pygame.image.load(address_assets +'4.png').convert_alpha(),
        pygame.image.load(address_assets +'5.png').convert_alpha(),
        pygame.image.load(address_assets +'6.png').convert_alpha(),
        pygame.image.load(address_assets +'7.png').convert_alpha(),
        pygame.image.load(address_assets +'8.png').convert_alpha(),
        pygame.image.load(address_assets +'9.png').convert_alpha()
    )
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load(address_assets +'message.png').convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load(address_assets +'base.png').convert_alpha()
    #import dot image to track points
    IMAGES['dot'] = pygame.image.load(address_assets +'dot.png').convert_alpha()
    IMAGES['bird_dot'] = pygame.image.load(address_assets +'bird_dot.png').convert_alpha()

    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        # select random pipe sprites
        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.rotate(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), 180),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )
        # select random player sprites
        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )
        # hismask for pipes
        HITMASKS['pipe'] = (
            #up pipe
            getHitmask(IMAGES['pipe'][0]),
            #down pipe
            getHitmask(IMAGES['pipe'][1]),
        )
        # hitmask for player
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )
        #show the wecomescreen
        movementInfo = showWelcomeAnimation()
        #this is the main body of the game
        mainGame(movementInfo)

def showWelcomeAnimation():
    global Num_generation
    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)
    basex = 10
    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    if Num_generation == 0:
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                        return {
                            'basex': basex,
                        }

                # adjust playery, playerIndex, basex
                basex = -((-basex + 4) % baseShift)
                # draw sprites
                SCREEN.blit(IMAGES['background'], (0,0))
                SCREEN.blit(IMAGES['message'], (messagex, messagey))
                SCREEN.blit(IMAGES['base'], (basex, BASEY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

    else:
        while True:
            # adjust playery, playerIndex, basex
            basex = -((-basex + 4) % baseShift)
            # draw sprites
            SCREEN.blit(IMAGES['background'], (0,0))
            SCREEN.blit(IMAGES['message'], (messagex, messagey))
            SCREEN.blit(IMAGES['base'], (basex, BASEY))
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            return{'basex': basex,}



def mainGame(movementInfo):
    global last_generation
    global Num_generation
    global  Num_birds
    print('Generation:' + str(Num_generation))

    birds = [0 for i in range(Num_birds)]
    crashTest = []
    crashTest_false = [False,False]

    if Num_generation != 0:
        '''Genetic Algorithm'''
        '''Genetic Algorithm'''
        '''Genetic Algorithm'''
        '''Genetic Algorithm'''
        GA      = Gen_Alg(Num_birds,last_generation)
        GA.new_generation()
        for i in range(Num_birds):
            birds[i]                = copy.deepcopy(BIRD())
            crashTest.append(crashTest_false)
            birds[i].hidden1_mat    =   GA.child[i].hidden1_mat
            birds[i].hidden2_mat    =   GA.child[i].hidden2_mat
            birds[i].bias1_mat      =   GA.child[i].bias1_mat
            birds[i].bias2_mat      =   GA.child[i].bias2_mat
    else:
        for i in range(Num_birds):
            birds[i] = copy.deepcopy(BIRD())
            crashTest.append(crashTest_false)
            birds[i].set_up()

    #move the base
    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    #initial the score
    score = 0

    # initialize 2 pipe
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH - 100, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH - 100 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    lowerPipes = [
        {'x': SCREENWIDTH - 100, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH - 100 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    #pipe velocity
    pipeVelX = -4
    # player velocity, max velocity, downward accleration, accleration on flap
    #playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
    #playerFlapAcc =  -9   # players speed on flapping
    playerVelY    =  -8   # player's velocity along Y, default same as playerFlapped
    playerFlapAcc =  -8   # players speed on flapping

    playerMaxVelY =  10   # max vel along Y, max descend speed
    playerMinVelY =  -8   # min vel along Y, max ascend speed
    playerAccY    =   1   # players downward accleration
    playerRot     =  45   # player's rotation
    playerVelRot  =   3   # angular speed
    playerRotThr  =  20   # rotation threshold
    playerFlapped = False # True when player flaps


    #initialize the bird velocity
    for i in range(Num_birds):
        birds[i].birdVelY = playerVelY

    closest_pip_x = upperPipes[0]['x']
    closest_pip_y = lowerPipes[0]['y']

    '''For showing the best bird'''
    if SHOW_BEST_BIRD:
        Num_birds   =   2
        birds = [0 for i in range(Num_birds)]
        crashTest = []
        crashTest_false = [False,False]

        for i in range(Num_birds):
            birds[i] = copy.deepcopy(BEST_BIRD())
            crashTest.append(crashTest_false)

    while True:
        for event in pygame.event.get():
            #close the program by user
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):

                '''save the best bird'''
                best_bird = birds[0].score
                j         = 0
                for i in range(Num_birds):
                    if best_bird    <   birds[i].score:
                        best_bird   =   birds[i].score
                        j           =   i

                save_bird(birds[j])


                pygame.quit()
                sys.exit()

            '''
            #act by keyboard
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                for i in range(Num_birds):
                    if birds[i].y > -2 * IMAGES['player'][0].get_height():
                        birds[i].birdVelY = playerFlapAcc
                        birds[i].birdFlapped =True
            '''

        #this is the brain of the birds
        for i in range(Num_birds):
            if birds[i].fly_up():
                if birds[i].y > -2 * IMAGES['player'][0].get_height():
                    birds[i].birdVelY = playerFlapAcc
                    birds[i].birdFlapped =True




        #Check bird crash
        for i in range(Num_birds):
            if not crashTest[i][0]:
                crashTest[i] = checkCrash({'x': birds[i].x, 'y': birds[i].y, 'index': 0},
                                        upperPipes, lowerPipes)

        #End the program until the last bird collision
        End_program = 0
        for i in range(Num_birds):
            if crashTest[i][0]:
                End_program = True

            else:
                End_program = False
                break
        #print the distance of the birds and end the program
        if End_program:
            last_generation = copy.deepcopy(birds)
            Num_generation  += 1
            return{}


        #update the distance bird fly
        for i in range(Num_birds):
            if not crashTest[i][0]:
                birds[i].distance += abs(pipeVelX)

        #The mid point of the bird x
        for i in range(Num_birds):
            birds[i].xMidpos = birds[i].x + IMAGES['player'][0].get_width() / 2

        #the mid point of the pipe x
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            #check each bird and award points, locate the closest pipe position
            for i in range(Num_birds):
                if pipeMidPos <= birds[i].xMidpos < pipeMidPos + 4:
                    #birds[i].score += 1
                    closest_pip_x = upperPipes[1]['x']
                    closest_pip_y = lowerPipes[1]['y']

        #check all birds and print the highest score on the screen
        for i in range(Num_birds):

            '''this score addition is wrong'''
            if birds[i].x > closest_pip_x:
                birds[i].score = copy.deepcopy(birds[i].score+1)


            if birds[i].score > score:
                score = copy.deepcopy(birds[i].score)


        # playerIndex basex change
        basex = -((-basex + 100) % baseShift)
        # rotate the player
        if playerRot > -90:
            playerRot -= playerVelRot

        # player's movement
        for i in range (Num_birds):
            if birds[i].birdVelY < playerMaxVelY and not birds[i].birdFlapped:
                birds[i].birdVelY += playerAccY

        for i in range(Num_birds):
            if birds[i].birdFlapped:
                birds[i].birdFlapped = False
                playerRot = 45

        #fly up
        playerHeight = IMAGES['player'][0].get_height()
        for i in range(Num_birds):
            if not crashTest[i][0]:
                #move along y axis if the bird still alive
                birds[i].y += min(birds[i].birdVelY, BASEY - birds[i].y - playerHeight)
            else:
                #move the bird out of the screen if the bird is dead
                birds[i].x += pipeVelX


        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        #tracking the closest pipe x position
        closest_pip_x += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
            closest_pip_x = upperPipes[0]['x']
            closest_pip_y = lowerPipes[0]['y']

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))
            #draw the center point for all pipes
            SCREEN.blit(IMAGES['dot'], (lPipe['x']+20, lPipe['y']-(PIPEGAPSIZE/2)))

        #draw the closest pipe only
        SCREEN.blit(IMAGES['bird_dot'], (closest_pip_x+20,closest_pip_y-(PIPEGAPSIZE/2)))


        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        # print score so player overlaps the score
        showScore(score)
        # Player rotation has a threshold
        visibleRot = playerRotThr
        if playerRot <= playerRotThr:
            visibleRot = playerRot

        playerSurface = pygame.transform.rotate(IMAGES['player'][0], visibleRot)

        #draw all birds
        for i in range(Num_birds):
            SCREEN.blit(pygame.transform.rotate(IMAGES['player'][0], visibleRot),
                        (birds[i].x, birds[i].y))
            #draw the dot on the birds
            SCREEN.blit(IMAGES['bird_dot'], (birds[i].x+12,birds[i].y+12))


        '''here to do the prediction!!!'''
        '''here to do the prediction!!!'''
        '''here to do the prediction!!!'''

        for i in range(Num_birds):
            #birds[i].set_up()
            birds[i].predict((closest_pip_x+20)-(birds[i].x+12) , (birds[i].y+12)-(closest_pip_y-(PIPEGAPSIZE/2)))

        #print(str(birds[0].hidden1_mat) + 'and' + str(birds[2].hidden1_mat) )
        #print(str(birds[0].hidden1_mat) + 'and' + str(birds[8].hidden1_mat) )

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)

    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]
def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()

def checkCrash(player, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False
def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask




def save_bird(bird):

    fileObject = open('/home/junyao/Documents/Neural_Network/Flappy_Bird/Flappy_Bird/Best_bird.txt', 'w')
    fileObject.write('The score of this birds is: ' + str(bird.score))
    fileObject.write('\n')
    fileObject.write('\n')
    fileObject.write('The first hidden layer:')
    fileObject.write('\n')
    fileObject.write(str(bird.hidden1_mat))
    fileObject.write('\n')
    fileObject.write('\n')
    fileObject.write('The second hidden layer:')
    fileObject.write('\n')
    fileObject.write(str(bird.hidden2_mat))
    fileObject.write('\n')
    fileObject.write('\n')
    fileObject.write('The first bias:')
    fileObject.write('\n')
    fileObject.write(str(bird.bias1_mat))
    fileObject.write('\n')
    fileObject.write('\n')
    fileObject.write('The second bias:')
    fileObject.write('\n')
    fileObject.write(str(bird.bias2_mat))



if __name__ == '__main__':
    main()
