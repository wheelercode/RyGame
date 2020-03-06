from copy import copy
from pygame import Rect

class RyRect(Rect):
    """ Custom pygame.Rect with value mapping to other RyRects."""
    def __init__(self, left, top, right, bottom):
        w = right - left
        h = bottom - top
        super().__init__(left, top, w, h)

    def map_point(self, r_dst, pt_src):
        """ Map a point from a source rect to a destination rect.
            i.e. map a point from world coordinates into screen coordinates. """
        (x_s, y_s) = pt_src
        x_d = self._map_range_value(self.left, self.right, r_dst.left, r_dst.right, x_s)
        y_d = self._map_range_value(self.bottom, self.top, r_dst.bottom, r_dst.top, y_s)
        return x_d, y_d

    def map_distance(self, r_dst, distance):
        rect = copy(self)
        rect.left = 0
        dst_dist, _ = rect.map_point(r_dst, (distance, 0))
        return dst_dist

    def map_rect(self, r_dst, rect):
        (left, top) = self.map_point(r_dst, (rect.left, rect.top))
        (right, bottom) = self.map_point(r_dst, (rect.right, rect.bottom))
        return RyRect(left, top, right, bottom)

    def map_points(self, r_dst, points):
        pts_dst = [self.map_point(r_dst, point) for point in points]
        return pts_dst

    def _map_range_value(self, src_min, src_max, dst_min, dst_max, src_value):
        """ Map a value from the src range to the dst range. """
        a, b, c, d, x_s = src_min, src_max, dst_min, dst_max, src_value
        return (d-c)*((x_s-b)/(b-a)) + d