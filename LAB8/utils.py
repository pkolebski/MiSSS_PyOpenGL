import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Figure:
    def draw(self):
        if not self.draw_fill: glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_TRIANGLES)
        glColor(self.color)
        for triangle in self.triangles:
            glVertex3fv(self.vertices[triangle[0]])
            glVertex3fv(self.vertices[triangle[1]])
            glVertex3fv(self.vertices[triangle[2]])
        glEnd()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        if self.draw_AABB: self.AABB.draw()

    def rotate(self, angle, axis):
        cr = np.cos(angle)
        icr = 1 - cr
        sr = np.sin(angle)
        u = axis / np.linalg.norm(axis)
        rot_mtx = np.matrix([
            [cr + u[0] ** 2 * icr, u[0] * u[1] * icr - u[2] * sr, u[0] * u[2] * icr + u[1] * sr],
            [u[1] * u[0] * icr + u[2] * sr, cr + u[1] ** 2 * icr, u[1] * u[2] * icr - u[0] * sr],
            [u[2] * u[0] * icr - u[1] * sr, u[2] * u[1] * icr + u[0] * sr, cr + u[2] ** 2 * icr]
        ], dtype=np.float32)
        center = np.mean(self.vertices, axis=0)
        for i in range(len(self.vertices)):
            self.vertices[i] = ((self.vertices[i] - center) * rot_mtx) + center
        self.AABB = AABB(self)

    def move(self, vec):
        self.vertices += vec
        self.AABB = AABB(self)

class Polygon(Figure):
    def __init__(self, pos):
        t = (1.0 + np.sqrt(5.0)) / 2.0
        self.draw_AABB = False
        self.draw_fill = True
        self.color = np.array([0, 1, 1])
        self.vertices = np.array([[-1, t, 0],
                  [1, t, 0],
                  [-1, -t, 0],
                  [1, -t, 0],
                  [0, -1, t],
                  [0, 1, t],
                  [0, -1, -t],
                  [0, 1, -t],
                  [t, 0, -1],
                  [t, 0, 1],
                  [-t, 0, -1],
                  [-t, 0, 1]], dtype=np.float32) + pos

        self.triangles = np.array([[0, 11, 5],
                              [0, 5, 1],
                              [0, 1, 7],
                              [0, 7, 10],
                              [0, 10, 11],
                              [1, 5, 9],
                              [5, 11, 4],
                              [11, 10, 2],
                              [10, 7, 6],
                              [7, 1, 8],
                              [3, 9, 4],
                              [3, 4, 2],
                              [3, 2, 6],
                              [3, 6, 8],
                              [3, 8, 9],
                              [4, 9, 5],
                              [2, 4, 10],
                              [6, 2, 11],
                              [8, 6, 7],
                              [9, 8, 1]])
        self.AABB = AABB(self)


class Cube(Figure):
    def __init__(self, pos):
        self.draw_AABB = False
        self.draw_fill = True
        self.vertices = np.array([
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5]], dtype=np.float32) + pos

        self.color = np.array([0.5, 0.6, 0.2])
        self.triangles = np.array([[0, 1, 2],
                              [2, 3, 0],
                              [4, 5, 6],
                              [6, 7, 4],
                              [1, 5, 6],
                              [6, 2, 1],
                              [0, 4, 7],
                              [7, 3, 0],
                              [3, 2, 6],
                              [6, 7, 3],
                              [0, 1, 5],
                              [5, 4, 0]], dtype=np.int)

        self.AABB = AABB(self)

class Tetrahedron(Figure):
    def __init__(self, *args):
        self.vertices = np.array(args, dtype=np.float32)
        self.color = np.array([0, 1, 0.5])
        self.draw_AABB = False
        self.draw_fill = True
        self.triangles = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [1, 2, 3],
            [0, 2, 3]], dtype=np.int)

        self.AABB = AABB(self)


class AABB:
    def __init__(self, figure):
        self.min_vertices = np.min(figure.vertices, axis=0)
        self.max_vertices = np.max(figure.vertices, axis=0)
        self.color = [0, 0, 0]
        self.vertices = np.array([
            [self.min_vertices[0], self.min_vertices[1], self.min_vertices[2]],
            [self.max_vertices[0], self.min_vertices[1], self.min_vertices[2]],
            [self.max_vertices[0], self.max_vertices[1], self.min_vertices[2]],
            [self.min_vertices[0], self.max_vertices[1], self.min_vertices[2]],
            [self.min_vertices[0], self.min_vertices[1], self.max_vertices[2]],
            [self.max_vertices[0], self.min_vertices[1], self.max_vertices[2]],
            [self.max_vertices[0], self.max_vertices[1], self.max_vertices[2]],
            [self.min_vertices[0], self.max_vertices[1], self.max_vertices[2]]], dtype=np.float32)

        self.links = np.array([
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [3, 2, 6, 7],
            [1, 2, 6, 5],
            [0, 1, 5, 4],
            [0, 3, 7, 4]])

    def draw(self):
        for link in self.links:
            glColor(self.color)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBegin(GL_POLYGON)
            glVertex3fv(self.vertices[link[0]])
            glVertex3fv(self.vertices[link[1]])
            glVertex3fv(self.vertices[link[2]])
            glVertex3fv(self.vertices[link[3]])
            glEnd()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)