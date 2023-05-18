import pygame, os, random
from pygame import mixer
pygame.init()
pygame.mixer.init()

class Stopwatch:
    def __init__(self, font, screen, position):
        self.start_time = pygame.time.get_ticks()
        self.font = font
        self.screen = screen
        self.position = position

    def update(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        elapsed_seconds = elapsed_time // 1000
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        timer_text = f"Time: {minutes:02}:{seconds:02}"
        timer_surface = self.font.render(timer_text, True, LGREEN)
        self.screen.blit(timer_surface, self.position)


#Background sound
mixer.music.load("misc/walk_around.ogg")
mixer.music.play(-1)

#  Variables for Game
score = 0
gameWidth = 1920
gameHeight = 900
picSize = 96
gameColumns = 16
gameRows = 3
padding = 10
leftMargin = (gameWidth - ((picSize + padding) * gameColumns)) // 2
rightMargin = leftMargin
topMargin = (gameHeight - ((picSize + padding) * gameRows)) // 2
bottomMargin = topMargin
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LGREEN = (51, 255, 153)
smallfont = pygame.font.SysFont("comicsansms", 25)
timer_font = pygame.font.SysFont("comicsansms", 25)
last_click_time = 0

selection1 = None
selection2 = None

# Loading the pygame screen.
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption('Jeff Bozo The Game')
gameIcon = pygame.image.load('bozo.png') #Not showing :(
pygame.display.set_icon(gameIcon)

# Load the BackGround image into Python
bgImage = pygame.image.load('jeffBozo.png')
bgImage = pygame.transform.scale(bgImage, (gameWidth, gameHeight))
bgImageRect = bgImage.get_rect()



def updateScore(score, increment):
    total = score + increment
    text = smallfont.render(f"Current Turns: {total}", True, GREEN)
    screen.blit(text, [(gameWidth // 2) - 100, 50])
    return total

stopwatch = Stopwatch(timer_font, screen, (gameWidth - 300, 50))

# Create list of Memory Pictures
memoryPictures = []
for item in os.listdir('animal_tiles_resources/'):
    memoryPictures.append(item.split('.')[0])
memoryPicturesCopy = memoryPictures.copy()
memoryPictures.extend(memoryPicturesCopy)
memoryPicturesCopy.clear()
random.shuffle(memoryPictures)

# Load each of the images into the python memory
memPics = []
memPicsRect = []
hiddenImages = []
for item in memoryPictures:
    picture = pygame.image.load(f'animal_tiles_resources/{item}.png')
    picture = pygame.transform.scale(picture, (picSize, picSize))
    memPics.append(picture)
    pictureRect = picture.get_rect()
    memPicsRect.append(pictureRect)

for i in range(len(memPicsRect)):
    memPicsRect[i][0] = leftMargin + ((picSize + padding) * (i % gameColumns))
    memPicsRect[i][1] = topMargin + ((picSize + padding) * (i % gameRows))
    hiddenImages.append(False)


print(memoryPictures)
print(memPics)
print(memPicsRect)
print(hiddenImages)



gameLoop = True
while gameLoop:
    # Load background image
    screen.blit(bgImage, bgImageRect)
    
    #Turn counter
    score = updateScore(score, 0)
    
    #timer
    screen.blit(bgImage, bgImageRect)
    score = updateScore(score, 0)

    stopwatch.update()

    # Input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False
            

        
        
        
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            current_time = pygame.time.get_ticks()
            if current_time - last_click_time >= 100:  # Check if 1 seconds have passed
                last_click_time = current_time  # Update the last_click_time
                select_sound = pygame.mixer.Sound("misc/select.ogg")
                select_sound.play()
                for item in memPicsRect:
                    if item.collidepoint(event.pos):
                        if hiddenImages[memPicsRect.index(item)] != True:
                            if selection1 != None:
                                selection2 = memPicsRect.index(item)
                                hiddenImages[selection2] = True
                            else:
                                selection1 = memPicsRect.index(item)
                                hiddenImages[selection1] = True

    for i in range(len(memoryPictures)):
        if hiddenImages[i] == True:
            screen.blit(memPics[i], memPicsRect[i])
        else:
            picture1 = pygame.image.load('misc/tile_back.png')
            picture1 = pygame.transform.scale(picture1, (picSize, picSize))
            screen.blit(picture1, (memPicsRect[i][0], memPicsRect[i][1], picSize, picSize))
            
    pygame.display.update()

    if selection1 != None and selection2 != None:
        score = updateScore(score, 1)
        if memoryPictures[selection1] == memoryPictures[selection2]:
            correct_sound = pygame.mixer.Sound("misc/correct.ogg")
            correct_sound.play()
            selection1, selection2 = None, None
        else:
            wrong_sound = pygame.mixer.Sound("misc/wrong.ogg")
            wrong_sound.play()
            pygame.time.wait(1000)
            hiddenImages[selection1] = False
            hiddenImages[selection2] = False
            selection1, selection2 = None, None

    win = 1
    for number in range(len(hiddenImages)):
        win *= hiddenImages[number]

    if win == 1:
        gameLoop = False


    pygame.display.update()

pygame.quit()


