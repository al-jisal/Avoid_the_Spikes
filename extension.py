'''
extension.py

Desmond Frimpong

This file describes the GUI of the game. It also sets the game up.

'''

# importing packages
import physics_objects as pho
import graphicsPlus as gr
import time
import random

# describes the start scene of the game
def startGame_scene(window):

    check = True

    startgame_object_list = [ ]

    startgame = gr.Text(gr.Point(250, 350), 'Press "Space" To Play Game')
    startgame.setSize(30)
    startgame.setFill('green')
    startgame.setFace('courier')
    startgame.draw(window)

    startgame_object_list.append(startgame)

    window.update()

    while check:

        key = window.getKey()

        if key == 'space':

            for objs in startgame_object_list:

                objs.undraw()

            window.update()

        check = False



# describes the game over scene
def gameOver_scene(window):

    gameover_object_list = []

    gameover = gr.Text(gr.Point(250, 350), 'Game Over')
    gameover.setSize(36)
    gameover.setFill('red')
    gameover.setFace('courier')
    gameover.draw(window)

    gameover_object_list.append(gameover)

    playAgain = gr.Text(gr.Point(250, 500), 'To Play Again Press "Space"')
    playAgain.setSize(24)
    playAgain.setFill('green1')
    playAgain.setFace('courier')
    playAgain.draw(window)

    gameover_object_list.append(playAgain)   

    exitTxt = gr.Text(gr.Point(250, 600), 'To Exit Press "q"')
    exitTxt.setSize(24)
    exitTxt.setFill('green1')
    exitTxt.setFace('courier')
    exitTxt.draw(window)

    window.update()

    gameover_object_list.append(exitTxt)

    while True:

        key = window.checkKey()

        if key == 'space':

            for objs in gameover_object_list:

                objs.undraw()

            window.close()

            main()

        if key == 'q' or key == 'Q':

            break
    

def main():


    # set gameOver to a false
    gameOver = False

    # create a window and sets its background color to black
    win = gr.GraphWin('Extension', 500, 700, False)
    win.setBackground('black')

    startGame_scene(win)

    # creates a list to hold the upward facing spikes
    spikeUpList = []

    # creates and fixes upward grey spikes on the floor of the window
    for i in range(10):

        spikeUp = pho.Spike(win, 'up')
        posX = (i+1)*5 - 2.5
        spikeUp.setPosition(posX, 0)
        spikeUp.fillColor('grey')
        spikeUp.draw()
        spikeUpList.append(spikeUp)

    # creates a list to hold the downward facing spikes
    spikeDownList = []

    # creates and fixes downward grey spikes on the ceiling of the window
    for i in range(10):

        spikeDown = pho.Spike(win, 'down')
        posX = (i+1)*5 - 2.5
        spikeDown.setPosition(posX, 70)
        spikeDown.fillColor('grey')
        spikeDown.draw()
        spikeDownList.append(spikeDown)

    # creates an empty list to hold the blocks to be created
    blockList = []

    # creates four white blocks moving upward
    for i in range(4):

        block = pho.Block(win, width= 15, height= 3)
        block.setPosition(random.randint(8, 43), i * 20)
        block.fillColor('white')
        block.setVelocity(0, 10)
        block.setAcceleration(0, 0.2)
        block.draw()

        blockList.append(block)

    dt = 0.033    # set the time frame to a suitable time 

    # creates a yellow falling centered ball 
    ball = pho.Ball(win, radius=1.5)
    ball.fillColor('yellow')
    ball.setAcceleration(0, -40)
    ball.setPosition(25, 50)
    ball.draw()

    win.update()

    while True:
        
        time.sleep(dt)  # slows down the iteration of the while loop

        for block in blockList:

            block.update(dt)
            pos_y_block = block.getPosition()[1]
            
            if pos_y_block > 70:
                # reset the position of the block when it goes out of the window

                block.setPosition(random.randint(8, 43), -10)
            
            if block.collision(ball):
                # keeps the ball on the block when they collide 

                posX = ball.getPosition()[0]
                posY = block.getPosition()[1]+0.5*block.getHeight()+ball.getRadius()

                ball.setPosition(posX, posY)
                ball.setVelocity(0, 0)

        ball.update(dt)

        key = win.checkKey()   # checks for any key input from the user

        if key == 'Left':
            # moves the ball to the left when the left arrow key is pressed

            ball.moveX(-3)

        if key == 'Right':
            # moves the ball to the right when the right arrow key is pressed

            ball.moveX(3)


        posX_ball = ball.getPosition()[0]

        if posX_ball < 1.5:
            # prevents the ball from going beyond the left border of the window
            
            pos_y = ball.getPosition()[1]
            ball.setPosition(1.5, pos_y)

        if posX_ball > 48.5:
            # prevents the ball from going beyond the right border of the window
            
            pos_y = ball.getPosition()[1]
            ball.setPosition(48.5, pos_y)


        # breaks the loop if there is a collision between the ball and the spikes
        for spikes in spikeUpList:

            if spikes.collision(ball):

                gameOver = True

        for spikes in spikeDownList:

            if spikes.collision(ball):

                gameOver = True

        if gameOver:

            break


        win.update()

    gameOver_scene(win)   # a call to the gameOver_scene
    
    win.close()


if __name__ == '__main__':

    main()


    



