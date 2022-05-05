import pygame
import time
import random


pygame.mixer.init()

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

backgroundHalf = display.get_width()/2

background = pygame.image.load('static/room.jpg').convert_alpha()
background = pygame.transform.scale(background, (display.get_width()+backgroundHalf,
                                                 display.get_height()))

buzzingSound = pygame.mixer.Sound('static/buzzing.wav')
buzzingSound.set_volume(0.3)

doorSound = pygame.mixer.Sound('static/door.wav')
doorSound.set_volume(0.3)

speedJumpscare = pygame.image.load('static/speedjump.jpg')
speedJumpscare = pygame.transform.scale(speedJumpscare,
                                        (display.get_width(),
                                         display.get_height()))
speedJumpscareSound = pygame.mixer.Sound('static/jumpscare.wav')
speedJumpscareSound.set_volume(1000000000.1000)

display.blit(background, (0, 0))

buzzingSound.play()


class BaseSpeed:

    def __init__(self, sprite, size, aggressive, wait_time):

        self.sprite = pygame.transform.scale(sprite, size)
        self.size = size
        self.aggressive = aggressive
        self.waitTime = wait_time

        self.nextAttack = None
        self.beforeKill = None

        self.attacking = False

    def update(self):
        if not self.beforeKill:
            if not self.nextAttack:
                self.nextAttack = Timer(random.randint(self.aggressive,
                                                       self.aggressive*3))
            else:
                self.nextAttack.update()
        if self.beforeKill:
            self.beforeKill.update()

        if self.nextAttack:
            if self.nextAttack.done:
                self.nextAttack = None
                self.attacking = True
                self.beforeKill = Timer(self.waitTime)

        if self.beforeKill:
            if self.beforeKill.done:
                if doorOpen:
                    speedJumpscareSound.play()
                    time.sleep(1)
                    display.blit(speedJumpscare, (0, 0))
                    pygame.display.update()
                    time.sleep(1)
                    quit()
                else:
                    self.beforeKill = None
                    self.attacking = False


def update_draw_oxygen():

    global oxygen

    if not doorOpen:
        oxygen -= 0.1
        if oxygen <= 0:
            speedJumpscareSound.play()
            time.sleep(1)
            display.blit(speedJumpscare, (0, 0))
            pygame.display.update()
            time.sleep(1)
            quit()

    percent = oxygen/100

    print(percent)

    displayWidth = display.get_width()*percent

    pygame.draw.rect(display, (0, 255, 0),
                     (0, display.get_height()-60,
                      displayWidth, 60))

class Timer:

    def __init__(self, sleep):

        self.sleep = sleep
        self.finishTime = time.time() + sleep
        self.doneProcent = False
        self.done = False

    def update(self):

        self.doneProcent = (self.finishTime - time.time()) / self.sleep * 100

        if self.doneProcent >= 100:
            self.done = True

        if time.time() >= self.finishTime:
            self.done = True


xOffSet = 0

speedSprite = pygame.image.load('static/speedidle.jpg').convert_alpha()
speed = BaseSpeed(speedSprite,
                  (display.get_width()/2.5, display.get_height()/2.5),
                  3, 2)


timer = Timer(0.1)
lightsOut = False

doorCloseTimeOut = Timer(1)

doorOpen = True

oxygen = 100.0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mixer.get_busy():
                if doorCloseTimeOut.done:
                    doorCloseTimeOut = Timer(1)
                    doorSound.play()
                    if doorOpen:
                        doorOpen = False
                    else:
                        doorOpen = True

    timer.update()
    doorCloseTimeOut.update()

    mousePos = pygame.mouse.get_pos()

    xOffSet = mousePos[0]-backgroundHalf/2

    speed.update()

    if xOffSet < 0:
        xOffSet = 0
    if xOffSet > display.get_width()-backgroundHalf:
        xOffSet = display.get_width()-backgroundHalf

    if not pygame.mixer.get_busy():
        if not lightsOut:
            lightsOut = True
            timer = Timer(1)
            display.fill((0, 0, 0))
        if lightsOut:
            if timer.doneProcent >= 50:
                lightsOut = False
                buzzingSound.play()
    if timer.done:
        display.blit(background, (0-xOffSet, 0))
        if doorOpen:
            pygame.draw.rect(display, (0, 0, 0),
                             (display.get_width()/1.99-xOffSet, display.get_height()/4.5,
                              backgroundHalf, backgroundHalf/1.44))
            if speed.attacking:
                display.blit(speed.sprite, (display.get_width()/1.8-xOffSet,
                                            display.get_height()/3,))

    update_draw_oxygen()
    pygame.display.update()
