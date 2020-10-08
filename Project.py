import math
import random
import time
import winsound
import abc
import pygame

pygame.init()


class Entity:

    def __init__(self, startingX, startingY, entitySize, window, entityImage):
        # main items

        self.x = startingX
        self.y = startingY
        self.stepSize = 2
        self.entitySize = entitySize
        self.window = window
        self.direction = 'nil'
        self.previousDirection = 'right'
        self.hitBox = (self.x, self.y, self.entitySize, self.entitySize)
        self.entityImage = entityImage

    def possibleMoves(self):
        collision = False
        if self.direction == 'left' and self.x > 0:
            for singleWall in TwoDMap.walls:
                if self.x + self.hitBox[2] > singleWall.x and self.y + self.hitBox[3] > singleWall.y and self.x - \
                        self.stepSize * 2 < singleWall.x + singleWall.hitBox[2] and self.y < singleWall.y + \
                        singleWall.hitBox[3]:
                    collision = True

        elif self.direction == 'right' and self.x < screenX - self.entitySize - self.stepSize:
            for singleWall in TwoDMap.walls:
                if self.x + self.stepSize * 2 + self.hitBox[2] > singleWall.x and self.y + self.hitBox[
                    3] > singleWall.y and self.x < singleWall.x + singleWall.hitBox[2] and self.y < singleWall.y + \
                        singleWall.hitBox[3]:
                    collision = True
        elif self.direction == 'up' and self.y > 0:
            for singleWall in TwoDMap.walls:
                if self.x + self.hitBox[2] > singleWall.x and self.y + self.hitBox[
                    3] > singleWall.y and self.x < singleWall.x + \
                        singleWall.hitBox[2] and self.y - self.stepSize * 2 < singleWall.y + singleWall.hitBox[3]:
                    collision = True
        elif self.direction == 'down' and self.y < screenY - self.entitySize - self.stepSize:
            for singleWall in TwoDMap.walls:
                if self.x + self.hitBox[2] > singleWall.x and self.y + self.stepSize * 2 + self.hitBox[
                    3] > singleWall.y and self.x < singleWall.x + singleWall.hitBox[2] and self.y < singleWall.y + \
                        singleWall.hitBox[3]:
                    collision = True
        return collision


class Ghost(Entity):

    def __init__(self, startingX, startingY, entitySize, window, entityImage):
        super().__init__(startingX, startingY, entitySize, window, entityImage)
        self.direction = 'right'
        # image
        self.ghostPic = pygame.image.load(self.entityImage)
        self.ghostPic = pygame.transform.scale(self.ghostPic, (self.entitySize, self.entitySize))

    def display(self):
        self.window.blit(self.ghostPic, (self.x, self.y))
        self.hitBox = (self.x, self.y, self.entitySize, self.entitySize)

    def move(self):
        if (self.x + 1, self.y + 1) in TwoDMap.nodes or (self.x + 2, self.y + 1) in TwoDMap.nodes or \
                (self.x + 1, self.y + 2) in TwoDMap.nodes or (self.x + 2, self.y + 2) in TwoDMap.nodes:
            self.randomMove()
        else:
            if self.direction == 'left':
                self.x -= self.stepSize
            elif self.direction == 'right':
                self.x += self.stepSize
            elif self.direction == 'up':
                self.y -= self.stepSize
            elif self.direction == 'down':
                self.y += self.stepSize

    def randomMove(self):
        optionalMoves = ['left', 'right', 'up', 'down']
        random.shuffle(optionalMoves)
        index = optionalMoves.index(self.previousDirection)
        if index != 3:
            temp = optionalMoves[3]
            optionalMoves[3] = optionalMoves[index]
            optionalMoves[index] = temp
        for x in range(0, 4):
            self.direction = optionalMoves[x]
            self.previousDirection = self.direction
            if not self.possibleMoves():
                if self.direction == 'left':
                    self.x -= self.stepSize
                elif self.direction == 'right':
                    self.x += self.stepSize
                elif self.direction == 'up':
                    self.y -= self.stepSize
                elif self.direction == 'down':
                    self.y += self.stepSize
                break


