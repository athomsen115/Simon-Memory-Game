import random, sys, time, pygame

''' See goal upgrade photo for where to take this'''

#Game Setup Variables
FRAMES_PS = 30
WIDTH = 640
HEIGHT = 480
SPEED = 500 #milliseconds
DELAY = 200 #milliseconds
BUTTONSIZE = 200
BUTTONGAP = 20
TIMEOUT = 4 #seconds

#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
LRED = (155,0,0)
GREEN = (0,255,0)
LGREEN = (0,155,0)
BLUE = (0,0,255)
LBLUE = (0,0,155)
YELLOW = (255,255,0)
LYELLOW = (155,155,0)
GREY = (40,40,40)
BACKGROUND = BLACK

XMARGIN = int((WIDTH - (2 * BUTTONSIZE) - BUTTONGAP) / 2)
YMARGIN = int((HEIGHT - (2 * BUTTONSIZE) - BUTTONGAP) / 2)

# Button Objects
GREENBUTTON = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDBUTTON = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAP, YMARGIN, BUTTONSIZE, BUTTONSIZE)
YELLOWBUTTON = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAP, BUTTONSIZE, BUTTONSIZE)
BLUEBUTTON = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAP, YMARGIN + BUTTONSIZE + BUTTONGAP, BUTTONSIZE, BUTTONSIZE)

pygame.init()
pygame.font.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simon Emulator Memory Game')
clock = pygame.time.Clock()


def main():
    global font, beep1, beep2, beep3, beep4
    
    font = pygame.font.SysFont('comicsans', 20)
    infoText = font.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, WHITE)
    infoRect = infoText.get_rect()
    infoRect.topleft = (10, HEIGHT - 25)
    
    #Sound Files
    #beep1 = pygame.mixer.Sound('beep1.ogg')
    #beep2 = pygame.mixer.Sound('beep2.ogg')
    #beep3 = pygame.mixer.Sound('beep3.ogg')
    #beep4 = pygame.mixer.Sound('beep4.ogg')
    
    pattern = []
    currentStep = 0
    lastClickTime = 0
    score = 0
    waitingForInput = False
    clickedButton = None
    run = True
    
    while run:
        clickedButton = None
        win.fill(BACKGROUND)
        drawButtons()
        scoreLabel = font.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreLabel.get_rect()
        returntoMenu = font.render("Press 'ESC' to return to main menu", 1, WHITE)
        win.blit(returntoMenu, (0, 0))
        scoreRect.topleft = (WIDTH - 100, 10)
        win.blit(scoreLabel, scoreRect)
        win.blit(infoText, infoRect)
        
        checkForQuit()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                posx, posy = event.pos
                clickedButton = getButtonClicked(posx, posy)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #run = False
                    mainMenu()
                if event.key == pygame.K_q:
                    clickedButton = LGREEN
                elif event.key == pygame.K_w:
                    clickedButton = LRED
                elif event.key == pygame.K_a:
                    clickedButton = LYELLOW
                elif event.key == pygame.K_s:
                    clickedButton = LBLUE
                    
        if not waitingForInput:
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((LYELLOW, LBLUE, LRED, LGREEN)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(DELAY)
            waitingForInput = True
        else:
            if clickedButton and clickedButton == pattern[currentStep]:
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()
                
                if currentStep == len(pattern):
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0
                    updateScore(score)
            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                gameOverAnimation()
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        clock.tick(FRAMES_PS)
    
def terminate():
    pygame.quit()
    sys.exit()
    
def checkForQuit():
    for event in pygame.event.get(pygame.QUIT):
        terminate()
    #for event in pygame.event.get(pygame.KEYDOWN):
    #    if event.key == pygame.K_ESCAPE:
    #        terminate()
        pygame.event.post(event)
        
def mainMenu():
    click = False
    while True:
        win.fill(BLUE)
        font = pygame.font.SysFont('comicsans', 50)
        buttonFont = pygame.font.SysFont('comicsans', 30)
        title = font.render("Simon Emulator Memory Game", 1, WHITE)
        win.blit(title, (WIDTH/2 - title.get_width()/2 , 50))
        
        pic = pygame.image.load('simonGame.png')
        win.blit(pic, (WIDTH/2 - pic.get_width()/2, HEIGHT/2 - pic.get_height()/2))
        
        posx, posy = pygame.mouse.get_pos()
        
        button1 = pygame.Rect(70, 350, 200, 50)
        pygame.draw.rect(win, RED, button1)
        gameButton = buttonFont.render("Play Game", 1, WHITE)
        win.blit(gameButton, (65 + gameButton.get_width()/2, 355 + gameButton.get_height()/2))
        button2 = pygame.Rect(370, 350, 200, 50)
        pygame.draw.rect(win, RED, button2)
        scoreButton = buttonFont.render("High Score", 1, WHITE)
        win.blit(scoreButton, (370 + scoreButton.get_width()/2, 355 + scoreButton.get_height()/2))
        if button1.collidepoint(posx, posy):
            if click:
                main()
        if button2.collidepoint(posx, posy):
            if click:
                highScoreScreen()
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        
def updateScore(nscore):
    score = maxScore()
        
    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))
            
