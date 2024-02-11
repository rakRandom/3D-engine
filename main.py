import pygame as pg
from sys import exit as pyexit

RES = WIDTH, HEIGHT = 720, 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
POS_ZERO = pg.math.Vector2(0, 0)


class Triangle:
    def __init__(self, central_pos: pg.math.Vector3, height, width, depth):
        self.central_pos = central_pos
        self.height = height
        self.width = width
        self.depth = depth
        self.points: list[pg.math.Vector3] = []
        self.get_points()
        self.lines: list[tuple[pg.math.Vector3]] = []
        self.get_lines()

    def get_points(self):
        self.points = [
            self.central_pos,
            pg.math.Vector3(self.central_pos.x - self.width/2, self.central_pos.y - self.height, self.central_pos.z - self.depth/2),
            pg.math.Vector3(self.central_pos.x - self.width/2, self.central_pos.y - self.height, self.central_pos.z + self.depth/2),
            pg.math.Vector3(self.central_pos.x + self.width/2, self.central_pos.y - self.height, self.central_pos.z + self.depth/2),
            pg.math.Vector3(self.central_pos.x + self.width/2, self.central_pos.y - self.height, self.central_pos.z - self.depth/2)
        ]

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

        self.speed = 10
        self.axis = pg.math.Vector2(90, 90)
        self.fov = HEIGHT
        self.camera_pos = pg.math.Vector3(0.1, 0, 0)

        self.shapes = list()
        self.shapes.append(Triangle(pg.math.Vector3(-250, 200, 150), 200, 200, 200))
        self.shapes.append(Triangle(pg.math.Vector3(0, 200, 150), 200, 200, 200))
        self.shapes.append(Triangle(pg.math.Vector3(250, 200, 150), 200, 200, 200))

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

        if keys[pg.K_d]:
            self.camera_pos.x -= self.speed
        elif keys[pg.K_a]:
            self.camera_pos.x += self.speed
        elif keys[pg.K_e]:
            self.camera_pos.y += self.speed
        elif keys[pg.K_q]:
            self.camera_pos.y -= self.speed
        elif keys[pg.K_w]:
            self.camera_pos.z += self.speed
        elif keys[pg.K_s]:
            self.camera_pos.z -= self.speed
        elif keys[pg.K_LEFT]:
            self.axis.y -= 1
        elif keys[pg.K_RIGHT]:
            self.axis.y += 1
        elif keys[pg.K_UP]:
            self.axis.x -= 1
        elif keys[pg.K_DOWN]:
            self.axis.x += 1

    def draw(self):
        self.screen.fill(BLACK)

        # for shape in self.shapes:
        #     for line in shape.lines:
        #         if line[0] != () and line[1] != ():
        #             x1 = (WIDTH / 2) - ((-2 * line[0].x + WIDTH) * self.fov) / (2 * (self.fov + line[0].z))
        #             y1 = (HEIGHT / 2) - ((-2 * line[0].y + HEIGHT) * self.fov) / (2 * (self.fov + line[0].z))
        #             x2 = (WIDTH / 2) - ((-2 * line[1].x + WIDTH) * self.fov) / (2 * (self.fov + line[1].z))
        #             y2 = (HEIGHT / 2) - ((-2 * line[1].y + HEIGHT) * self.fov) / (2 * (self.fov + line[1].z))
        #             pg.draw.line(self.screen, WHITE, (x1, y1), (x2, y2))

        for shape in self.shapes:
            relative_central_pos = shape.central_pos - self.camera_pos
            relative_y_ang = POS_ZERO.angle_to(relative_central_pos.xz.normalize()) - self.axis.y / 2

            # print(relative_y_ang)

            for line in shape.lines:
                vec1 = line[0] - self.camera_pos
                vec2 = line[1] - self.camera_pos

                if vec1 and vec2:
                    # x1 = (WIDTH / 2) - ((-2 * vec1.x + WIDTH) * self.fov) / (2 * (self.fov + vec1.z))
                    # x2 = (WIDTH / 2) - ((-2 * vec2.x + WIDTH) * self.fov) / (2 * (self.fov + vec2.z))
                    #
                    # y1 = (HEIGHT / 2) - ((-2 * vec1.y + HEIGHT) * self.fov) / (2 * (self.fov + vec1.z))
                    # y2 = (HEIGHT / 2) - ((-2 * vec2.y + HEIGHT) * self.fov) / (2 * (self.fov + vec2.z))

                    x1 = (WIDTH * ((POS_ZERO.angle_to(vec1.xz.normalize()) - self.axis.y / 2) / 90))
                    x2 = (WIDTH * ((POS_ZERO.angle_to(vec2.xz.normalize()) - self.axis.y / 2) / 90))

                    y1 = (HEIGHT * ((POS_ZERO.angle_to(vec1.yz.normalize()) - self.axis.x / 2) / 90))
                    y2 = (HEIGHT * ((POS_ZERO.angle_to(vec2.yz.normalize()) - self.axis.x / 2) / 90))

                    pg.draw.line(self.screen, WHITE, (x1, y1), (x2, y2))


if __name__ == '__main__':
    main = Main()
    main.run()
