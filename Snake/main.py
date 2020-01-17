import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, color=(255, 0, 0)):
        self.pos = start
        self.dir_x = 1
        self.dir_y = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dir_x = dirnx
        self.dir_y = dirny
        self.pos = (self.pos[0] + self.dir_x, self.pos[1] + self.dir_y)
        pass

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * dis, j * dis, dis - 2, dis - 2))

        if eyes:
            centre = dis // 2
            radius = 3
            left_eye = (i * dis + centre - radius, j * dis + 8)
            right_eye = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), left_eye, radius)
            pygame.draw.circle(surface, (0, 0, 0), right_eye, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, position):
        self.color = color
        self.head = cube(position)
        self.body.append(self.head)
        self.dir_x = 0
        self.dir_y = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.dir_x = -1
                self.dir_y = 0
                self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
            elif keys[pygame.K_RIGHT]:
                self.dir_x = 1
                self.dir_y = 0
                self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
            elif keys[pygame.K_UP]:
                self.dir_x = 0
                self.dir_y = -1
                self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
            elif keys[pygame.K_DOWN]:
                self.dir_x = 0
                self.dir_y = 1
                self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dir_x == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dir_x == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dir_y == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dir_y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dir_x, c.dir_y)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dir_x = 0
        self.dir_y = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dir_x, tail.dir_y

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        if dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        if dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        if dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dir_x = dx
        self.body[-1].dir_y = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    siteBtw = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x += siteBtw
        y += siteBtw

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, apple
    surface.fill((0, 0, 0))
    s.draw(surface)
    apple.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomApple(item):
    global rows
    position = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), position))) > 0:
            continue
        else:
            break
    return (x, y)


def message_box(subject, content):
    text_box = tk.Tk()
    text_box.attributes("-topmost", True)
    text_box.withdraw()
    messagebox.showinfo(subject, content)
    try:
        text_box.destroy()
    except:
        pass


def main():
    global width, rows, s, apple
    width = 500
    height = 500
    rows = 20
    win = pygame.display.set_mode((width, height))
    s = snake((255, 0, 0), (10, 10))
    apple = cube(randomApple(s), color=(0, 255, 0))
    clock = pygame.time.Clock()
    flag = True
    while flag:
        pygame.time.delay(100)
        clock.tick(10)
        s.move()
        if s.body[0].pos == apple.pos:
            s.addCube()
            apple = cube(randomApple(s), color=(0, 255, 0))
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print("Your score is : ", len(s.body))
                message_box("You Lost!", "Play again :)")
                s.reset((10, 10))
                break

        redrawWindow(win)


main()
