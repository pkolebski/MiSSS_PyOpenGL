import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def normalize(vec):
    return vec / np.linalg.norm(vec)


class Sphere():
    def __init__(self, v=[0, 0, 0], p=[0, 3, 0], col=[0, 0.5, 0], r=1, m=1, s=1, quad=None, gravity=1.5, aerodyn=0.2):
        self.v = np.array(v, dtype=np.float64)
        self.p = np.array(p, dtype=np.float64)
        self.col = col
        self.orginal_col = col
        self.r = np.array(r, dtype=np.float64)
        self.quad = quad
        self.m = r * m
        self.s = s
        self.gravity = gravity
        self.aerodyn = aerodyn

    def draw(self, angle=0, sphere=[]):
        glLoadIdentity()
        if angle != 0:
            glTranslate(sphere[0], sphere[1], sphere[2])
            glRotate(angle, 0, 1, 0)
            glTranslate(-sphere[0], -sphere[1], -sphere[2])
        glTranslatef(self.p[0], self.p[1], self.p[2])
        glColor3fv(self.col)
        gluSphere(self.quad, self.r, 16, 16)

    def update(self, dt, floor):
        if self.p[1] - self.r < floor:
            print("XD")
            self.v += [
                np.sign(self.v[0]) * -1 * self.aerodyn,
                np.sign(self.v[1]) * -1 * self.aerodyn,
                np.sign(self.v[2]) * -1 * self.aerodyn]
        else:
            self.v += [
                np.sign(self.v[0]) * -1 * self.aerodyn,
                -self.gravity + (np.sign(self.v[1]) * -1 * self.aerodyn),
                np.sign(self.v[2]) * -1 * self.aerodyn]

        self.p[0] += dt * self.v[0]
        self.p[1] += dt * self.v[1]
        self.p[2] += dt * self.v[2]


class Cube():
    def __init__(self, down, up, left, right, back, front, color=[1, 1, 0.5], fill=True):
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

    def draw(self, angle=0, sphere=[]):
        glLoadIdentity()
        if angle != 0:
            glTranslate(sphere[0], sphere[1], sphere[2])
            glRotate(angle, 0, 1, 0)
            glTranslate(-sphere[0], -sphere[1], -sphere[2])
        glColor3fv(self.color)
        if not self.fill: glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for link in self.links:
            glBegin(GL_POLYGON)
            for i in range(4):
                glVertex3fv(self.vertices[link[i]])
            glEnd()
        if not self.fill: glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
