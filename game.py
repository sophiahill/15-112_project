from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import random
import math

score = 0
restartCount = 0
spritesMade = False
coinScreenShown = False

# ModalApp structure from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#subclassingModalApp
class LoadingScreen(Mode):
    def appStarted(mode):
        mode.turn = True
        mode.counter = 0
        mode.image0 = mode.loadImage('screen frame 1.jpg')

    def timerFired(mode):
        mode.counter += 1
        if mode.counter % 10 == 0:
            mode.load()
        if mode.counter == 100:
            mode.app.setActiveMode(mode.app.introduction)

    def keyPressed(mode, event):
        if event.key == 'Right':
            mode.app.setActiveMode(mode.app.introduction)
        elif event.key == 'w':
            mode.app.setActiveMode(mode.app.winMode)
        elif event.key == 'l':
            mode.app.setActiveMode(mode.app.loseMode)
        elif event.key == 'm':
            mode.app.setActiveMode(mode.app.mazeMode)

    def load(mode):
        mode.turn = not mode.turn
        if mode.turn == True:
            mode.image0 = mode.loadImage('screen frame 1.jpg')
        else:
            mode.image0 = mode.loadImage('screen frame 2.jpg')

    def redrawAll(mode, canvas):
        canvas.create_image(300, 300, image=ImageTk.PhotoImage(mode.image0))

class Introduction(Mode):
    def appStarted(mode):
        mode.counter = 0
        mode.image = mode.scaleImage(mode.loadImage('112TA.jpg'), .7)
        mode.image1 = mode.scaleImage(mode.loadImage('dia1.jpg'), .75)
        mode.image2 = mode.scaleImage(mode.loadImage('dia2.jpg'), .75)
        mode.dialogue = [mode.image1, mode.image2]

    def keyPressed(mode, event):
        if (event.key == 'Right'):
            mode.counter += 1

        if (event.key == 'Left'):
            mode.counter -= 1
            if mode.counter < 0:
                mode.counter += 1
        
        if mode.counter == len(mode.dialogue):
            mode.app.setActiveMode(mode.app.sideScrollerMode)

    def redrawAll(mode, canvas):
        if mode.counter == 0:
            canvas.create_text(150, mode.height - 20, 
                                text= 'Press the right arrow key to advance.', font = 'Helvetica 10')

        canvas.create_image(200, 175, image=ImageTk.PhotoImage(mode.dialogue[mode.counter]))
        canvas.create_image(425, 475, image=ImageTk.PhotoImage(mode.image))

# modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#sidescrollerExamples
# spritestrip format from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#spritesheetsWithCropping
class SideScrollerMode(Mode):
    # initialize buildings and characters
    def appStarted(mode):
        mode.scrollMargin = 50
        mode.scrollX = 0
        mode.player = [200, 528]
        mode.door = [mode.width*2.1, mode.height - 120, mode.width*2.1 + 75, mode.height - 20]
        mode.step = 10
        mode.gates = [800, 375]
        mode.image1 = mode.loadImage('GatesPoptropica.jpg')
        mode.cloudCenter = [200, 150]
        spritestrip = mode.loadImage('sprite sheet.png')
        spritestripback = mode.loadImage('sprite sheet back.png')
        mode.forward = None
        # make player / sprite
        mode.sprites = []
        for i in range(1,6):
            sprite = spritestrip.crop((200*i, 0, 200+200*i, 300))
            mode.sprites.append(sprite)
        mode.spriteCounter = 0
        mode.spritesback = []
        for i in range(1,6):
            sprite = spritestripback.crop((200*i, 0, 200+200*i, 300))
            mode.spritesback.append(sprite)
        mode.spriteCounterBack = 0

    # from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#sidescrollerExamples
    def makePlayerVisible(mode):
        # scroll to make player visible as needed
        if (mode.player[0] < mode.scrollX + mode.scrollMargin):
            mode.scrollX = mode.player[0] - mode.scrollMargin
        if (mode.player[0] > mode.scrollX + mode.width - mode.scrollMargin):
            mode.scrollX = mode.player[0] - mode.width + mode.scrollMargin

    # from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#sidescrollerExamples
    def movePlayer(mode, dx, dy):
        mode.player[0] += dx
        mode.makePlayerVisible()

    def keyPressed(mode, event):
        if (event.key == "Left"): 
            mode.movePlayer(-mode.step, 0)
            mode.spriteCounterBack = (1 + mode.spriteCounterBack) % len(mode.spritesback)
            mode.forward = False

        elif (event.key == "Right"): 
            mode.movePlayer(mode.step, 0)
            mode.spriteCounter = (1 + mode.spriteCounter) % len(mode.sprites)
            mode.forward = True

        if mode.inDoor():
            mode.app.setActiveMode(mode.app.mazeMode)

    def inDoor(mode):
        if (mode.player[0] - mode.width*1.5 >= mode.doorX0 and mode.player[0] - mode.width*1.5 <= mode.doorX1):
            mode.app.setActiveMode(mode.app.mazeMode)

    def redrawAll(mode, canvas):
        # draw sky
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'DeepSkyBlue3')

        # draw Gates
        mode.gates[0] -= mode.scrollX
        canvas.create_image(mode.gates[0], mode.gates[1], image=ImageTk.PhotoImage(mode.image1))
        mode.gates[0] += mode.scrollX

        # draw player
        if mode.forward == True or mode.forward == None:
            sprite = mode.sprites[mode.spriteCounter]
            sprite = mode.scaleImage(sprite, .4)
            mode.player[0] -= mode.scrollX
            canvas.create_image(mode.player[0], mode.player[1], image=ImageTk.PhotoImage(sprite))
            mode.player[0] += mode.scrollX

        elif mode.forward == False:
            sprite = mode.spritesback[mode.spriteCounterBack]
            sprite = mode.scaleImage(sprite, .4)
            mode.player[0] -= mode.scrollX
            canvas.create_image(mode.player[0], mode.player[1], image=ImageTk.PhotoImage(sprite))
            mode.player[0] += mode.scrollX

        # draw door with shift
        topLeftX, topLeftY, botRightX, botRightY = mode.door
        topLeftX -= mode.scrollX
        botRightX -= mode.scrollX
        canvas.create_rectangle(topLeftX, topLeftY, botRightX, botRightY)

        # draw ground
        canvas.create_rectangle(0, mode.height - 20, mode.width, mode.height, fill = 'black')

        # store current values to check if player is within door
        mode.doorX0 = topLeftX
        mode.doorX1 = botRightX

# from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#genericBacktrackingSolver
class BacktrackingPuzzleSolver(object):
    def __init__(self, maze):
        # initialize state.maze
        self.startState = maze
        self.moves = [(0,0)]

    def solve(self):
        self.states = set()
        self.solutionState = self.solveFromState(MazeState(self.startState), self.moves)
        return (self.solutionState, self.moves)

    def solveFromState(self, state, moves):
        if moves[-1] in self.states:
            return None
        self.states.add(moves[-1])
        if self.isSolutionState(moves):
            return True
        else:
            for move in self.getLegalMoves(state):
                childState = self.doMove(state, move)
                if self.stateSatisfiesConstraints(childState):
                    self.moves.append(move)
                    result = self.solveFromState(state, moves)
                    if result != None:
                        return result
                    else:
                        self.moves.pop()
            return None

    # returns a list of the moves for enemy to follow
    def retMoves(self):
        return self.moves

# from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#whatIsBacktracking
class State(object):
    def __eq__(self, other): return (other != None) and self.__dict__ == other.__dict__
    def __hash__(self): return hash(str(self.__dict__))
    def __repr__(self): return str(self.__dict__)

# MazeState class
# from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#whatIsBacktracking
class MazeState(State):
    def __init__(self, maze):
        self.maze = maze

