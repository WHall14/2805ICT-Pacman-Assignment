import pygame
import random

pygame.init()


class Ghost:

    def __init__(self, startingX, startingY, pic, window):
        self.x = startingX
        self.y = startingY
        self.stepSize = 1
        self.ghostSize = 24
        self.direction = 'right'
        self.window = window
        self.hitBox = (self.x, self.y, self.ghostSize, self.ghostSize)

        self.ghostImageName = pic
        self.ghostPic = pygame.image.load(self.ghostImageName)
        self.ghostPic = pygame.transform.scale(self.ghostPic, (self.ghostSize, self.ghostSize))

    def display(self):
        self.window.blit(self.ghostPic, (self.x, self.y))

    def move(self):
        if (self.x, self.y) in mapA.nodes or (self.x + 1, self.y) in mapA.nodes or (self.x, self.y + 1) in mapA.nodes \
                or (self.x + 1, self.y + 1) in mapA.nodes:
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

    def possibleMoves(self):
        collision = False
        if self.direction == 'left' and self.x > 0:
            for singleWall in mapA.walls:
                if self.x + self.hitBox[2] > singleWall.x and self.y + self.hitBox[3] > singleWall.y and self.x - \
                        self.stepSize * 2 < singleWall.x + singleWall.hitBox[2] and self.y < singleWall.y + \
                        singleWall.hitBox[3]:
                    collision = True
        elif self.direction == 'right' and self.x < screenX - self.ghostSize - self.stepSize:
            for singleWall in mapA.walls:
                if self.x + self.stepSize * 2 + self.hitBox[2] > singleWall.x and self.y + self.hitBox[
                    3] > singleWall.y and self.x < singleWall.x + singleWall.hitBox[2] and self.y < singleWall.y + \
                        singleWall.hitBox[3]:
                    collision = True
        elif self.direction == 'up' and self.y > 0:
            for singleWall in mapA.walls:
                if self.x + self.hitBox[2] > singleWall.x and self.y + self.hitBox[
                    3] > singleWall.y and self.x < singleWall.x + \
                        singleWall.hitBox[2] and self.y - self.stepSize * 2 < singleWall.y + singleWall.hitBox[3]:
                    collision = True
        elif self.direction == 'down' and self.y < screenY - self.ghostSize - self.stepSize:
            for singleWall in mapA.walls:
                if self.x + self.hitBox[2] > singleWall.x and self.y + self.stepSize * 2 + self.hitBox[
                    3] > singleWall.y and self.x < singleWall.x + singleWall.hitBox[2] and self.y < singleWall.y + \
                        singleWall.hitBox[3]:
                    collision = True
        return collision

    def randomMove(self):
        pathFound = False
        while not pathFound:
            temp = random.randint(1, 4)
            if temp == 1:
                self.direction = 'left'
                if not self.possibleMoves():
                    self.x -= self.stepSize
                    pathFound = True
            elif temp == 2:
                self.direction = 'right'
                if not self.possibleMoves():
                    self.x += self.stepSize
                    pathFound = True
            elif temp == 3:
                self.direction = 'up'
                if not self.possibleMoves():
                    self.y -= self.stepSize
                    pathFound = True
            elif temp == 4:
                self.direction = 'down'
                if not self.possibleMoves():
                    self.y += self.stepSize
                    pathFound = True


class Pacman:

    def __init__(self, startingX, startingY, characterSize, window):
        # main items

        self.x = startingX
        self.y = startingY
        self.stepSize = 2
        self.characterSize = characterSize
        self.window = window
        self.direction = 'nil'
        self.previousDirection = 'nil'
        self.hitBox = (self.x, self.y, self.characterSize, self.characterSize)

        # images
        self.playerImageName = 'pac.png'
        self.playerRightPic = pygame.image.load(self.playerImageName)
        self.playerRightPic = pygame.transform.scale(self.playerRightPic, (self.characterSize, self.characterSize))
        self.playerLeftPic = pygame.transform.flip(self.playerRightPic, self.characterSize, self.characterSize)
        self.playerUpPic = pygame.transform.rotate(self.playerRightPic, 90)
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
        self.hitBox = (self.x, self.y, self.characterSize, self.characterSize)

    def move(self):
        collision = False
        if self.direction == 'left' and self.x > 0:
            for singleWall in mapA.walls:
                if self.x + self.hitBox[2] > singleWall.x and self.y + self.hitBox[3] > singleWall.y and self.x - \
                        self.stepSize < singleWall.x + singleWall.hitBox[2] and self.y < singleWall.y + \
                        singleWall.hitBox[3]:
                    collision = True
                    self.stepSize = 2
                    self.direction = self.previousDirection
            if not collision:
                self.x -= self.stepSize
        elif self.direction == 'right' and self.x < screenX - self.characterSize - self.stepSize:
            for singleWall in mapA.walls:
                if self.x + self.stepSize + self.hitBox[2] > singleWall.x and self.y + self.hitBox[
                    3] > singleWall.y and self.x < singleWall.x + singleWall.hitBox[2] and self.y < singleWall.y + \
                        singleWall.hitBox[3]:
                    collision = True
                    self.stepSize = 2
                    self.direction = self.previousDirection
            if not collision:
                self.x += self.stepSize
        elif self.direction == 'up' and self.y > 0:
            for singleWall in mapA.walls:
                if self.x + self.hitBox[2] > singleWall.x and self.y + self.hitBox[
                    3] > singleWall.y and self.x < singleWall.x + \
                        singleWall.hitBox[2] and self.y - self.stepSize < singleWall.y + singleWall.hitBox[3]:
                    collision = True
                    self.stepSize = 2
                    self.direction = self.previousDirection
            if not collision:
                self.y -= self.stepSize
        elif self.direction == 'down' and self.y < screenY - self.characterSize - self.stepSize:
            for singleWall in mapA.walls:
                if self.x + self.hitBox[2] > singleWall.x and self.y + self.stepSize + self.hitBox[
                    3] > singleWall.y and self.x < singleWall.x + singleWall.hitBox[2] and self.y < singleWall.y + \
                        singleWall.hitBox[3]:
                    collision = True
                    self.stepSize = 2
                    self.direction = self.previousDirection
            if not collision:
                self.y += self.stepSize


