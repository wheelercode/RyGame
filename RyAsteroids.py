from copy import copy
import pygame
from RyGame import RyGame
from RyRect import RyRect
from RyMatrix import RyTranslationMatrix, RyRotationMatrix, RyIdentityMatrix, RyScalingMatrix
from RyVector import RyVector

class Asteroids(RyGame):
    def __init__(self, w, h, world=RyRect(-100, 100, 100, -100)):
        self.ship = Ship(2, world)
        self.fps = 30
        super().__init__(w, h, world)

    def handle_events(self):
        # user input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_UP:
                    self.ship.thrusting = True
                if event.key == pygame.K_LEFT:
                    self.ship.rot_dir = -1
                    self.ship.rotating = True
                if event.key == pygame.K_RIGHT:
                    self.ship.rot_dir = 1
                    self.ship.rotating = True
                if event.key == pygame.K_DOWN:
                    pass

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.ship.thrusting = False
                if event.key == pygame.K_LEFT:
                    self.ship.rotating = False
                if event.key == pygame.K_RIGHT:
                    self.ship.rotating = False
                if event.key == pygame.K_DOWN:
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

    def update(self):
        self.ship.update(self.dt/1000)

    def draw(self):
        self.pyscreen.fill((0, 0, 0))
        # dir_point = (self.ship.direction()*10 + self.ship.pos).point()
        # self.draw_circle((0,255,0), dir_point, 2)
        # self.draw_circle((255,0,0), self.ship.pos.point(), 4)
        self.draw_lines((255, 255, 255), True, self.ship.points, width=1)
        # flip drawing buffer to screen
        pygame.display.flip()

class Ship:
    def __init__(self, size, world):
        self.world = world
        self.size = size
        self.pos = RyVector(0, 0)
        self.vel = RyVector(0, 0)
        self.acc = RyVector(0, 0)
        self.angle = 0
        self.origin_points = [(0, 4*size), (-3*size, -4*size), (0, -3*size), (3*size, -4*size)]
        self.points = copy(self.origin_points)
        self.R = RyIdentityMatrix()
        self.T = RyIdentityMatrix()
        self.thrusting = False
        self.rotating = False
        self.acc_max = 9.8
        self.vel_max = RyVector(200, 200)
        self.rot_dir = 1    # 1 or -1 for clock-wise or counter-clock
        self.rot_vel = 0
        self.rot_dv = 20
        self.rot_max = 35

    def reset_transformations(self):
        self.R = RyIdentityMatrix()
        self.T = RyIdentityMatrix()

    def translate(self, d_pos):
        self.T *= RyTranslationMatrix(d_pos.x, d_pos.y)
        self.pos = self.T * RyVector(0,0)

    def rotate(self, d_angle):
        self.R *= RyRotationMatrix(d_angle)
        self.angle += d_angle

    def direction(self):
        # return unit vector representing ship's forward pointing
        # direction (angle 0 = (0,1))
        direction = RyVector(0, 1)
        R = RyRotationMatrix(self.angle)
        return R * direction

    def wrap(self):
        # wrap from L->R, R->L, T->B, B->T
        x, y = self.pos.point()
        W = self.world
        if x < W.left:
            self.translate(RyVector(W.width, 0))
        if x > W.right:
            self.translate(RyVector(-W.width, 0))
        if y < W.bottom:
            self.translate(RyVector(0, -W.height))
        if y > W.top:
            self.translate(RyVector(0, W.height))

    def thrust(self, dt):
        # thrusting
        if self.thrusting:
            self.acc = self.direction() * self.acc_max
            vel_new = self.vel + self.acc
            # vel_max holds the maximum value
            # for the abs value of each component
            # respectively.

            # we check both positive and negative components
            if vel_new.x < self.vel_max.x and vel_new.x > -self.vel_max.x:
                self.vel.x = vel_new.x
            if vel_new.y < self.vel_max.y and vel_new.y > -self.vel_max.y:
                self.vel.y = vel_new.y
        else:
            self.acc = RyVector(0, 0)
        self.translate(self.vel * dt)

    def rotation(self, dt):
        # rotation
        if self.rotating:
            if abs(self.rot_vel) < self.rot_max:
                self.rot_vel += self.rot_dv * self.rot_dir * dt
        else:
            if self.rot_vel > 0:
                self.rot_vel -= self.rot_dv * dt
            elif self.rot_vel < 0:
                self.rot_vel += self.rot_dv * dt
        self.rotate(self.rot_vel * dt)

    def transform(self):
        # transform ship vertices
        V_origin_points = [RyVector(x, y) for x, y in self.origin_points]
        V_points = [self.T*self.R*P for P in V_origin_points]
        self.points = [V.point() for V in V_points]

    def update(self, dt):
        self.thrust(dt)     # linear motion
        self.rotation(dt)   # rotation motion
        self.transform()    # apply transformations to ships vertices
        self.wrap()         # wrap around screen edges

class Asteroid:
    pass

class Bullet:
    pass

class Enemy:
    pass
