import pygame
import sys


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, color=(255, 0, 0)):
        self.pos = start
        self.drinx = 1
        self.driny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.drinx = dirnx
        self.driny = dirny
        self.pos = (self.pos[0] + self.drinx, self.pos[1] + self.driny)
        pass

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i*dis + centre-radius,j*dis+8)
            circleMiddle2 = (i*dis+dis-radius*2,j*dis+8)
            pygame.draw.circle(surface,(0,0,0),circleMiddle,radius)
            pygame.draw.circle(surface,(0,0,0),circleMiddle2,radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, position):
        self.color = color
        self.head = cube(position)
        self.body.append(self.head)
        self.drinx = 0
        self.driny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.drinx = -1
                    self.driny = 0
                    self.turns[self.head.pos[:]] = [self.drinx, self.driny]
                elif keys[pygame.K_RIGHT]:
                    self.drinx = 1
                    self.driny = 0
                    self.turns[self.head.pos[:]] = [self.drinx, self.driny]
                elif keys[pygame.K_UP]:
                    self.drinx = 0
                    self.driny = -1
                    self.turns[self.head.pos[:]] = [self.drinx, self.driny]
                elif keys[pygame.K_DOWN]:
                    self.drinx = 0
                    self.driny = 1
                    self.turns[self.head.pos[:]] = [self.drinx, self.driny]
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.drinx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.drinx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.driny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.driny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.drinx, c.driny)

    def reset(self, pos):
        pass

    def addCube(self):
        pass

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
    global rows, width
    surface.fill((0, 0, 0))
    s.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def message_box(subject, content):
    pass


def main():
    global width, rows, s
    width = 500
    height = 500
    rows = 20
    win = pygame.display.set_mode((width, height))
    s = snake((255, 0, 0), (10, 10))
    clock = pygame.time.Clock()
    flag = True
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        redrawWindow(win)


main()
