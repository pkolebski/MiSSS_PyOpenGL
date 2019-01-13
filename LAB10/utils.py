import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def normalize(vec):
    return vec / np.linalg.norm(vec)


class Figure:
    def __init__(self, points=None, links=None, color=[1, 1, 1], fill=True):
        self.vertices = 3*np.array([
            [7, -10, -10],
            [15, 10, -10],
            [-10, 10, -10],
            [-10, -10, -10],
            [7, -10, 10],
            [15, 10, 10],
            [-10, -10, 10],
            [-10, 10, 10]]
        ) if points is None else points
        self.links = np.array([
            [0, 1, 2, 3],
            [4, 5, 7, 6],
            [0, 1, 5, 4],
            [2, 3, 6, 7],
            [0, 3, 6, 4],
            [1, 2, 7, 5]
        ]) if links is None else links
        self.color = color
        self.fill = fill

    def check_collisions(self, obj):
        for link in obj.links:
            for point in self.vertices:
                if distance_point_wall(point, obj.vertices[link]) < 0.4:
                    print("kolizja")

    def draw(self):
        glLoadIdentity()
        glColor3fv(self.color)
        if not self.fill: glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for link in self.links:
            glBegin(GL_POLYGON)
            for i in range(len(link)):
                glVertex3fv(self.vertices[link[i]])
            glEnd()
        if not self.fill: glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def calculate_r(self, alpha, beta, gamma):
        return np.array(
            [[np.cos(beta) * np.cos(gamma),                                                 -np.cos(beta) * np.sin(gamma),                                                 np.sin(beta)             ],
             [np.sin(alpha) * np.sin(beta) + np.cos(alpha) * np.sin(gamma),                  -np.sin(alpha) * np.sin(beta) * np.sin(gamma) + np.cos(alpha) * np.cos(gamma), -np.sin(alpha) * np.cos(beta)],
             [-np.cos(alpha) * np.sin(beta) * np.cos(gamma) + np.sin(alpha) * np.sin(gamma), np.cos(alpha) * np.sin(beta) * np.sin(gamma) + np.sin(alpha) * np.cos(gamma),  np.cos(alpha) * np.cos(beta)]
             ], dtype=np.float32)


class Scene(Figure):
    pass


class Tetrahedron(Figure):
    def __init__(self, v=[1, 1, 1], points=None, links=None, mass=3, color=[1, 1, 0.5], fill=True):
        vertices = np.array([
            [5, 5, 0],
            [-5, 5, 0],
            [0, -3, 0],
            [0, 0, 5],
        ], dtype=np.float32) if points is None else points

        links = np.array([
            [0, 1, 2],
            [1, 3, 2],
            [3, 0, 2],
            [0, 3, 1],
        ]) if links is None else links
        super().__init__(vertices, links, color=color, fill=fill)
        self.mass = mass
        self.mass_center = np.mean(self.vertices)
        self.linear_velocity = np.array(v, dtype=np.float32)
        self.angular_velocity = np.array([0.5, 0, 0], dtype=np.float32)
        self.r = np.mean(self.vertices[0:3])
        self.h = distance_point_wall(self.vertices[-1, :], self.vertices[:3, :])
        self.p = self.vertices
        self.momentum = self.mass * self.linear_velocity

        self.inertia_tensor = [
            [0.6 * self.mass * self.h ** 2 + 0.15 * self.mass * self.r ** 2, 0, 0],
            [0, 0.6 * self.mass * self.h ** 2 + 0.15 * self.mass * self.r ** 2, 0],
            [0, 0, 0.3 * self.mass * self.r ** 2]
        ]

    def update(self, dt):
        self.p = self.p @ self.calculate_r(*self.angular_velocity)
        self.p += dt * self.linear_velocity
        self.vertices = self.p
        self.mass_center = np.mean(self.vertices)
        self.momentum = self.mass * self.linear_velocity

def distance_point_wall(point, wall):
    a, b, c = np.cross(wall[0] - wall[1], wall[1] - wall[2])
    return np.abs(a * (point[0] - wall[0, 0]) + b * (point[1] - wall[0, 1]) + c * (point[2] - wall[0, 2]))
