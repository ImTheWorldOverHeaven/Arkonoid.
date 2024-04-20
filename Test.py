import pygame
import sys
from time import sleep

pygame.init()

sleep(1.25)
move_right = False
move_left = False

back = (64, 64, 64)
mw = pygame.display.set_mode((1375, 775))
mw.fill(back)
clock = pygame.time.Clock()

racket_x = 675
racket_y = 625

dx = 7
dy = 7

game_over = False

monsters = []  # Initialize monsters list

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        pygame.draw.rect(mw, self.fill_color, self.rect)
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

ball = Picture('BallMonster.png', 160, 0, 200, 200)
platform = Picture('platformeGrass.png', 160, 200, 50, 50)

# Add monsters to the list
monsters.append(Picture('robot cop.png', x=100, y=100, width=50, height=50))
monsters.append(Picture('robot cop.png', x=500, y=100, width=50, height=50))
# Add more monsters as needed

while not game_over:
    mw.fill(back)  # Clear the screen
    ball.draw()
    platform.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False

    if move_right and platform.rect.x < 1151:
        platform.rect.x += 25
    if move_left and platform.rect.x > 0:
        platform.rect.x -= 25

    # Check collisions
    for m in monsters:
        m.draw()
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.draw()  # Redraw the monster after removing
            dy *= -1

    ball.rect.x += dx
    ball.rect.y += dy
    if ball.rect.y < 0:
        dy *= -1
    if ball.rect.x > 1325 or ball.rect.x < 0:
        dx *= -1
    if ball.rect.colliderect(platform.rect):
        dy *= -1

    if ball.rect.y > 750:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text('YOU LOSE', 60, (255, 0, 0))
        time_text.draw(10, 10)
        game_over = True
    if len(monsters) == 0:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text('YOU WIN', 60, (0, 200, 0))
        time_text.draw(10, 10)
        game_over = True

    pygame.display.update()
    clock.tick(60)  # Limit FPS to 60
