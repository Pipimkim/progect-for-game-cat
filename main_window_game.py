import sys
import pygame
import os
import random
import pygame_widgets
from pygame_widgets.textbox import TextBox

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUN = [pygame.image.load(os.path.join("Assets/Cat", "CatRun1.jpg")),
       pygame.image.load(os.path.join("Assets/Cat", "CatRun2.jpg"))]
JUMP = pygame.image.load(os.path.join("Assets/Cat", "CatJump2.jpg"))
DOWN = [pygame.image.load(os.path.join("Assets/Cat", "CatDown1.jpg")),
        pygame.image.load(os.path.join("Assets/Cat", "CatDown1.jpg"))]

SMALL_DOG = [pygame.image.load(os.path.join("Assets/Dogs", "small.jpg")),
             pygame.image.load(os.path.join("Assets/Dogs", "small.jpg")),
             pygame.image.load(os.path.join("Assets/Dogs", "small.jpg"))]
BIG_DOG = [pygame.image.load(os.path.join("Assets/Dogs", "big.jpg")),
           pygame.image.load(os.path.join("Assets/Dogs", "big2.png")),
           pygame.image.load(os.path.join("Assets/Dogs", "big3.jpg"))]

DRON = [pygame.image.load(os.path.join("Assets/DRON", "dron.jpg")),
        pygame.image.load(os.path.join("Assets/DRON", "dron.jpg"))]

BACKGROUND = pygame.image.load(os.path.join("Assets/Other", "gra.jpg"))

textbox = TextBox(SCREEN, 100, 100, 300, 80, fontSize=50,
                  borderColour=(255, 0, 0), textColour=(0, 200, 0), radius=10, borderThickness=5)
a = True
b = False


class Cat:
    X_POS = 80
    Y_POS = 310
    Y_POS_DOWN = 340
    JUMP_VEL = 8

    def __init__(self):
        self.down_img = DOWN
        self.run_img = RUN
        self.jump_img = JUMP

        self.cat_down = b
        self.cat_run = a
        self.cat_jump = b

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.cat_rect = self.image.get_rect()
        self.cat_rect.x = self.X_POS
        self.cat_rect.y = self.Y_POS

    def update(self, vvod):
        if self.step_index >= 10:
            self.step_index = 0
        if vvod[pygame.K_UP] and not self.cat_jump:
            self.cat_down = b
            self.cat_run = b
            self.cat_jump = a
        elif vvod[pygame.K_DOWN] and not self.cat_jump:
            self.cat_down = a
            self.cat_run = b
            self.cat_jump = b
        elif not (self.cat_jump or vvod[pygame.K_DOWN]):
            self.cat_down, self.cat_run, self.cat_jump = b, a, b

        if self.cat_down:
            self.down()
        if self.cat_run:
            self.run()
        if self.cat_jump:
            self.jump()

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.cat_rect = self.image.get_rect()
        self.cat_rect.y = self.Y_POS
        self.step_index += 1
        self.cat_rect.x = self.X_POS

    def jump(self):
        self.image = self.jump_img
        if self.jump_vel < - self.JUMP_VEL:
            self.cat_jump = False
            self.jump_vel = self.JUMP_VEL
        if self.cat_jump:
            self.cat_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

    def down(self):
        self.image = self.down_img[self.step_index // 5]
        self.cat_rect = self.image.get_rect()
        self.cat_rect.y = self.Y_POS_DOWN
        self.cat_rect.x = self.X_POS
        self.step_index += 1

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.cat_rect.x, self.cat_rect.y))


class Prep:
    def __init__(self, img, type):
        self.img = img
        self.type = type
        self.rect = self.img[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def draw(self, SCREEN):
        SCREEN.blit(self.img[self.type], self.rect)

    def update(self):
        self.rect.x -= gas
        if self.rect.x < -self.rect.width:
            preps.pop()


class SmallDog(Prep):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class BigDog(Prep):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Dron(Prep):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.img[self.index // 5], self.rect)
        self.index += 1


def main():
    global gas, x_pos_bg, y_pos_bg, points, preps
    gas = 20  # скорость игры
    run = True
    clock = pygame.time.Clock()
    player = Cat()

    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    preps = []
    dead = 0

    def score():
        global points, gas
        points += 1
        if points % 200 == 0:
            gas += 1

        text = font.render("Очки: " + str(points), True, (0, 0, 0))
        txtc = text.get_rect()
        txtc.center = (1000, 40)
        SCREEN.blit(text, txtc)

    def background():
        global x_pos_bg, y_pos_bg
        SCREEN.blit(BACKGROUND, (x_pos_bg, y_pos_bg))
        image_width = BACKGROUND.get_width()
        SCREEN.blit(BACKGROUND, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BACKGROUND, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= gas

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        vvod = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(vvod)

        if len(preps) == 0:
            if random.randint(0, 2) == 0:
                preps.append(SmallDog(SMALL_DOG))
            elif random.randint(0, 2) == 1:
                preps.append(BigDog(BIG_DOG))
            elif random.randint(0, 2) == 2:
                preps.append(Dron(DRON))

        for prep in preps:
            prep.draw(SCREEN)
            prep.update()
            if player.cat_rect.colliderect(prep.rect):
                pygame.time.delay(2000)
                dead += 1
                menu(dead)

        background()
        score()
        clock.tick(30)
        pygame.display.update()


def menu(dead):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if dead == 0:
            text = font.render("Нажмите на любую кнопку, чтобы начать", True, (0, 0, 0))

        elif dead > 0:
            text = font.render("Нажмите на любую кнопку, чтобы начать сначала", True, (0, 0, 0))
            score = font.render("Ваш счёт: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUN[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()

            pygame_widgets.update(pygame.event.get())
            pygame.display.update()


menu(dead=0)
pygame.quit()
