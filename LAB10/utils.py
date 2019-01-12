import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def normalize(vec):
    return vec / np.linalg.norm(vec)


class Scene:
    def __init__(self, down, up, left, right, back, front, color=[1, 1, 1], fill=True):
        self.down = down
        self.up = up
        self.left = left
        self.right = right
        self.front = front
        self.back = back
        self.color = color
        self.fill = fill

        self.vertices = [
            [front, down, right],
            [back, down, right],
            [back, up, right],
            [front, up, right],
            [front, down, left],
            [back, down, left],
            [back, up, left],
            [front, up, left]]

        self.links = [
            [0, 1, 5, 4],
            [3, 2, 6, 7],
            [4, 5, 6, 7],
            [0, 1, 2, 3],
            [1, 2, 6, 5],
            [0, 3, 7, 4]
        ]

    def draw(self):
        glLoadIdentity()
        glColor3fv(self.color)
        if not self.fill: glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for link in self.links:
            glBegin(GL_POLYGON)
            for i in range(4):
                glVertex3fv(self.vertices[link[i]])
            glEnd()
        if not self.fill: glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


class Tetrahedron:
    def __init__(self, down, up, left, right, back, front, mass=3, color=[1, 1, 0.5], fill=True):
        self.down = down
        self.up = up
        self.left = left
        self.right = right
        self.front = front
        self.back = back
        self.color = color
        self.fill = fill
        self.mass = mass

        self.vertices = [
            [front, down, left],
            [front, down, right],
            [back, down, (left + right) / 2],
            [(front + back) / 2, up, (left + right) / 2]]

        self.r = np.mean(self.vertices[0:3])
        self.h = self.up - self.down

        self.links = [
            [0, 1, 3],
            [0, 1, 2],
            [1, 2, 3],
            [2, 3, 0]
        ]

        self.inertia_tensor = [
            [0.6 * self.mass * self.h ** 2 + 0.15 * self.mass * self.r ** 2, 0, 0],
            [0, 0.6 * self.mass * self.h ** 2 + 0.15 * self.mass * self.r ** 2, 0],
            [0, 0, 0.3 * self.mass * self.r ** 2]
        ]

    def draw(self):
        glLoadIdentity()
        glColor3fv(self.color)
        if not self.fill: glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for link in self.links:
            glBegin(GL_POLYGON)
            for i in range(3):
                glVertex3fv(self.vertices[link[i]])
            glEnd()
        if not self.fill: glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


def distance_point_wall(point, wall):
    a, b, c = np.cross(wall[0] - wall[1], wall[1] - wall[2])
    return np.abs(a * (point[0] - wall[0, 0]) + b * (point[1] - wall[0, 1]) + c * (point[2] - wall[0, 2]))
