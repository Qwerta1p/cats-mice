import pygame
import random
import sys
from pygame.locals import *

#создание констант
width = 600
height = 600
txtcolor = (255, 255, 255)
backcolor = (0, 0, 0)
FPS = 60 # Количество циклов в секунду


#size_diff = 1.754

minsize = 10
maxsize = 70
minSpeed = 7
maxSpeed = 10
NEWCAT = 5 # Количество новых котов
MouseSpeed = 5 #Кол-во пикселей, на которое моделька игрока перемещается в окне при каждом цикле.

def GameExit(): #Закрытие игры
    pygame.quit()
    sys.exit()

def Pause(): # Экран паузы. 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                GameExit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Нажатие ESC осуществляет выход.
                    GameExit()
                return

def collision(MouseObject, cats):
    for b in cats:
        if MouseObject.colliderect(b['rect']):
            return True
    return False

def Text(text, font, surface, x, y):
    textobj = font.render(text, 1, txtcolor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Настройка pygame, окна и указателя мыши.
pygame.init()# Установка pygame. Это нужно для любой pygame-программы.
mainClock = pygame.time.Clock() #Обеспечивает выполнение программы с надлежащей скоростью. 
windowSurface = pygame.display.set_mode((width, height))# Окно программы.
pygame.display.set_caption('Кошки-Мышки') #Загловок окна.
pygame.mouse.set_visible(False) #Делает мышь невидимой. 

# Настройка шрифтов.
font = pygame.font.SysFont(None, 35)

# Настройка звуков.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('gamemusic.wav')

# Настройка изображений.
playerImage = pygame.image.load('mouse.png')
MouseObject = playerImage.get_rect()
catImage = pygame.image.load('cat.png')
catSmileImage = pygame.image.load('cat_smile.png')

# Вывод начального экрана.
windowSurface.fill(backcolor)
Text('Кошки-Мышки', font, windowSurface, (width / 3), (height / 3))
Text('Нажмите клавишу для начала игры', font, windowSurface, (width / 5) - 30, (height / 3) + 50)
pygame.display.update()
Pause()

topScore = 0
while True:
    # Начало.
    cats = [] #Список словварей с ключами "rect", "speed", "surface".
    score = 0
    MouseObject.topleft = (width / 2, height - 50) # Начальное положение изображения игрока.
    moveLeft = moveRight = moveUp = moveDown = False
    catAdd = 0  # Показывает, когда нужно добавить нового кота.
    pygame.mixer.music.play(-1, 0.0) # Воспроизведение звука.
    pygame.mixer.music.set_volume(0.2)
    while True: # Игровой цикл выполняется, пока игра работает.
        #score += 1 # Увеличение количества очков.

        for event in pygame.event.get():
            if event.type == QUIT:
                GameExit()
            # Настройки управления.
            if event.type == KEYDOWN:
                
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                
                if event.key == K_ESCAPE:
                        GameExit()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                # Если мышь движется, переместить игрока к указателю мыши.
                MouseObject.centerx = event.pos[0]
                MouseObject.centery = event.pos[1]
        # Если необходимо, добавить новых котов в верхнюю часть экрана.

        catAdd += 1 # Добавление кота.
        if catAdd == NEWCAT: 
            catAdd = 0  
            catsize = random.randint(minsize, maxsize) # Рандомно выбирается размер кота.  
            newBaddie = {'rect': pygame.Rect(random.randint(0, width - catsize), 0 - catsize, catsize, catsize),
                        'speed': random.randint(minSpeed, maxSpeed),
                        'surface':pygame.transform.scale(catImage, (catsize, catsize)),
                        }
            score+=1
            cats.append(newBaddie)

        # Перемещение игрока по экрану.
        if moveLeft and MouseObject.left > 0:
            MouseObject.move_ip(-1 * MouseSpeed, 0)
        if moveRight and MouseObject.right < width:
            MouseObject.move_ip(MouseSpeed, 0)
        if moveUp and MouseObject.top > 0:
            MouseObject.move_ip(0, -1 * MouseSpeed)
        if moveDown and MouseObject.bottom < height:
            MouseObject.move_ip(0, MouseSpeed)

        # Перемещение котов вниз.
        for b in cats:
            b['rect'].move_ip(0, b['speed'])
            
            b['rect'].move_ip(0, -5)
            
            b['rect'].move_ip(0, 1)

        # Удаление котов, упавших за нижнюю границу экрана.
        for b in cats[:]:
            if b['rect'].top > height:
                cats.remove(b)

        # Отображение в окне игрового мира.
        windowSurface.fill(backcolor)

        # Отображение количества очков и лучшего результата.
        Text('Счет: %s' % (score), font, windowSurface, 10, 0)
        Text('Рекорд: %s' % (topScore), font, windowSurface, 10, 40)

        # Отображение прямоугольника игрока.
        windowSurface.blit(playerImage, MouseObject)

        # Отображение каждого кота.
        for b in cats:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Проверка, попал ли в игрока какой-либо из котов.
        if collision(MouseObject, cats):
            if score > topScore:
                topScore = score
            break

        mainClock.tick(FPS)

    # Отображение игры и вывод надписи 'Игра окончена'.
    pygame.mixer.music.stop()
    gameOverSound.set_volume(0.2)
    gameOverSound.play()
    for b in cats:
        wth = b['surface'].get_width()
        surf = pygame.transform.scale(catSmileImage, (wth, wth))
        windowSurface.blit(surf, b['rect'])
    pygame.display.update()
    Text('ИГРА ОКОНЧЕНА!', font, windowSurface, (width / 3), (height / 3))
    Text('Нажмите клавишу для начала игры', font, windowSurface, (width / 5) - 30, (height / 3) + 50)
    pygame.display.update()
    Pause()
    gameOverSound.stop()