def maxScore():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
        
    return score
        
def highScoreScreen():
    run = True
    while run:
        score = maxScore()
        pic = pygame.image.load('simonSays.jpg')
        
        win.fill(GREEN)
        win.blit(pic, (WIDTH/2 - pic.get_width()/2, 50))
        scoreFont = pygame.font.SysFont('comicsans', 50)
    
        title = scoreFont.render("Highest Score to Date: " + score, 1, WHITE)
        win.blit(title, (WIDTH/2 - title.get_width()/2, 300))
        font = pygame.font.SysFont('comicsans', 30)
        returntoMenu = font.render("Press 'ESC' to return to main menu", 1, BLACK)
        win.blit(returntoMenu, (WIDTH/2 - returntoMenu.get_width()/2, 400))
        play = font.render("Press 'space' to play a game", 1, BLACK)
        win.blit(play, (WIDTH/2 - play.get_width()/2, 425))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainMenu()
                if event.key == pygame.K_SPACE:
                    main()
        
        pygame.display.update()

def flashButtonAnimation(color, animationSpeed=50):
    if color == LYELLOW:
        #sound = beep1
        flashColor = YELLOW
        rectangle = YELLOWBUTTON
    elif color == LBLUE:
        #sound = beep2
        flashColor = BLUE
        rectangle = BLUEBUTTON
    elif color == LRED:
        #sound = beep3
        flashColor = RED
        rectangle = REDBUTTON
    elif color == LGREEN:
        #sound = beep4
        flashColor = GREEN
        rectangle = GREENBUTTON
        
    screen  = win.copy()
    flashScreen = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashScreen = flashScreen.convert_alpha()
    r, g, b = flashColor
    #sound.play()
    for start, end, step in ((0,255,1),(255,0,-1)):
        for alpha in range(start, end, animationSpeed*step):
            checkForQuit()
            win.blit(screen, (0,0))
            flashScreen.fill((r, g, b, alpha))
            win.blit(flashScreen, rectangle.topleft)
            pygame.display.update()
            clock.tick(FRAMES_PS)
    win.blit(screen, (0, 0))

def drawButtons():
    pygame.draw.rect(win, LYELLOW, YELLOWBUTTON)
    pygame.draw.rect(win, LBLUE, BLUEBUTTON)
    pygame.draw.rect(win, LRED, REDBUTTON)
    pygame.draw.rect(win, LGREEN, GREENBUTTON)
    
def changeBackgroundAnimation(animationSpeed=40):
    global BACKGROUND
    newBG = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    newScreen = pygame.Surface((WIDTH, HEIGHT))
    newScreen = newScreen.convert_alpha()
    r, g, b = newBG
    for alpha in range(0, 255, animationSpeed):
        checkForQuit()
        win.fill(BACKGROUND)
        newScreen.fill((r, g, b, alpha))
        win.blit(newScreen, (0,0))
        
        pygame.display.update()
        clock.tick(FRAMES_PS)
        
    BACKGROUND = newBG

def gameOverAnimation(color=WHITE, animationSpeed=50):
    screen = win.copy()
    flashScreen = pygame.Surface(win.get_size())
    flashScreen = flashScreen.convert_alpha()
    #beep1.play()
    #beep2.play()
    #beep3.play()
    #beep4.play()
    
    r, g, b = color
    for _ in range(3):
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animationSpeed * step):
                checkForQuit()
                flashScreen.fill((r,g,b,alpha))
                win.blit(screen, (0,0))
                win.blit(flashScreen, (0,0))
                drawButtons()
                pygame.display.update()
                clock.tick(FRAMES_PS)
    
def getButtonClicked(x, y):
    if YELLOWBUTTON.collidepoint((x, y)):
        return LYELLOW
    elif BLUEBUTTON.collidepoint((x, y)):
        return LBLUE
    elif REDBUTTON.collidepoint((x, y)):
        return LRED
    elif GREENBUTTON.collidepoint((x, y)):
        return LGREEN
    

mainMenu() 
    