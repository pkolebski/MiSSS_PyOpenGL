from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
import numpy as np

# licznik czasu - do wymuszenia częstotliwości odświeżania
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
    if key == b'-':
        sphere.s -= 0.1
    if key == b',':
        sphere.gravity += 1
    if key == b'.':
        sphere.gravity -= 1
    if key == b't':
        sphere.v = np.random.rand(3) * 20

# klasa pomocnicza, pozwalająca na odwoływanie się do słowników przez notację kropkową
class dd(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Sphere():
    def __init__(self, v=[1, -1, 0], p=[0, 3, 0], col=[0, 0.5, 0], r=1, m=10, s=1.0, quad=None, gravity=.9, aerodyn=0.47):
        self.v = np.random.rand(3) * 10
        self.p = p
        self.col = col
        self.r = r
        self.quad = quad
        self.m = m
        self.s = s
        self.gravity = gravity
        self.aerodyn = aerodyn

    def draw(self):
        glLoadIdentity()
        glTranslatef(self.p[0], self.p[1], self.p[2])
        glColor3fv(self.col)
        gluSphere(self.quad, self.r, 16, 16)

    def update(self, dt):
        self.v += [np.sign(self.v[0]) * -1 * self.aerodyn, - self.gravity + (np.sign(self.v[1]) * -1 * self.aerodyn), np.sign(self.v[2]) * -1 * self.aerodyn]
        self.p[0] += dt * self.v[0]
        self.p[1] += dt * self.v[1]
        self.p[2] += dt * self.v[2]


class Cube():
    def __init__(self, down, up, left, right, back, front):
        self.down = down
        self.up = up
        self.left = left
        self.right = right
        self.front = front
        self. back = back

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
        glColor3fv([0.3, 0.3, 0.3])
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for link in self.links:
            glBegin(GL_POLYGON)
            for i in range(4):
                glVertex3fv(self.vertices[link[i]])
            glEnd()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


sphere = Sphere()
cube = Cube(0, 10, -10, 10, 10, -10)


def chceckSphereToCubeCollision(sphere, cube):
    if sphere.p[1] - sphere.r < cube.down:
        sphere.v[1] = -sphere.s * sphere.v[1]
        sphere.p[1] += cube.down - (sphere.p[1] - sphere.r)

    if sphere.p[1] + sphere.r > cube.up:
        sphere.v[1] = -sphere.s * sphere.v[1]
        sphere.p[1] -= (sphere.p[1] + sphere.r) - cube.up


    if sphere.p[0] - sphere.r < cube.front:
        sphere.v[0] = -sphere.s * sphere.v[0]
        sphere.p[0] += cube.front - (sphere.p[0] - sphere.r)

    if sphere.p[0] + sphere.r > cube.back:
        sphere.v[0] = -sphere.s * sphere.v[0]
        sphere.p[0] -= (sphere.p[0] + sphere.r) - cube.back


    if sphere.p[2] - sphere.r < cube.left:
        sphere.v[2] = -sphere.s * sphere.v[2]
        sphere.p[2] += cube.left - (sphere.p[2] - sphere.r)

    if sphere.p[2] + sphere.r > cube.right:
        sphere.v[2] = -sphere.s * sphere.v[2]
        sphere.p[2] -= (sphere.p[2] + sphere.r) - cube.right


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
    cube.draw()
    sphere.update(0.2)
    # updateSphereCollision(sphere)
    chceckSphereToCubeCollision(sphere, cube)
    sphere.draw()


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
# przygotowanie oświetlenia
glEnable(GL_LIGHT0)
glLight(GL_LIGHT0, GL_POSITION, [0., 5., 5., 0.])
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
# przygotowanie sfery
sphere.quad = gluNewQuadric()
gluQuadricNormals(sphere.quad, GLU_SMOOTH)
glutMainLoop()