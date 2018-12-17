from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
import numpy as np
from utils import Polygon, Cube, Tetrahedron


# licznik czasu - do wymuszenia częstotliwości odświeżania
tick = 0
moving_figure = 1

# parametry kamery
eye = np.array([0., 0., 15.])  # pozycja
orient = np.array([0., 0., -1.])  # kierunek
up = np.array([0., 1., 0.])  # góra


figures = [#Cube([2, 6, 5]),
           #Polygon([-2, -4, 2]),
           Tetrahedron([0, 0, 0], [2, 0, 0], [0, 2, 0], [1, 1, 2]),
           Tetrahedron([3, 0, 0], [5, 0, 0], [3, 2, 0], [4, 1, 2])]


# ruch kamery
def keypress(key, x, y):
    global eye, orient, up, moving_figure
    if key == b"e":
        eye = eye + orient * np.array([0.1, 0.1, 0.1])
    if key == b"q":
        eye = eye - orient * np.array([0.1, 0.1, 0.1])
    if key == b"a":
        right = np.cross(up, orient)
        right = right / np.linalg.norm(right)
        inverse = np.array([right, up, orient])
        inverse = np.transpose(inverse)
        rot = np.array([[np.cos(0.1), 0, np.sin(0.1)], [0, 1, 0],
        [-np.sin(0.1), 0, np.cos(0.1)]])
        orient = np.matmul(rot, np.array([0, 0, 1]))
        orient = np.matmul(inverse, orient)
    if key == b"d":
        right = np.cross(up, orient)
        right = right / np.linalg.norm(right)
        inverse = np.array([right, up, orient])
        inverse = np.transpose(inverse)
        rot = np.array([[np.cos(-0.1), 0, np.sin(-0.1)], [0, 1, 0],
        [-np.sin(-0.1), 0, np.cos(-0.1)]])
        orient = np.matmul(rot, np.array([0, 0, 1]))
        orient = np.matmul(inverse, orient)
    if key == b"s":
        right = np.cross(up, orient)
        right = right / np.linalg.norm(right)
        inverse = np.array([right, up, orient])
        inverse = np.transpose(inverse)
        rot = np.array([[1, 0, 0], [0, np.cos(0.1), -np.sin(0.1)],
        [0, np.sin(0.1), np.cos(0.1)]])
        orient = np.matmul(rot, np.array([0, 0, 1]))
        orient = np.matmul(inverse, orient)
        up = np.matmul(rot, np.array([0, 1, 0]))
        up = np.matmul(inverse, up)
    if key == b"w":
        right = np.cross(up, orient)
        right = right / np.linalg.norm(right)
        inverse = np.array([right, up, orient])
        inverse = np.transpose(inverse)
        rot = np.array([[1, 0, 0], [0, np.cos(-0.1), -np.sin(-0.1)],
        [0, np.sin(-0.1), np.cos(-0.1)]])
        orient = np.matmul(rot, np.array([0, 0, 1]))
        orient = np.matmul(inverse, orient)
        up = np.matmul(rot, np.array([0, 1, 0]))
        up = np.matmul(inverse, up)
    if key == b"b":
        for fig in figures:
            fig.draw_AABB = not fig.draw_AABB
    if key == b'f':
        for fig in figures:
            fig.draw_fill = not fig.draw_fill
    if key == b'i':
        figures[moving_figure].move([0, 0, -1])
    if key == b'k':
        figures[moving_figure].move([0, 0, 1])
    if key == b'j':
        figures[moving_figure].move([-1, 0, 0])
    if key == b'l':
        figures[moving_figure].move([1, 0, 0])
    if key == b'o':
        figures[moving_figure].rotate(np.pi/10, [0, 0, 1])
    if key == b'u':
        figures[moving_figure].rotate(-np.pi/10, [0, 0, 1])
    if key == b'0':
        moving_figure = 0
    if key == b'1':
        moving_figure = 1
    if key == b'2':
        moving_figure = 2
    if key == b'3':
        moving_figure = 3

def is_colliding_AABB(aabb1, aabb2):
    for i in range(3):
        if aabb1.max_vertices[i] < aabb2.min_vertices[i] or aabb1.min_vertices[i] > aabb2.max_vertices[i]:
            return False
    return True


def triangle_side(point1, point2, point3, p):
    return np.linalg.det(np.matrix([point1, point2, point3] - np.matrix(p)))


def triangle_collision(triangle1, triangle2):
    sides = [triangle_side(*triangle1, p) for p in triangle2]

    if any([s == 0 for s in sides]):
        return True

    if all([s > 0 for s in sides]) or all([s < 0 for s in sides]):
        return False
    return True


def figure_collision(figure1, figure2):
    for triangle1 in figure1.triangles:
        for triangle2 in figure2.triangles:
            if triangle_collision(figure1.vertices[triangle1], figure2.vertices[triangle2]):
                print('Kolizja')


def check_collisions(figures):
    for fig1 in figures:
        for fig2 in figures:
            if fig1 != fig2:
                figure_collision(fig1, fig2)


def check_collisions_AABB(figs):
    for fig in figs:
        fig.AABB.color = [0, 0, 0]

    colored = []

    for fig in figs:
        for f in figs:
            if f != fig and f not in colored:
                if is_colliding_AABB(f.AABB, fig.AABB):
                    # print('kolizja')
                    colored.append(f)

    for fig in colored:
        fig.AABB.color = [1, 0, 0]


# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick
    ltime = time.clock()
    if (ltime < tick + 0.1): # max 10 ramek / s
        return False
    tick = ltime
    return True


# pętla wyświetlająca
def display():
    if not cupdate():
        return
    global eye, orient, up
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1, 1, -1, 1, 1, 100)
    center = eye + orient
    gluLookAt(eye[0], eye[1], eye[2], center[0], center[1], center[2],
    up[0], up[1], up[2])
    global tetra2
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    check_collisions(figures)

    for fig in figures:
        fig.draw()

    glFlush()


glutInit()
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Kolizje 03")
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(keypress)
glClearColor(1.0, 1.0, 1.0, 1.0)
glClearDepth(1.0)
glDepthFunc(GL_LESS)
glEnable(GL_DEPTH_TEST)
glutMainLoop()