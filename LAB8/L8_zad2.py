from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
import numpy as np


# licznik czasu - do wymuszenia częstotliwości odświeżania
tick = 0


# klasa pomocnicza, pozwalająca na odwoływanie się do słowników przez notację kropkową
class dd(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


# trojkaty
tri1 = {"a":[-4.0, 0.0], "b":[-2.0, 0.0], "c":[-1.0, 2.0], "col":[1, 0, 0]}; tri1 = dd(tri1)
tri2 = {"a":[-4.0, -4.0], "b":[-2.0, -6.0], "c":[-0.0, -0.0], "col":[0, 0, 1]}; tri2 = dd(tri2)
tri2.center = [(tri2.a[0] + tri2.b[0] + tri2.c[0]) / 3, (tri2.a[1] + tri2.b[1] + tri2.c[1]) / 3]
tri3 = {"a":[4.0, 4.0], "b":[2.0, 6.0], "c":[1.0, 1.0], "col":[0, 1, 1]}; tri3 = dd(tri3)
tri3.center = [(tri3.a[0] + tri3.b[0] + tri3.c[0]) / 3, (tri3.a[1] + tri3.b[1] + tri3.c[1]) / 3]

def check_point_in_triangle(tri1, tri2):
    x = [tri1.a, tri1.b, tri1.c]
    for p in x:
        alpha = ((p[0] - tri2.a[0]) * (tri2.c[1] - tri2.a[1]) - (tri2.c[0] - tri2.a[0]) * (p[1] - tri2.a[1])) / ((tri2.b[0] - tri2.a[0]) * (tri2.c[1] - tri2.a[1]) - (tri2.c[0] - tri2.a[0]) * (tri2.b[1] - tri2.a[1]))
        beta = ((tri2.b[0] - tri2.a[0]) * (p[1] - tri2.a[1]) - (p[0] - tri2.a[0]) * tri2.b[1] - tri2.a[1]) / ((tri2.b[0] - tri2.a[0]) * (tri2.c[1] - tri2.a[1]) - (tri2.c[0] - tri2.a[0]) * (tri2.b[1] - tri2.a[1]))
        if alpha > 0 and beta > 0 and alpha + beta <= 1:
            return 1
    return 0

def check_triangle_in_triangle(tri1, tri2):
    x = [tri1.a, tri1.b, tri1.c]
    out = 0
    for p in x:
        alpha = ((p[0] - tri2.a[0]) * (tri2.c[1] - tri2.a[1]) - (tri2.c[0] - tri2.a[0]) * (p[1] - tri2.a[1])) / ((tri2.b[0] - tri2.a[0]) * (tri2.c[1] - tri2.a[1]) - (tri2.c[0] - tri2.a[0]) * (tri2.b[1] - tri2.a[1]))
        beta = ((tri2.b[0] - tri2.a[0]) * (p[1] - tri2.a[1]) - (p[0] - tri2.a[0]) * tri2.b[1] - tri2.a[1]) / ((tri2.b[0] - tri2.a[0]) * (tri2.c[1] - tri2.a[1]) - (tri2.c[0] - tri2.a[0]) * (tri2.b[1] - tri2.a[1]))
        if alpha > 0 and beta > 0 and alpha + beta <= 1:
            out += 1
    if out > 2:
        return 1
    return 0

def check_crossing_triangles(*args):
    for triangle in args:
        for other_triangle in args:
            if triangle != other_triangle:
                if (check_crossing_lines([triangle.a, triangle.b], [other_triangle.a, other_triangle.b]) or
                    check_crossing_lines([triangle.a, triangle.b], [other_triangle.b, other_triangle.c]) or
                    check_crossing_lines([triangle.a, triangle.b], [other_triangle.c, other_triangle.a]) or


                    check_crossing_lines([triangle.b, triangle.c], [other_triangle.a, other_triangle.b]) or
                    check_crossing_lines([triangle.b, triangle.c], [other_triangle.b, other_triangle.c]) or
                    check_crossing_lines([triangle.b, triangle.c], [other_triangle.c, other_triangle.a]) or

                    check_crossing_lines([triangle.c, triangle.a], [other_triangle.a, other_triangle.b]) or
                    check_crossing_lines([triangle.c, triangle.a], [other_triangle.b, other_triangle.c]) or
                    check_crossing_lines([triangle.c, triangle.a], [other_triangle.c, other_triangle.a])):
                        print('kolizja')
                        triangle.col = np.random.randn(3)


def check_crossing_lines(line1, line2):
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


def check_collisions(tri1, tri2, tri3):
    if check_point_in_triangle(tri1, tri3) or check_point_in_triangle(tri3, tri1):
        print('tri1 x tri3, ', end='')
    if check_point_in_triangle(tri2, tri3) or check_point_in_triangle(tri3, tri2):
        print('tri2 x tri3, ', end='')
    if check_point_in_triangle(tri1, tri2) or check_point_in_triangle(tri2, tri1):
        print('tri1 x tri2, ', end='')
    check_crossing_triangles(tri1, tri2, tri3)
    if check_triangle_in_triangle(tri1, tri3):
        print('trojkat1 w trojkacie3 XD')
    if check_triangle_in_triangle(tri2, tri3):
        print('trojkat2 w trojkacie3 XD')
    if check_triangle_in_triangle(tri1, tri2):
        print('trojkat1 w trojkacie2 XD')

    if check_triangle_in_triangle(tri3, tri1):
        print('trojkat3 w trojkacie1 XD')
    if check_triangle_in_triangle(tri3, tri2):
        print('trojkat3 w trojkacie2 XD')
    if check_triangle_in_triangle(tri2, tri1):
        print('trojkat2 w trojkacie1 XD')




# funkcja rysująca trójkąt w 2d
def dtri2f(a, b, c, col):
    glColor3fv(col)
    glBegin(GL_POLYGON)
    glVertex2fv(a)
    glVertex2fv(b)
    glVertex2fv(c)
    glEnd()


# obsługa klawiatury
def keypress(key, x, y):
    global tri3
    if key == b"a": tri3.a[0] -= 0.1; tri3.b[0] -= 0.1; tri3.c[0] -= 0.1;
    if key == b"d": tri3.a[0] += 0.1; tri3.b[0] += 0.1; tri3.c[0] += 0.1;
    if key == b"w": tri3.a[1] += 0.1; tri3.b[1] += 0.1; tri3.c[1] += 0.1;
    if key == b"s": tri3.a[1] -= 0.1; tri3.b[1] -= 0.1; tri3.c[1] -= 0.1;
    tri3.center = [(tri3.a[0] + tri3.b[0] + tri3.c[0]) / 3,
    (tri3.a[1] + tri3.b[1] + tri3.c[1]) / 3]
    if key == b"q": tri3 = rotTri(tri3, 0.1)
    if key == b"e": tri3 = rotTri(tri3, -0.1)

# rotacja trójkąta (uwaga: deformacja przy każdym uruchomieniu)
def rotTri(tri, rot):
    nx = cos(rot) * (tri.a[0] - tri.center[0]) - sin(rot) * (tri.a[1] - tri.center[1]) + tri.center[0]
    ny = sin(rot) * (tri.a[0] - tri.center[0]) + cos(rot) * (tri.a[1] - tri.center[1]) + tri.center[1]
    tri.a[0] = nx; tri.a[1] = ny
    nx = cos(rot) * (tri.b[0] - tri.center[0]) - sin(rot) * (tri.b[1] - tri.center[1]) + tri.center[0]
    ny = sin(rot) * (tri.b[0] - tri.center[0]) + cos(rot) * (tri.b[1] - tri.center[1]) + tri.center[1]
    tri.b[0] = nx; tri.b[1] = ny
    nx = cos(rot) * (tri.c[0] - tri.center[0]) - sin(rot) * (tri.c[1] - tri.center[1]) + tri.center[0]
    ny = sin(rot) * (tri.c[0] - tri.center[0]) + cos(rot) * (tri.c[1] - tri.center[1]) + tri.center[1]
    tri.c[0] = nx; tri.c[1] = ny
    return tri


# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick
    ltime = time.clock()
    if ltime < tick + 0.1: # max 10 ramek / s
        return False
    tick = ltime
    return True


# pętla wyświetlająca
def display():
    if not cupdate():
        return
    global tri1, tri2, tri3
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    dtri2f(tri3.a, tri3.b, tri3.c, tri3.col)
    dtri2f(tri2.a, tri2.b, tri2.c, tri2.col)
    dtri2f(tri1.a, tri1.b, tri1.c, tri1.col)
    check_collisions(tri1, tri2, tri3)
    print('-')
    tri2 = rotTri(tri2, 0.1)
    glFlush()


glutInit()
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Kolizje 02")
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(keypress)
glClearColor(1.0, 1.0, 1.0, 1.0)
glClearDepth(1.0)
glDepthFunc(GL_LESS)
glEnable(GL_DEPTH_TEST)

# ustaw projekcję ortograficzną
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-10, 10, -10, 10, 15, 20)
gluLookAt(0.0, 0.0, 15.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
glMatrixMode(GL_MODELVIEW)
glutMainLoop()
