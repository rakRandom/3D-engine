import pygame as pg
from sys import exit as pyexit

RES = WIDTH, HEIGHT = 720, 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Triangle:
    def __init__(self, central_pos: list[int, int, int], height, width, depth):
        self.central_pos = central_pos
        self.height = height
        self.width = width
        self.depth = depth
        self.points = list()
        self.get_points()
        self.lines = list()
        self.get_lines()

    def get_points(self):
        self.points = [self.central_pos,
                       (self.central_pos[0]-self.width/2, self.central_pos[1] + self.height, self.central_pos[2]-self.depth/2),
                       (self.central_pos[0]-self.width/2, self.central_pos[1] + self.height, self.central_pos[2]+self.depth/2),
                       (self.central_pos[0]+self.width/2, self.central_pos[1] + self.height, self.central_pos[2]+self.depth/2),
                       (self.central_pos[0]+self.width/2, self.central_pos[1] + self.height, self.central_pos[2]-self.depth/2)]

    def get_lines(self):
        self.lines = [(self.points[0], self.points[1]),
                      (self.points[0], self.points[2]),
                      (self.points[0], self.points[3]),
                      (self.points[0], self.points[4]),
                      (self.points[1], self.points[2]),
                      (self.points[2], self.points[3]),
                      (self.points[3], self.points[4]),
                      (self.points[4], self.points[1])]


class Main:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Engine 3D")
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()

        self.fov = HEIGHT
        self.shapes = list()
        self.shapes.append(Triangle([150, 100, 150], 200, 200, 200))

    def run(self):
        while True:
            self.event_handler()
            self.update()
            self.draw()
            self.clock.tick(90)
            pg.display.update()

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                pyexit(0)

    def update(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT]:
            for shape in self.shapes:
                shape.central_pos[0] += 1
                shape.get_points()
                shape.get_lines()
        elif keys[pg.K_LEFT]:
            for shape in self.shapes:
                shape.central_pos[0] -= 1
                shape.get_points()
                shape.get_lines()
        elif keys[pg.K_UP]:
            for shape in self.shapes:
                shape.central_pos[1] -= 1
                shape.get_points()
                shape.get_lines()
        elif keys[pg.K_DOWN]:
            for shape in self.shapes:
                shape.central_pos[1] += 1
                shape.get_points()
                shape.get_lines()

    def draw(self):
        self.screen.fill(BLACK)

        for shape in self.shapes:
            for line in shape.lines:
                if line[0] != () and line[1] != ():
                    x1 = (WIDTH / 2) - ((-2 * line[0][0] + WIDTH) * self.fov) / (2 * (self.fov + line[0][2]))
                    y1 = (HEIGHT / 2) - ((-2 * line[0][1] + HEIGHT) * self.fov) / (2 * (self.fov + line[0][2]))
                    x2 = (WIDTH / 2) - ((-2 * line[1][0] + WIDTH) * self.fov) / (2 * (self.fov + line[1][2]))
                    y2 = (HEIGHT / 2) - ((-2 * line[1][1] + HEIGHT) * self.fov) / (2 * (self.fov + line[1][2]))
                    pg.draw.line(self.screen, WHITE, (x1, y1), (x2, y2))


if __name__ == '__main__':
    main = Main()
    main.run()
