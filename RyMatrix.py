from math import cos, sin
from RyVector import RyVector


class RyMatrix:
    """ Very basic 3x3 Matrix functionality.
        i.e.    Apply transformation to a homogenous 2D vector.
                Multiply two 3x3 matrices. """
    def __init__(self, rows):
        self.rows = rows

    def row(self, i):
        """ Return row i. """
        return self.rows[i]

    def column(self, i):
        """ Return column i."""
        V = []
        for row in self.rows:
            V.append(row[i])
        return V

    def columns(self):
        """ Return list of columns. """
        columns = []
        for i in range(len(self.rows[0])):
            column = []
            for row in self.rows:
                column.append(row[i])
            columns.append(column)
        return columns

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            """ Multiply matrix by scalar. """
            result = []
            for row in self.rows:
                row_new = [other * i for i in row]
                result.append(row)
            return RyMatrix(result)
        elif isinstance(other, RyVector):
            """ Multiply 3x3 matrix by 2D homogenized vector. """
            V = (other.x, other.y, 1)  # homogenize
            V_new = []
            for row in self.rows:
                element = 0
                for i in range(len(self.rows)):
                    element += row[i] * V[i]
                V_new.append(element)
            return RyVector(V_new[0], V_new[1])
        elif isinstance(other, RyMatrix):
            """ Compose matrices together."""
            rows_new = []
            for row_i in range(len(self.rows)):
                row_new = []
                for col_i in range(len(other.columns())):
                    row = self.row(row_i)
                    col = other.column(col_i)
                    row_new.append(self._v3_dot(row, col))
                rows_new.append(row_new)
            return RyMatrix(rows_new)
        raise TypeError('Expected int/float/RyVector/RyMatrix')

    def _v3_dot(self, v1, v2):
        """ 3D vector dot product. """
        dot = 0
        for i in range(len(v1)):
            dot += v1[i] * v2[i]
        return dot

class RyIdentityMatrix(RyMatrix):
    def __init__(self):
        super().__init__([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

class RyTranslationMatrix(RyMatrix):
    """ Translate. """
    def __init__(self, dx, dy):
        rows = [[1, 0, dx], [0, 1, dy], [0, 0, 1]]
        super().__init__(rows)

class RyRotationMatrix(RyMatrix):
    """ Rotate about origin. """
    def __init__(self, angle):
        rows = [[cos(angle), sin(angle), 0], [-sin(angle), cos(angle), 0], [0, 0, 1]]
        super().__init__(rows)

class RyScalingMatrix(RyMatrix):
    """ Scale about origin. """
    def __init__(self, dw, dh):
        rows = [[dw, 0, 0], [0, dh, 0], [0, 0, 1]]
        super().__init__(rows)