class Pacman(Entity):

    def __init__(self, startingX, startingY, entitySize, window, entityImage):
        super().__init__(startingX, startingY, entitySize, window, entityImage)
        self.stepSize = 2
        self.scoreAmount = 100
        self.score = -100
        self.oldTime = 0
        self.currentTime = 0

        # images
        self.playerRightPic = pygame.image.load(self.entityImage)
        self.playerRightPic = pygame.transform.scale(self.playerRightPic, (self.entitySize, self.entitySize))
        self.playerLeftPic = pygame.transform.flip(self.playerRightPic, self.entitySize, self.entitySize)
        self.playerUpPic = pygame.transform.rotate(self.playerRightPic, 90)
        self.playerUpRightPic = pygame.transform.rotate(self.playerRightPic, 45)
        self.playerDownRightPic = pygame.transform.rotate(self.playerRightPic, -45)
        self.playerUpLeftPic = pygame.transform.rotate(self.playerLeftPic, -45)
        self.playerDownLeftPic = pygame.transform.rotate(self.playerLeftPic, 45)
        self.playerDownPic = pygame.transform.rotate(self.playerRightPic, -90)

    def display(self):
        if self.direction == 'right':
            self.window.blit(self.playerRightPic, (self.x, self.y))
        elif self.direction == 'left':
            self.window.blit(self.playerLeftPic, (self.x, self.y))
        elif self.direction == 'up':
            self.window.blit(self.playerUpPic, (self.x, self.y))
        else:
            self.window.blit(self.playerDownPic, (self.x, self.y))
        self.hitBox = (self.x, self.y, self.entitySize, self.entitySize)

    def TwoDmove(self, direction):
        player.previousDirection = player.direction
        player.direction = direction
        if self.direction == 'left' and self.x > 0:
            if self.possibleMoves():
                self.stepSize = 2
                self.direction = self.previousDirection
            else:
                self.x -= self.stepSize
                return
        elif self.direction == 'right' and self.x < screenX - self.entitySize - self.stepSize:
            if self.possibleMoves():
                self.stepSize = 2
                self.direction = self.previousDirection
            else:
                self.x += self.stepSize
                return
        elif self.direction == 'up' and self.y > 0:
            if self.possibleMoves():
                self.stepSize = 2
                self.direction = self.previousDirection
            else:
                self.y -= self.stepSize
                return
        elif self.direction == 'down' and self.y < screenY - self.entitySize - self.stepSize:
            if self.possibleMoves():
                self.stepSize = 2
                self.direction = self.previousDirection
            else:
                self.y += self.stepSize
                return
        return False

    def dotCollision(self, dot):
        if dot.visible is True and dot.hitBox[0] < self.hitBox[0] + self.hitBox[2] / 2 and dot.hitBox[1] < \
                self.hitBox[1] + self.hitBox[3] / 2 and dot.hitBox[0] + dot.hitBox[3] > self.hitBox[0] and \
                dot.hitBox[1] + dot.hitBox[2] > self.hitBox[1]:
            dot.visible = False
            if self.currentTime - self.oldTime > 2000:
                if player.scoreAmount > 1:
                    player.scoreAmount = player.scoreAmount - 1
                self.oldTime = pygame.time.get_ticks()
            player.currentTime = pygame.time.get_ticks()
            player.score += player.scoreAmount

    def ghostCollisionCheck(self):
        for entity in entityList:
            if entity is not player:
                if entity.hitBox[0] < self.hitBox[0] + self.hitBox[2] - 4 and entity.hitBox[1] < self.hitBox[1] + \
                        self.hitBox[3] - 4 and entity.hitBox[0] + entity.hitBox[3] > self.hitBox[0] and \
                        entity.hitBox[1] + entity.hitBox[2] > self.hitBox[1]:
                    return True
        return False