# mazeSolver class
# from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#whatIsBacktracking
class MazeSolver(BacktrackingPuzzleSolver):
    # returns a list of all the positions around a position that are in the maze
    def getLegalMoves(self, state):
        legalMoves = []
        (curRow, curCol) = self.moves[-1]
        for drow in [-1,0,1]:
            for dcol in [-1,0,1]:
                if abs(drow) == 1 and abs(dcol) == 1:
                    continue
                newRow = curRow + drow
                newCol = curCol + dcol
                # check in bounds of maze
                if (self.notInBounds(state, newRow, newCol) or 
                    (curCol == newCol and curRow == newRow)):
                    continue
                legalMoves.append((newRow, newCol))
        return legalMoves

    # checks if newRow, newCol is within the maze
    def notInBounds(self, state, row, col):
        if row < 0 or row >= len(self.startState) or col < 0 or col >= len(self.startState): 
            return True
        return False

    def doMove(self, state, move):
        newMoves = copy.deepcopy(self.moves)
        newMoves.append(move)
        return newMoves
        
    # solution state if last move is the bottom right row, col
    def isSolutionState(self, moves):
        if len(moves) == 0: 
            return False
        (row, col) = moves[-1]
        if row == len(self.startState)-1 and col == len(self.startState)-1:
            return True
        return False

    # if the element of the last move in board is 0
    def stateSatisfiesConstraints(self, state):
        if self.startState[self.moves[-1][0]][self.moves[-1][1]] == 0:
            return True
        return False

