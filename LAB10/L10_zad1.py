from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
import numpy as np
from utils import Tetrahedron, Scene
import scipy

# licznik czasu - do wymuszenia czestotliwosci odswiezania
tick = 0

myszkax = 0
myszkay = 0

distance = 30


def mouseWheel(a, b, c, d):
    global distance
    distance += b


def myszka(x, y):
    global myszkax, myszkay
    myszkax = x
    myszkay = y
    glutPostRedisplay()


def keypress(key, x, y):
    global sphere
    if key == b'+':
        sphere.s += 0.1
        print('sprezystosc' + str(sphere.s))
    if key == b'-':
        sphere.s -= 0.1
        print('sprezystosc' + str(sphere.s))
    if key == b',':
        sphere.gravity += 1
    if key == b'.':
        sphere.gravity -= 1
    if key == b't':
        sphere.v = np.random.rand(3) * 20
    if key == b'p':
        sphere.aerodyn += 0.1
        print('areodynamika' + str(sphere.aerodyn))
    if key == b'o':
        sphere.aerodyn -= 0.1
        print('areodynamika' + str(sphere.aerodyn))


scene = Scene(fill=False)
tetrahedron = Tetrahedron()


# wymuszenie czestotliwosci odswiezania
def cupdate():
    global tick
    ltime = time.clock()
    if ltime < tick + 0.1:  # max 10 ramek / s
        return False
    tick = ltime
    return True


# petla wyswietlajaca
def display():
    global sphere, myszkax, myszkay, distance
    if not cupdate():
        return
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1, 1, -1, 1, 1, 100)

    eyeX = distance * np.cos(myszkay / 100) * np.sin(myszkax / 100)
    eyeY = distance * np.sin(myszkay / 100) * np.sin(myszkax / 100)
    eyeZ = distance * np.cos(myszkax / 100)

    gluLookAt(eyeX, eyeY, eyeZ, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    tetrahedron.update(0.2)
    tetrahedron.check_collisions(scene)
    scene.draw()
    tetrahedron.draw()

    glutSwapBuffers()
    # glFlush()


glutInit()
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Kolizje 05")
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutDisplayFunc(display)
glutIdleFunc(display)
glutMotionFunc(myszka)
glutKeyboardFunc(keypress)
glutMouseWheelFunc(mouseWheel)
glClearColor(1.0, 1.0, 1.0, 1.0)
glClearDepth(1.0)
glDepthFunc(GL_LESS)
glEnable(GL_DEPTH_TEST)
# przygotowanie oswietlenia
glEnable(GL_LIGHT0)
glLight(GL_LIGHT0, GL_POSITION, [0., 5., 5., 0.])
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
# przygotowanie sfery
# sphere.quad = gluNewQuadric()
# gluQuadricNormals(sphere.quad, GLU_SMOOTH)
glutMainLoop()