class MapHexagon:
    def __init__(self, x, y, radius, window):
        self.x = x
        self.y = y
        self.n = 6
        self.radius = radius
        self.window = window
        self.list = []
        for i in range(self.n):
            self.list.append((round(math.cos(i / self.n * math.pi * 2) * self.radius + self.x),
                              round(math.sin(i / self.n * math.pi * 2) * self.radius + self.y)))

    def display(self):
        pygame.draw.polygon(self.window, (0, 0, 0), self.list, 2)


class MapSquare:

    def __init__(self, x, y, width, height, window):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.window = window
        self.hitBox = (self.x, self.y, self.width, self.height)

    def display(self):
        pygame.draw.rect(self.window, (0, 128, 128), self.hitBox)


class DotSquare(MapSquare):

    def __init__(self, x, y, width, height, window, pic):
        super().__init__(x, y, width, height, window)
        self.dotSquarePic = pygame.image.load(pic)
        self.visible = True

    def display(self):
        if self.visible:
            self.window.blit(self.dotSquarePic, (self.x, self.y))


class FruitSquare(DotSquare):
    def __init__(self, x, y, width, height, window, pic):
        super().__init__(x, y, width, height, window, pic)

    def display(self):
        if self.visible:
            self.window.blit(self.dotSquarePic, (self.x, self.y))


class TwoDMap:

    def __init__(self):
        self.walls = []
        self.dots = []
        self.edges = [(25, 50), (25, 75), (25, 125), (25, 275), (25, 425), (25, 525), (50, 25), (75, 25), (100, 50),
                      (75, 100), (50, 100), (100, 75), (100, 125), (100, 175), (100, 200), (100, 225), (100, 250),
                      (75, 150), (50, 150), (125, 25), (100, 300), (100, 325), (100, 350), (100, 375), (100, 425),
                      (100, 475), (100, 550), (50, 550), (75, 550), (50, 275), (75, 275), (50, 400), (75, 400),
                      (50, 475), (75, 500), (0, 275), (150, 25), (175, 25), (300, 25), (325, 25), (350, 25), (400, 25),
                      (425, 25), (200, 50), (275, 50), (375, 50), (450, 50), (200, 75), (275, 75), (375, 75), (450, 75),
                      (125, 100), (175, 100), (225, 100), (250, 100), (300, 100), (350, 100), (400, 100), (425, 100),
                      (450, 125), (425, 150), (400, 150), (375, 125), (375, 175), (375, 200), (375, 225), (375, 250),
                      (400, 275), (425, 275), (450, 275), (475, 275), (375, 300), (375, 325), (375, 350), (375, 375),
                      (400, 400), (425, 400), (450, 425), (425, 475), (375, 425), (350, 450), (300, 450), (250, 450),
                      (225, 450), (175, 450), (125, 450), (350, 400), (300, 400), (175, 400), (125, 400), (275, 425),
                      (200, 425), (125, 550), (150, 550), (175, 550), (225, 550), (250, 550), (300, 550), (325, 550),
                      (350, 550), (375, 550), (400, 550), (425, 550), (450, 525), (275, 525), (200, 525), (175, 500),
                      (300, 500), (325, 475), (375, 475), (150, 475), (400, 500), (175, 150), (150, 125), (300, 150),
                      (325, 125), (275, 175), (300, 200), (325, 225), (325, 250), (350, 275), (325, 300), (325, 325),
                      (325, 375), (225, 200), (250, 200), (200, 175), (175, 200), (150, 225), (150, 250), (125, 275),
                      (150, 300), (150, 325), (150, 375), (200, 350), (175, 350), (225, 350), (250, 350), (275, 350),
                      (300, 350), (275, 300), (250, 300), (225, 300), (200, 300), (275, 275), (250, 275), (225, 275),
                      (200, 275), (275, 250), (250, 250), (225, 250), (200, 250)]
        self.nodes = [(25, 25), (100, 25), (200, 25), (275, 25), (375, 25), (450, 25), (25, 100), (100, 100),
                      (150, 100), (200, 100), (275, 100), (325, 100), (375, 100), (450, 100), (25, 150),
                      (100, 150), (150, 150), (200, 150), (275, 150), (325, 150), (375, 150), (450, 150),
                      (150, 200), (200, 200), (275, 200), (325, 200), (100, 275), (150, 275), (325, 275),
                      (375, 275), (150, 350), (325, 350), (25, 400), (100, 400), (150, 400), (200, 400),
                      (275, 400), (325, 400), (375, 400), (450, 400), (25, 450), (50, 450), (100, 450),
                      (150, 450), (200, 450), (275, 450), (325, 450), (375, 450), (425, 450), (450, 450),
                      (25, 500), (50, 500), (100, 500), (150, 500), (200, 500), (275, 500), (325, 500),
                      (375, 500), (425, 500), (450, 500), (25, 550), (200, 550), (275, 550), (450, 550),
                      (450, 275), (25, 275)]
        self.middle = [(200, 250), (225, 250), (250, 250), (275, 250), (200, 275), (225, 275), (250, 275), (275, 275),
                       (200, 300), (225, 300), (250, 300), (275, 300)]

    def teleportCheck(self):
        for entity in entityList:
            if entity.x < 1:
                entity.x = 471
                entity.y = 274

            if entity.x > 471:
                entity.x = 1
                entity.y = 274

    def dotCheck(self):
        for dot in self.dots:
            player.dotCollision(dot)

    def displayDefaultMap(self):
        for y in range(0, 600, 25):
            for x in range(0, 500, 25):
                if (x, y) not in self.nodes and (x, y) not in self.edges:
                    self.walls.append(MapSquare(x + 1, y + 1, 22, 22, screen))
                elif (x, y) not in self.middle:
                    self.dots.append(DotSquare(x, y, 3, 3, screen, 'dot.png'))