class MazeMode(Mode):
    def appStarted(mode, restarted = False):
        global spritesMade
        if (restarted == False):
            mode.rows = 10
            mode.cols = 10
            mode.mazeCounter = 1
        else:
            mode.rows += 5
            mode.cols += 5
            mode.mazeCounter += 1

        mode.transportSpotsMade = False
        mode.mazeMade = False
        mode.drawBacktrackingPath = False
        mode.timerDelay = 100
        mode.spotR = (mode.width / mode.rows) // 2
        mode.r = mode.spotR - 5
        mode.font = 'Helvetica 20'
        mode.counter = 0
        mode.step = 10
        mode.playerPosition = [mode.r, mode.r]
        mode.enemyPosition = [0,0]
        mode.transportSpots = []
        mode.enemyMoves = [(0,0)]
        # intialize maze as a 2d list of 0s
        mode.maze = [[0 for j in range(mode.cols)] for i in range(mode.rows)]
        # make sprites
        if spritesMade == False:
            # make player
            spritestrip = mode.loadImage('sprite sheet.png')
            spritestripback = mode.loadImage('sprite sheet back.png')
            mode.forward = None
            mode.sprites = []
            for i in range(1,6):
                sprite = spritestrip.crop((200*i, 0, 200+200*i, 300))
                mode.sprites.append(sprite)
            mode.spriteCounter = 0
            mode.spritesback = []
            for i in range(1,6):
                sprite = spritestripback.crop((200*i, 0, 200+200*i, 300))
                mode.spritesback.append(sprite)
            mode.spriteCounterBack = 0
            spritesMade = True
            # make enemy
            # enemy image from http://tnedreport.com/wp-content/uploads/2018/03/Grade-F.jpg
            mode.enemyImage = mode.scaleImage(mode.loadImage('enemy.png'), .4 / mode.rows)

    # move player
    def keyPressed(mode, event):
        global coinScreenShown
        if event.key == 'Left':
            mode.playerPosition[0] -= mode.step
            mode.spriteCounterBack = (1 + mode.spriteCounterBack) % len(mode.spritesback)
            mode.forward = False
            if mode.checkCollisions(mode.playerPosition):
                mode.playerPosition[0] += mode.step
        elif event.key == 'Right':
            mode.playerPosition[0] += mode.step
            mode.spriteCounter = (1 + mode.spriteCounter) % len(mode.sprites)
            mode.forward = True
            if mode.checkCollisions(mode.playerPosition):
                mode.playerPosition[0] -= mode.step
        elif event.key == 'Up':
            mode.playerPosition[1] -= mode.step
            if mode.checkCollisions(mode.playerPosition):
                mode.playerPosition[1] += mode.step
        elif event.key == 'Down':
            mode.playerPosition[1] += mode.step
            if mode.checkCollisions(mode.playerPosition):
                mode.playerPosition[1] -= mode.step
        elif (event.key == 'h'):
            mode.app.setActiveMode(mode.app.helpMode)
        elif (event.key == 'b'):
            mode.drawBacktrackingPath = not mode.drawBacktrackingPath

        # if in a transport spot, transport the user to a submaze
        for spot in mode.transportSpots:
            if (mode.playerPosition[0] > spot[0]  and
                mode.playerPosition[0] + mode.r < spot[2] and 
                mode.playerPosition[1] > spot[1] and 
                mode.playerPosition[1] + mode.r < spot[3]):
                # turn transport spot into a white spot
                mode.transportSpots.remove(spot)
                (row, col) = mode.getCell(spot[0],spot[1])
                mode.maze[row][col] = 0
                # generate a new sub maze
                mode.app.subMazeMode.restartSubMaze()
                if coinScreenShown == False:
                    mode.app.setActiveMode(mode.app.coinScreen)
                else:
                    mode.app.setActiveMode(mode.app.subMazeMode)

        # if in endPosition, make new harder maze
        (endX0, endY0, endX1, endY1) = mode.getCellBounds(mode.rows-1, mode.cols-1)
        if (mode.playerPosition[0] > endX0 and mode.playerPosition[0] + mode.r < endX1 and
            mode.playerPosition[1] > endY0 and mode.playerPosition[1] + mode.r < endY1):
            if mode.mazeCounter == 3:
                mode.app.setActiveMode(mode.app.winMode)
            mode.resetMaze()

    # reset maze when the player completes 3 main mazes (levels)
    def resetMaze(mode):
        mode.appStarted(restarted = True)

    # restart game when player loses
    def restartGame(mode):
        mode.appStarted(restarted = False)

    # randomly generate transport spots
    def makeTransportSpots(mode):
        for row in range(mode.rows):
            for col in range(mode.cols):
                # if block is black
                if mode.maze[row][col] == 1:
                    choice = random.randint(0, 20)
                    if (choice == 0 or choice == 20):
                        (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                        mode.transportSpots.append((x0, y0, x1, y1))
        mode.transportSpotsMade = True   

    def checkCollisions(mode, playerPosition):
        # check player collision with canvas walls
        if (playerPosition[0] - mode.r*.5 < 0 or playerPosition[0] + mode.r > mode.width or
            playerPosition[1] - mode.r*.7 < 0 or playerPosition[1] + mode.r > mode.height):
            return True

        # check player collision with maze
        (playerRow, playerCol) = mode.getCell(mode.playerPosition[0], mode.playerPosition[1])
        (playerRowTwo, playerColTwo) = mode.getCell(mode.playerPosition[0] + (mode.r*.8), mode.playerPosition[1] + (mode.r*.8))
        (playerRowThree, playerColThree) = mode.getCell(mode.playerPosition[0] + (mode.r*.8), mode.playerPosition[1])
        (playerRowFour, playerColFour) = mode.getCell(mode.playerPosition[0], mode.playerPosition[1] + (mode.r*.8))
        for row in range(mode.rows):
            for col in range(mode.cols):
                if mode.maze[row][col] == 1:
                    # if player hits a transport spot, return False (player can go into transport spot)
                    for spot in mode.transportSpots:
                        (spotRow, spotCol) = mode.getCell(spot[0], spot[1])
                        if ((playerRow == spotRow and playerCol == spotCol) or (playerRowTwo == spotRow and playerColTwo == spotCol)
                            or (playerRowThree == spotRow and playerColThree == spotCol) or (playerRowFour == spotRow and playerColFour == spotCol)):
                            return False
                    if ((playerRow == row and playerCol == col) or (playerRowTwo == row and playerColTwo == col)
                        or (playerRowThree == row and playerColThree == col) or (playerRowFour == row and playerColFour == col)):
                        return True
        return False

    def intersects(mode):
        # check player collision with enemy
        playerCX = mode.playerPosition[0] + (mode.r/2)
        playerCY = mode.playerPosition[1] + (mode.r/2)
        
        (row, col) = mode.enemyPosition
        if row == 0 and col == 0:
            return False
        (x0, y0, x1, y1) = mode.getCellBounds(row, col)
        enemyCX = x0 + (.75 * mode.r) + (mode.r/2)
        enemyCY = y0 + (.75 * mode.r) + (mode.r/2)

        centersDist = math.sqrt((enemyCY - playerCY)**2 + (enemyCX - playerCX)**2)
        if (centersDist <= mode.r):
            return True
        return False

    def timerFired(mode):
        global score
        if (mode.intersects()):
            mode.app.setActiveMode(mode.app.loseMode)

        if mode.timerDelay % 500 == 0:
            mode.moveEnemy()

    def moveEnemy(mode):
        mode.counter += 1
        mode.enemyPosition = mode.enemyMoves[mode.counter]
        # if at end, then enemy restarts
        if mode.enemyMoves[mode.counter] == (mode.rows - 1, mode.cols - 1):
            mode.counter = 0

    # make a random maze of 1s and 0s (1 = wall, 0 = empty)
    def makeMaze(mode, maze):
        for row in range(mode.rows):
            for col in range(mode.cols):
                maze[row][col] = random.randint(0,1)
        maze[0][0] = 0
        maze[len(maze)-1][len(maze)-1] = 0
        return maze

    # modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCellBounds(mode, row, col):
        rowHeight = mode.height / mode.rows
        columnWidth = mode.width / mode.cols
        x0 = col * columnWidth
        x1 = (col+1) * columnWidth
        y0 = row * rowHeight
        y1 = (row+1) * rowHeight
        return (x0, y0, x1, y1)

    # modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCell(mode, x, y):
        cellWidth  = mode.width / mode.cols
        cellHeight = mode.height / mode.rows
        row = int(y / cellHeight)
        col = int(x / cellWidth)
        return (row, col)

    def redrawAll(mode, canvas):
        mode.timerDelay += 100
        global score 
        # draw the maze with black squares as walls, white squares as empty cells,
        # and green squares as the start and end positions
        if mode.mazeMade == False:
            mode.maze = mode.makeMaze(mode.maze)
            while (MazeSolver(mode.maze).solve()[0] != True): 
                mode.maze = mode.makeMaze(mode.maze)
                mode.enemyMoves = MazeSolver(mode.maze).solve()[1]
            mode.mazeMade = True
        for row in range(mode.rows):
            for col in range(mode.cols):
                if mode.maze[row][col] == 1:
                    outline = 'black'
                    fill = 'black'
                elif mode.maze[row][col] == 0:
                    outline = 'white'
                    fill = 'white'
                if ((row == 0 and col == 0) or (row == mode.rows - 1 and col == mode.cols - 1)):
                    outline = 'green'
                    fill = 'green'
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill = fill, outline = outline)

        if mode.drawBacktrackingPath == True:
            for move in mode.enemyMoves:
                # each move is a tuple with board position
                (row, col) = move
                if (row == mode.rows - 1 and col == mode.cols - 1) or (row == 0 and col == 0):
                    continue
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill = 'RosyBrown1', outline = 'RosyBrown1')

        # draw spots that transport to submazes
        if mode.transportSpotsMade == False:
            mode.makeTransportSpots()
        for spot in mode.transportSpots:
            canvas.create_rectangle(spot[0],spot[1], spot[2], spot[3], fill = 'cyan')
            canvas.create_rectangle(spot[0]+(mode.spotR//2),spot[1]+(mode.spotR//2),
                                    spot[2]-(mode.spotR//2),spot[3]-(mode.spotR//2), fill = 'hot pink')
    
        # draw player
        if mode.forward == True or mode.forward == None:
            sprite = mode.sprites[mode.spriteCounter]
            sprite = mode.scaleImage(sprite, 2 / mode.rows)
            canvas.create_image(mode.playerPosition[0], mode.playerPosition[1], image=ImageTk.PhotoImage(sprite))

        elif mode.forward == False:
            sprite = mode.spritesback[mode.spriteCounterBack]
            sprite = mode.scaleImage(sprite, 2 / mode.rows)
            canvas.create_image(mode.playerPosition[0], mode.playerPosition[1], image=ImageTk.PhotoImage(sprite))

        # draw enemy
        (row, col) = mode.enemyPosition
        (x0, y0, x1, y1) = mode.getCellBounds(row, col)
        canvas.create_image(x0 + (1.25*mode.r), y0 + (1.5*mode.r), image=ImageTk.PhotoImage(mode.enemyImage))

        # draw score and level (mazeCounter)
        canvas.create_text(mode.width/2, 20, text=f'Level {mode.mazeCounter}', font=mode.font, fill = 'red')
        canvas.create_text(mode.width/2, 50, text=f'Score: {score}', font=mode.font, fill = 'red')

# inherits from MazeMode
class SubMazeMode(MazeMode):
    def appStarted(mode):
        global score
        super().appStarted()
        mode.coinsMade = False
        mode.rowEnemiesGo = True
        mode.colEnemiesGo = False
        mode.fill = None
        mode.coinsList = []
        mode.enemyRows = []
        mode.enemyCols = []
        mode.rowEnemies = []
        mode.colEnemies = []
        mode.rowEnemyPositions = []
        mode.colEnemyPositions = []
        mode.counter = -1
        mode.fillCounter = 0
        mode.timerDelay = 100
        mode.r = ((mode.width / mode.rows) // 2) - 5
        mode.makeEnemyPaths()

    # if player reaches endPosition, go back to maze mode
    # if player collides with coin, add 10 to the score
    def keyPressed(mode, event):
        global score
        if event.key == 'Left':
            mode.playerPosition[0] -= mode.step
            if mode.checkCollisions(mode.playerPosition):
                mode.playerPosition[0] += mode.step
        elif event.key == 'Right':
            mode.playerPosition[0] += mode.step
            if mode.checkCollisions(mode.playerPosition):
                mode.playerPosition[0] -= mode.step
        elif event.key == 'Up':
            mode.playerPosition[1] -= mode.step
            if mode.checkCollisions(mode.playerPosition):
                mode.playerPosition[1] += mode.step
        elif event.key == 'Down':
            mode.playerPosition[1] += mode.step
            if mode.checkCollisions(mode.playerPosition):
                mode.playerPosition[1] -= mode.step
        elif (event.key == 'h'):
            mode.app.setActiveMode(mode.app.helpMode)
        elif (event.key == 'b'):
            mode.drawBacktrackingPath = not mode.drawBacktrackingPath

        for coin in mode.coinsList:
            if mode.coinInPlayer(coin):
                mode.coinsList.remove(coin)
                score += 10

        (endX0, endY0, endX1, endY1) = mode.getCellBounds(mode.rows-1, mode.cols-1)
        if (mode.playerPosition[0] > endX0 and mode.playerPosition[0] + mode.r < endX1 and
            mode.playerPosition[1] > endY0 and mode.playerPosition[1] + mode.r < endY1):
            mode.app.setActiveMode(mode.app.mazeMode)

    def restartSubMaze(mode):
        mode.appStarted()

    # check if player collides with coin
    def coinInPlayer(mode, coin):
        (x0,y0,x1,y1) = coin
        coinX = (x1 + x0) // 2
        coinY = (y1 + y0) // 2
        # top left coordinates
        (xP, yP) = mode.playerPosition
        if ((xP < coinX < xP + mode.r) and (yP < coinY < yP + mode.r)):
            return True
        return False

    # randomly generate coins in empty squares
    def makeCoins(mode):
        for row in range(mode.rows):
            for col in range(mode.cols):
                # if block is white
                if mode.maze[row][col] == 0:
                    choice = random.randint(0,5)
                    if (choice == 0 or choice == 5):
                        (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                        mode.coinsList.append((x0, y0, x1, y1))
        mode.coinsMade = True

    def intersects(mode):
        # check player collision with enemies
        playerCX = mode.playerPosition[0] + (mode.r/2)
        playerCY = mode.playerPosition[1] + (mode.r/2)
        
        for enemy in mode.rowEnemyPositions:
            (row, col) = enemy
            (x0, y0, x1, y1) = mode.getCellBounds(row, col)
            enemyCX = x0 + (.75 * mode.r) + (mode.r/2)
            enemyCY = y0 + (.75 * mode.r) + (mode.r/2)
            centersDist = math.sqrt((enemyCY - playerCY)**2 + (enemyCX - playerCX)**2)
            if (centersDist <= mode.r):
                return True
        for enemy in mode.colEnemyPositions:
            (row, col) = enemy
            (x0, y0, x1, y1) = mode.getCellBounds(row, col)
            enemyCX = x0 + (.75 * mode.r) + (mode.r/2)
            enemyCY = y0 + (.75 * mode.r) + (mode.r/2)
            centersDist = math.sqrt((enemyCY - playerCY)**2 + (enemyCX - playerCX)**2)
            if (centersDist <= mode.r):
                return True
        return False

    # make two lists of rows and cols that enemies will traverse through
    def makeEnemyPaths(mode):
        # make lists of rows and cols that enemies will be in
        for row in range(mode.rows):
            choice = random.randint(0, mode.rows)
            if row % 2 != 0:
                mode.enemyRows.append(row)
                if row == mode.rows - 1:
                    continue
                mode.enemyCols.append(row + 1)

        # make lists of starting positions of enemies
        for row in mode.enemyRows:
            mode.rowEnemies.append([(row, 0)])
        for col in mode.enemyCols:
            mode.colEnemies.append([(0, col)])

        # make lists of all enemy positions
        for col in range(1, mode.cols):
            for enemy in mode.rowEnemies:
                if mode.maze[enemy[0][0]][col] == 1:
                    continue
                enemy.append((enemy[0][0], col))
        for row in range(1, mode.rows):
            for enemy in mode.colEnemies:
                if mode.maze[row][enemy[0][1]] == 1:
                    continue
                enemy.append((row, enemy[0][1]))

    def timerFired(mode):
        global score
        if mode.timerDelay % 300 == 0:
            mode.fillCounter += 1
            mode.moveEnemy()
            
        if (mode.intersects()):
            score -= 10

    def moveEnemy(mode):
        if mode.fillCounter % 2 == 0:
            mode.fill = 'red'
        else:
            mode.fill = 'yellow'

        mode.rowEnemyPositions = []
        mode.colEnemyPositions = []

        mode.counter += 1
        # list of current enemy positions
        if mode.rowEnemiesGo == True:
            for enemy in mode.rowEnemies:
                mode.rowEnemyPositions.append(enemy[mode.counter])
        else:
            mode.rowEnemyPositions = []
        
        if mode.colEnemiesGo == True:
            for enemy in mode.colEnemies:
                mode.colEnemyPositions.append(enemy[mode.counter])
        else:
            mode.colEnemyPositions = []
        # if at end, then enemy restarts
        if mode.counter == mode.rows - 1:
            mode.counter = -1
            mode.rowEnemiesGo = not mode.rowEnemiesGo
            mode.colEnemiesGo = not mode.colEnemiesGo

    def redrawAll(mode, canvas):
        mode.timerDelay += 100
        global score
        # draw the maze
        if mode.mazeMade == False:
            mode.maze = mode.makeMaze(mode.maze)
            while (MazeSolver(mode.maze).solve()[0] != True): 
                mode.maze = mode.makeMaze(mode.maze)
                mode.enemyMoves = MazeSolver(mode.maze).solve()[1]
            mode.mazeMade = True
        for row in range(mode.rows):
            for col in range(mode.cols):
                if mode.maze[row][col] == 1:
                    outline = 'black'
                    fill = 'black'
                elif mode.maze[row][col] == 0:
                    outline = 'white'
                    fill = 'white'
                if ((row == 0 and col == 0) or (row == mode.rows - 1 and col == mode.cols - 1)):
                    outline = 'green'
                    fill = 'green'
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill = fill, outline = outline)

        # draw coins
        if mode.coinsMade == False:
            mode.makeCoins()
        for coin in mode.coinsList:
            (x0,y0,x1,y1) = coin
            canvas.create_oval(x0 + mode.r, y0 + mode.r, x1 - mode.r, y1 - mode.r, fill = 'gold')

        for enemy in mode.rowEnemyPositions:
            (row, col) = enemy
            (x0, y0, x1, y1) = mode.getCellBounds(row, col)
            enemyCX = x0 + (.75 * mode.r) + (mode.r/2)
            enemyCY = y0 + (.75 * mode.r) + (mode.r/2)
            canvas.create_oval(enemyCX - mode.r/2, enemyCY - mode.r/2, enemyCX + mode.r/2, enemyCY + mode.r/2, fill = mode.fill)

        for enemy in mode.colEnemyPositions:
            (row, col) = enemy
            (x0, y0, x1, y1) = mode.getCellBounds(row, col)
            enemyCX = x0 + (.75 * mode.r) + (mode.r/2)
            enemyCY = y0 + (.75 * mode.r) + (mode.r/2)
            canvas.create_oval(enemyCX - mode.r/2, enemyCY - mode.r/2, enemyCX + mode.r/2, enemyCY + mode.r/2, fill = mode.fill)

        # draw score
        canvas.create_text(mode.width/2, 20, text=f'Score: {score}', font=mode.font, fill = 'red')

        # draw player
        canvas.create_oval(mode.playerPosition[0], mode.playerPosition[1], mode.playerPosition[0]
                            + mode.r, mode.playerPosition[1] + mode.r, fill = 'purple')
        

class WinMode(Mode):
    def appStarted(mode):
        mode.image = mode.scaleImage(mode.loadImage('winscreen.jpg'), .7)

    def redrawAll(mode, canvas):
        canvas.create_image(425, 475, image=ImageTk.PhotoImage(mode.image))
        font = 'Helvetica 15'
        canvas.create_text(mode.width/4, mode.height/7, text='You win!', font=font)
        canvas.create_text(mode.width/4, mode.height/7 + 50, text = f'Score: {score}', font = font)

class LoseMode(Mode):
    def appStarted(mode):
        mode.image = mode.scaleImage(mode.loadImage('losescreen.jpg'), .7)

    def redrawAll(mode, canvas):
        canvas.create_image(425, 475, image=ImageTk.PhotoImage(mode.image))
        font = 'Helvetica 15'
        canvas.create_text(mode.width/4, mode.height/4, text='You lose!', font=font)
        canvas.create_text(mode.width/4, mode.height/4 + 50, text = "Press 'r' to restart the maze.", font = font)

    def keyPressed(mode, event):
        global score 
        if (event.key == 'r'):
            score = 0
            mode.app.mazeMode.restartGame()
            mode.app.setActiveMode(mode.app.mazeMode)
            
# from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#subclassingModalApp
class HelpMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Helvetica 13'
        canvas.create_text(mode.width/2, mode.height/(mode.height/100), text ='Help Screen:', font = 'Helvetica 24')
        canvas.create_text(mode.width/2, mode.height/(mode.height/100) + 100, text ="Get through three levels to win, but don't touch the enemy!", font = font)
        canvas.create_text(mode.width/2, mode.height/(mode.height/100) + 150, text ="Collect points in submazes, but don't let the enemy touch you!", font = font)
        canvas.create_text(mode.width/2, mode.height/(mode.height/100) + 200, text ="Try to get the highest score!", font = font)
        canvas.create_text(mode.width/2, mode.height/(mode.height/100) + 250, text = "Press 'b' to see the enemy path.", font = font)
        canvas.create_text(mode.width/2, mode.height/(mode.height/100) + 300, text ='Press any key to return to the game.', font = font)

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.mazeMode)

class CoinScreen(Mode):
    def appStarted(mode):
        mode.image = mode.loadImage('coinscreen.png')
        mode.counter = 0

    def timerFired(mode):
        global coinScreenShown
        mode.counter += 1
        if mode.counter % 20 == 0:
            coinScreenShown = True
            mode.app.setActiveMode(mode.app.subMazeMode)

    def redrawAll(mode, canvas):
        canvas.create_image(300, 300, image=ImageTk.PhotoImage(mode.image))

class MyGame(ModalApp):
    def appStarted(mode):
        mode.loadingScreen = LoadingScreen()
        mode.introduction = Introduction()
        mode.sideScrollerMode = SideScrollerMode()
        mode.mazeMode = MazeMode()
        mode.subMazeMode = SubMazeMode()
        mode.helpMode = HelpMode()
        mode.winMode = WinMode()
        mode.loseMode = LoseMode()
        mode.coinScreen = CoinScreen()
        mode.setActiveMode(mode.loadingScreen)

mode = MyGame(width=600, height=600)