class Wall:

    def __init__(self, x, y, width, height, window):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.window = window
        self.hitBox = (self.x, self.y, self.width, self.height)

    def display(self):
        self.hitBox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.window, (128, 128, 0), self.hitBox)


class Map:

    def __init__(self):
        self.walls = []

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

    def teleportCheck(self, entity):
        pass  # ###################################################################################################

    def displayDefaultMap(self):
        for y in range(0, 600, 25):
            for x in range(0, 500, 25):
                if (x, y) not in mapA.nodes and (x, y) not in mapA.edges:
                    self.walls.append(Wall(x, y, 24, 24, screen))
        self.walls.append(Wall(475, 275, 24, 24, screen))
        self.walls.append(Wall(0, 275, 24, 24, screen))


def displayMainMenu():
    screen.fill((255, 255, 255))
    if not mouseRestExit:
        pygame.draw.rect(screen, (128, 0, 0), (200, 350, 100, 50))
    else:
        pygame.draw.rect(screen, (178, 0, 0), (200, 350, 100, 50))
    if not mouseRestPlay:
        pygame.draw.rect(screen, (0, 128, 0), (200, 250, 100, 50))
    else:
        pygame.draw.rect(screen, (0, 178, 0), (200, 250, 100, 50))
    screen.blit(textTitle, textRectTitle)
    screen.blit(textExit, textRectExit)
    screen.blit(textPlay, textRectPlay)
    pygame.display.update()


def displayGameWindow():
    screen.fill((0, 0, 0))  # makes the game teal
    for singleWall in mapA.walls:
        singleWall.display()
    player.display()
    inky.display()
    blinky.display()
    pinky.display()
    clyde.display()
    pygame.display.update()


# Text and font setup
fontTitle = pygame.font.Font('freesansbold.ttf', 32)
fontButtons = pygame.font.Font('freesansbold.ttf', 20)

# title text creation
textTitle = fontTitle.render('Pac-Man Game', True, (0, 0, 0))
textRectTitle = textTitle.get_rect()
textRectTitle.center = (250, 125)

# exit button text and creation
textExit = fontButtons.render('Exit', True, (255, 255, 255))
textRectExit = textExit.get_rect()
textRectExit.center = (250, 375)

# Play button text and creation
textPlay = fontButtons.render('Play', True, (255, 255, 255))
textRectPlay = textPlay.get_rect()
textRectPlay.center = (250, 275)

screenX = 500
screenY = 600
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Pac-Man")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# initialising the object player (could be Pac-man but used player for re-usability and understandability)
clyde = Ghost(200, 200, 'clyde.jpg', screen)
pinky = Ghost(225, 200, 'pinky.jpg', screen)
inky = Ghost(250, 200, 'inky.jpg', screen)
blinky = Ghost(275, 200, 'blinky.jpg', screen)
player = Pacman(25, 25, 25, screen)
mapA = Map()

# loop booleans
mouseRestPlay = False
mouseRestExit = False
menu = True
gameScreen = False
gameRunning = True

mapA.displayDefaultMap()
# clock used for FPS
clock = pygame.time.Clock()
while gameRunning:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False

    if gameScreen:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.previousDirection = player.direction
            player.direction = 'left'
            player.move()
        elif keys[pygame.K_RIGHT]:
            player.previousDirection = player.direction
            player.direction = 'right'
            player.move()
        elif keys[pygame.K_UP]:
            player.previousDirection = player.direction
            player.direction = 'up'
            player.move()
        elif keys[pygame.K_DOWN]:
            player.previousDirection = player.direction
            player.direction = 'down'
            player.move()
        else:
            player.stepSize = 2
        player.move()
        inky.move()
        blinky.move()
        pinky.move()
        clyde.move()
        player.stepSize = 1
        displayGameWindow()

    elif menu:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 200 + 100 > mouse[0] > 200 and 250 + 50 > mouse[1] > 250:
            mouseRestPlay = True
            if click[0] == 1:
                menu = False
                gameScreen = True

        elif 200 + 100 > mouse[0] > 200 and 350 + 50 > mouse[1] > 350:
            mouseRestExit = True
            if click[0] == 1:
                gameRunning = False
        else:
            mouseRestPlay = False
            mouseRestExit = False
        displayMainMenu()

pygame.quit()