def twoPointGradientFunction(x1, y1, x2, y2):
    if (x2 - x1) != 0:
        return (y2 - y1) / (x2 - x1)
    else:
        return -1


class HexMap:

    def __init__(self):
        self.hexagon = []
        self.lineFirst = [(35, 50), (35, 50), (450, 50), (35, 530), (35, 50), (35, 300), (245, 50),
                          (160, 300), (330, 300)]
        self.lineSecond = [(35, 530), (450, 290), (450, 530), (450, 530), (450, 50), (450, 300), (245, 530),
                           (160, 530), (330, 530)]
        for x, y in zip(self.lineFirst, self.lineSecond):
            pygame.draw.line(screen, (0, 0, 0), x, y, 1)

    def displayDefaultMap(self):
        bool1 = True
        for y in range(-50, 650, 24):
            bool1 = not bool1
            for x in range(-50, 550, 84):
                if bool1:
                    z = 42
                else:
                    z = 0
                check = False
                tempHex = MapHexagon(x + z, y, 28, screen)  # for each hex
                for u, v in zip(self.lineFirst,
                                self.lineSecond):  # For each line check that each hexagon is not colliding with a line
                    m = twoPointGradientFunction(u[0], u[1], v[0], v[1])
                    if m != -1 and m != 0:
                        for a in range(u[0], v[0], 1):
                            pass
                            if tempHex.list[0][0] >= a >= tempHex.list[3][0] and tempHex.list[1][1] - 28 >= round(a * m) >= tempHex.list[5][1]:
                                check = True
                    elif m == -1:
                        for a in range(u[1], v[1], 1):
                            if tempHex.list[1][1] >= a >= tempHex.list[5][1] and u[0] < tempHex.list[0][0] < u[0] + 50:
                                check = True
                    elif m == 0:
                        for a in range(u[0], v[0], 1):
                            if tempHex.list[0][0] >= a >= tempHex.list[3][0] and tempHex.list[1][1] >= u[1] >= tempHex.list[5][1]:
                                check = True
                if check is False:
                    self.hexagon.append(tempHex)
                else:
                    del tempHex


