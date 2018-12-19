from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
import numpy as np
from utils import Polygon, Cube, Tetrahedron, normalize


# licznik czasu - do wymuszenia częstotliwości odświeżania
tick = 0
moving_figure = 1

# parametry kamery
eye = np.array([0., 0., 15.])  # pozycja
orient = np.array([0., 0., -1.])  # kierunek
up = np.array([0., 1., 0.])  # góra


figures = [Cube([1, 0, 10], 2),
           Cube([1, 0, 10])]
           #Polygon([-2, -4, 2]),
           # Tetrahedron([0, 0, 0], [2, 0, 0], [0, 2, 0], [1, 1, 2]),
           # Tetrahedron([3, 0, 0], [5, 0, 0], [3, 2, 0], [4, 1, 2])]


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

    if all([s == 0 for s in sides]):
        x = [1 if all(triangle1[:, i] == triangle2[:, i]) else 0 for i in range(3)]
        if np.sum(x) > 0:
            arg = np.argsort(x)
            if check_crossing_triangles2D(triangle1[:, arg[:2]], triangle2[:, arg[:2]]) or \
                    check_point_in_triangle2D(triangle1[:, arg[:2]], triangle2[:, arg[:2]]) or \
                    check_point_in_triangle2D(triangle2[:, arg[:2]], triangle1[:, arg[:2]]):
                # print("kolizja punkt w środku")
                    pass
            return True

    if all([s > 0 for s in sides]) or all([s < 0 for s in sides]):
        # print('dziala')
        return False
    # print('nie dziala')

    intersection_points = []
    if triangle_plane_colliding_with_line(triangle1, triangle2[0], triangle2[1]):
        check, ip = find_intersection_point(triangle1, triangle2[0], triangle2[1])
        if check == 1:
            intersection_points.append(ip)
    if triangle_plane_colliding_with_line(triangle1, triangle2[1], triangle2[2]):
        check, ip = find_intersection_point(triangle1, triangle2[1], triangle2[2])
        if check == 1:
            intersection_points.append(ip)
    if triangle_plane_colliding_with_line(triangle1, triangle2[0], triangle2[2]):
        check, ip = find_intersection_point(triangle1, triangle2[0], triangle2[2])
        if check == 1:
            intersection_points.append(ip)
    # print(intersection_points)
    for point in intersection_points:
        print('create cube')
        cube = Cube(point, 0.1)
        cube.draw()
    return False

def find_intersection_point(triangle, p0, p1):
    a, b, c = triangle

    n = np.cross(b-a, c-a)
    n = n/np.linalg.norm(n)
    I = np.array([0, 0, 0])
    u = p1-p0
    w = p0 - a

    D = n @ u
    N = - n@w
    check = 0
    if abs(D) < 10e-7:
        if N == 0:
            check = 2
        else:
            check = 0

    sI = N/D
    I = p0 + np.array(sI) * np.array(u)

    if sI < 0 or sI > 1:
        check = 3
    else:
        check = 1

    return check, I

def triangle_plane_colliding_with_line(triangle, p1, p2):
    a, b, c = triangle

    v = np.cross(b - a, c - a)
    v = normalize(v)

    u = v @ a

    try:
        t = (u - v @ a) / (v @ (p2 - p1))
    except ZeroDivisionError:
        print('XD')
        return False
    x = p1 + t * (p2 - p1)
    # print(v, u, t, a, (p2-p1), (u - v @ a))
    return 0 <= t <= 1, x


def check_point_in_triangle2D(tri1, tri2):
    x = [tri1[0], tri1[1], tri1[2]]
    for p in x:
        alpha = ((p[0] - tri2[0][0]) * (tri2[2][1] - tri2[0][1]) - (tri2[2][0] - tri2[0][0]) * (p[1] - tri2[0][1])) / ((tri2[1][0] - tri2[0][0]) * (tri2[2][1] - tri2[0][1]) - (tri2[2][0] - tri2[0][0]) * (tri2[1][1] - tri2[0][1]))
        beta = ((tri2[1][0] - tri2[0][0]) * (p[1] - tri2[0][1]) - (p[0] - tri2[0][0]) * tri2[1][1] - tri2[0][1]) / ((tri2[1][0] - tri2[0][0]) * (tri2[2][1] - tri2[0][1]) - (tri2[2][0] - tri2[0][0]) * (tri2[1][1] - tri2[0][1]))
        if alpha > 0 and beta > 0 and alpha + beta <= 1:
            return 1
    return 0

def check_crossing_triangles2D(triangle, other_triangle):

    if (check_crossing_lines2D([triangle[0], triangle[1]], [other_triangle[0], other_triangle[1]]) or
        check_crossing_lines2D([triangle[0], triangle[1]], [other_triangle[1], other_triangle[2]]) or
        check_crossing_lines2D([triangle[0], triangle[1]], [other_triangle[2], other_triangle[0]]) or

        check_crossing_lines2D([triangle[1], triangle[2]], [other_triangle[0], other_triangle[1]]) or
        check_crossing_lines2D([triangle[1], triangle[2]], [other_triangle[1], other_triangle[2]]) or
        check_crossing_lines2D([triangle[1], triangle[2]], [other_triangle[2], other_triangle[0]]) or

        check_crossing_lines2D([triangle[2], triangle[0]], [other_triangle[0], other_triangle[1]]) or
        check_crossing_lines2D([triangle[2], triangle[0]], [other_triangle[1], other_triangle[2]]) or
        check_crossing_lines2D([triangle[2], triangle[0]], [other_triangle[2], other_triangle[0]])):
            return True
    return False


def check_crossing_lines2D(line1, line2):
    a = line1[0]
    b = line1[1]
    c = line2[0]
    d = line2[1]
    try:
        t = ((c[0] - a[0]) * (c[1] - d[1]) - (c[1] - a[1]) * (c[0] - d[0])) / ((b[0] - a[0]) * (c[1] - d[1]) - (b[1] - a[1]) * (c[0] - d[0]))
        s = ((b[0] - a[0]) *(c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) / ((b[0] - a[0]) * (c[1] - d[1]) - (b[1] - a[1]) * (c[0] - d[0]))
    except ZeroDivisionError:
        t = inf
        s = 1
    if 0 <= t <= 1 and 0 <= s <= 1:
        return 1
    return 0


def figure_collision(figure1, figure2):
    for triangle1 in figure1.triangles:
        for triangle2 in figure2.triangles:
            if triangle_collision(figure1.vertices[triangle1], figure2.vertices[triangle2]):
                # print('Kolizja')
                pass


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