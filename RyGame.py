import pygame
from RyRect import RyRect


########################################################
class RyGame:
    """ A pygame drawing system. All drawing is done in
        world (arbitrary) coordinates. """
    def __init__(self, w, h, world=RyRect(0, 1, 1, 0)):
        pygame.init()
        self.pyscreen = pygame.display.set_mode((w, h), flags=pygame.HWSURFACE)
        self.screen = RyRect(0, 0, w, h)
        self.world = world
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 1e-10
        self.running = True
        self.run()

    def update(self):
        pass
        # update data
        # TODO

    def draw(self):
        pass

    def pause(self):
        # throttle the simulation framerate
        self.dt = self.clock.tick(self.fps) # will throttle to fps

    def handle_events(self):
        pass

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.pause()
        pygame.quit()

    def draw_rect(self, rect, color, width=0):
        screen_rect = self.world.map_rect(self.screen, rect)
        pygame.draw.rect(self.pyscreen, color, screen_rect, width)

    def draw_polygon(self, color, points, width=0):
        screen_points = self.world.map_points(self.screen, points)
        pygame.draw.polygon(self.pyscreen, color, screen_points, width)

    def draw_circle(self, color, center, radius, width=0):
        screen_center = self.world.map_point(self.screen, center)
        # apparently pygame.draw.circle only accepts integer values for center point
        screen_center = (int(screen_center[0]), int(screen_center[1]))
        screen_radius = int(self.world.map_distance(self.screen, radius))
        pygame.draw.circle(self.pyscreen, color, screen_center, screen_radius, width)

    def draw_ellipse(self, color, rect, width=0):
        screen_rect = self.world.map_rect(self.screen, rect)
        pygame.draw.ellipse(self.pyscreen, color, screen_rect, width)

    def draw_arc(self, color, rect, start_angle, stop_angle, width=1):
        screen_rect = self.world.map_rect(self.screen, rect)
        pygame.draw.arc(self.pyscreen, color, screen_rect, start_angle, stop_angle, width)

    def draw_line(self, color, start_pos, end_pos, width=1):
        beg = self.world.map_point(self.screen, start_pos)
        end = self.world.map_point(self.screen, end_pos)
        pygame.draw.line(self.pyscreen, color, beg, end, width)

    def draw_lines(self, color, closed, points, width=1):
        pts = self.world.map_points(self.screen, points)
        pygame.draw.lines(self.pyscreen, color, closed, pts, width)

    def draw_aaline(self, color, start_pos, end_pos, blend=1):
        beg = self.world.map_point(self.screen, start_pos)
        end = self.world.map_point(self.screen, end_pos)
        pygame.draw.aaline(self.pyscreen, color, beg, end, blend)

    def draw_aalines(self, color, closed, points, blend=1):
        pts = self.world.map_points(self.screen, points)
        pygame.draw.lines(self.pyscreen, color, closed, pts, blend)

# game = RyGame(700, 500, world=RyRect(-10, 10, 10, -10))