def displayButtonMenu(Title, TopButton, MiddleButton, LastButton, restMouseButtons):
    screen.fill((255, 255, 255))
    if not restMouseButtons[0]:
        pygame.draw.rect(screen, (0, 128, 0), (175, 250, 150, 50))
    else:
        pygame.draw.rect(screen, (0, 178, 0), (175, 250, 150, 50))
    if not restMouseButtons[1]:
        pygame.draw.rect(screen, (0, 0, 128), (175, 350, 150, 50))
    else:
        pygame.draw.rect(screen, (0, 0, 178), (175, 350, 150, 50))
    if not restMouseButtons[2]:
        pygame.draw.rect(screen, (128, 0, 0), (175, 450, 150, 50))
    else:
        pygame.draw.rect(screen, (178, 0, 0), (175, 450, 150, 50))
    screen.blit(Title, textRectTitle)
    screen.blit(TopButton, textRectTop)
    screen.blit(MiddleButton, textRectMiddle)
    screen.blit(LastButton, textRectBottom)
    pygame.display.update()


def displayTwoDGameWindow():
    screen.fill((0, 0, 0))  # makes the game teal
    for singleWall in TwoDMap.walls:
        singleWall.display()
    for singleDot in TwoDMap.dots:
        singleDot.display()
    screen.blit(scoreText, scoreDisplay)
    scoreTextVar = fontScore.render(str(player.score), True, (255, 255, 255))
    screen.blit(scoreTextVar, scoreDisplayVar)
    player.display()
    inky.display()
    blinky.display()
    pinky.display()
    clyde.display()
    pygame.display.update()


def displayHexagonGameWindow():
    screen.fill((255, 255, 255))
    # for x, y in zip(HexMap.lineFirst, HexMap.lineSecond):
    #      pygame.draw.line(screen, (0, 0, 0), x, y, 1)
    for hexagon in HexMap.hexagon:
        hexagon.display()
    player.display()
    pygame.display.update()


def menuButtonFunctions(restMouseButtons):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if 200 + 150 > mouse[0] > 200 and 250 + 50 > mouse[1] > 250:
        restMouseButtons[0] = True
        if click[0] == 1:
            return 'Top'
    elif 200 + 150 > mouse[0] > 200 and 350 + 50 > mouse[1] > 350:
        restMouseButtons[1] = True
        if click[0] == 1:
            return 'Mid'
    elif 200 + 150 > mouse[0] > 200 and 450 + 50 > mouse[1] > 450:
        restMouseButtons[2] = True
        if click[0] == 1:
            return 'Bot'
    else:
        restMouseButtons[0] = False
        restMouseButtons[1] = False
        restMouseButtons[2] = False


screenX = 500
screenY = 600
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Pac-Man")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# initialising the object player (could be Pac-man but used player for re-usability and understandability)
clyde = Ghost(199, 199, 27, screen, 'clyde.jpg')
pinky = Ghost(224, 199, 27, screen, 'pinky.jpg')
inky = Ghost(249, 199, 27, screen, 'inky.jpg')
blinky = Ghost(274, 199, 27, screen, 'blinky.jpg')
player = Pacman(24, 24, 27, screen, 'pac.png')
entityList = [clyde, pinky, inky, blinky, player]
TwoDMap = TwoDMap()
HexMap = HexMap()

# Text and font setup
fontTitle = pygame.font.Font('freesansbold.ttf', 32)
fontButtons = pygame.font.Font('freesansbold.ttf', 20)
fontScore = pygame.font.Font('freesansbold.ttf', 16)

# title text creation
textTitleMenu = fontTitle.render('Pac-Man Game', True, (0, 0, 0))
textRectTitle = textTitleMenu.get_rect()
textRectTitle.center = (250, 125)
textTitleLevel = fontTitle.render('Pick The Level', True, (0, 0, 0))

# Top button text and creation
textPlay = fontButtons.render('Play', True, (255, 255, 255))
textRectTop = textPlay.get_rect()
textRectTop.center = (215, 275)
textSquare = fontButtons.render('Square', True, (255, 255, 255))

# Middle button text and creation
textConfigure = fontButtons.render('Configure', True, (255, 255, 255))
textRectMiddle = textPlay.get_rect()
textRectMiddle.center = (215, 375)
textHexagon = fontButtons.render('Hexagon', True, (255, 255, 255))

# Bottom button text and creation
textExit = fontButtons.render('Exit', True, (255, 255, 255))
textRectBottom = textExit.get_rect()
textRectBottom.center = (215, 475)
textArbitrary = fontButtons.render('Arbitrary', True, (255, 255, 255))

scoreText = fontScore.render('Score:', True, (255, 255, 255))
scoreDisplay = scoreText.get_rect()
scoreDisplay.center = (230, 260)
scoreDisplayVar = scoreText.get_rect()
scoreDisplayVar.center = (230, 280)

# loop booleans
restButtons = [False, False, False]  # respective to [Top, Mid, Bottom]
screenDisplay = [True, False, False, False,
                 False]  # respective to [Menu, Level, Configuration, Square, Hexagon, Arbitrary]
gameRunning = True

# clock used for FPS
clock = pygame.time.Clock()
while gameRunning:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False

    if screenDisplay[0]:
        pressed = menuButtonFunctions(restButtons)
        if pressed == 'Top':
            screenDisplay[1] = True
            screenDisplay[0] = False
            time.sleep(0.5)
        elif pressed == 'Mid':
            screenDisplay[2] = True
            screenDisplay[0] = False
            time.sleep(0.5)
        elif pressed == 'Bot':
            gameRunning = False
        displayButtonMenu(textTitleMenu, textPlay, textConfigure, textExit, restButtons)

    elif screenDisplay[1]:
        pressed = menuButtonFunctions(restButtons)
        if pressed == 'Top':
            time.sleep(0.5)
            screenDisplay[3] = True
            screenDisplay[1] = False
            TwoDMap.displayDefaultMap()
        elif pressed == 'Mid':
            screenDisplay[4] = True
            screenDisplay[1] = False
            HexMap.displayDefaultMap()
            time.sleep(0.5)
        elif pressed == 'Bot':
            time.sleep(0.5)
        displayButtonMenu(textTitleLevel, textSquare, textHexagon, textArbitrary, restButtons)

    elif screenDisplay[2]:  # beginning for configuration
        screenDisplay[0] = True
        screenDisplay[2] = False

    elif screenDisplay[3]:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.stepSize = 1
            player.TwoDmove('left')
        elif keys[pygame.K_RIGHT]:
            player.stepSize = 1
            player.TwoDmove('right')
        elif keys[pygame.K_UP]:
            player.stepSize = 1
            player.TwoDmove('up')
        elif keys[pygame.K_DOWN]:
            player.stepSize = 1
            player.TwoDmove('down')
        else:
            player.stepSize = 2
        if player.TwoDmove(player.direction) is False:
            player.stepSize = 1
            player.TwoDmove(player.previousDirection)
        inky.move()
        blinky.move()
        pinky.move()
        clyde.move()

        if player.ghostCollisionCheck():
            winsound.Beep(2500, 200)
            player.x = 24
            player.y = 24
        TwoDMap.teleportCheck()
        TwoDMap.dotCheck()
        displayTwoDGameWindow()

    elif screenDisplay[4]:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.stepSize = 1
            player.TwoDmove('left')
        elif keys[pygame.K_RIGHT]:
            player.stepSize = 1
            player.TwoDmove('right')
        elif keys[pygame.K_UP]:
            player.stepSize = 1
            player.TwoDmove('up')
        elif keys[pygame.K_DOWN]:
            player.stepSize = 1
            player.TwoDmove('down')
        else:
            player.stepSize = 2
        if player.TwoDmove(player.direction) is False:
            player.stepSize = 1
            player.TwoDmove(player.previousDirection)
        displayHexagonGameWindow()

pygame.quit()
