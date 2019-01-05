from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
import numpy as np
from utils import Sphere, Cube, normalize

tick = 0
myszkax = 429
myszkay = 418

distance = 30
cubes = []
spheres = []
cubes.append(Cube(0, 2, -10, 10, -10, 10, color=[0, 1, 0]))
cubes.append(Cube(-2, 4, -12, -10, -10, 10)) #prawa ograniczenie: -10
cubes.append(Cube(-2, 4, 12, 10, -10, 10)) #lewa ograniczenie: 10
cubes.append(Cube(-2, 4, 10, -10, -12, -10)) #tylnia ograniczenie: -10
cubes.append(Cube(-2, 4, 10, -10, 12, 10)) #przednia ograniczenie: 10
spheres.append(Sphere(v=[4, 0, 4], p=[-5, 3, 0], col=[1, 0, 0]))
spheres.append(Sphere(v=[-4, 0, -4], p=[5, 3, 0], col=[0, 0, 1]))
Boundings = [-10,10]

def mouseWheel(a, b, c, d):
    global distance
    distance += b

def myszka(x, y):
    global myszkax, myszkay
    myszkax = x
    myszkay = y
    print(myszkax, myszkay)
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


def chceckSphereToCubeCollision(sphere, cube):
    if sphere.p[1] - sphere.r < cube.up:
        sphere.v[1] = -sphere.s * sphere.v[1]
        sphere.p[1] += cube.up - (sphere.p[1] - sphere.r)

def check_sphere_to_cube_collision(sphere, cube):
    if sphere.p[0] - sphere.r < cube.left:
        sphere.v[0] = -sphere.s * sphere.v[0]
        sphere.p[0] += cube.left + (sphere.p[0] - sphere.r)

def check_sphere_to_sphere_collision(obj1, obj2):
    return abs((obj1.p[0] - obj2.p[0])**2 + (obj1.p[2] - obj2.p[2])**2) <= (obj1.r + obj2.r)**2

# def process_sphere_to_sphere_collision0(obj1, obj2):
#     pp = np.mean([obj1.p, obj2.p])
#     n = normalize(obj1.p - obj2.p)
#     if not (obj1.v - obj2.v) * n < 0:
#         n = normalize(obj2.p - obj1.p)
#
#         if abs(n[0]) <= abs(n[1]) and abs(n[0]) <= abs(n[2]): p = np.array([0, n[2], -n[1]])
#         if abs(n[1]) <= abs(n[0]) and abs(n[1]) <= abs(n[2]): p = np.array([-n[2], 0, n[0]])
#         if abs(n[2]) <= abs(n[0]) and abs(n[2]) <= abs(n[1]): p = np.array([n[1], -n[0], 0])
#         t = normalize(p)
#         k = np.cross(n, t)
#
#         a = np.eye(3)[0, :]
#         b = np.eye(3)[1, :]
#         c = np.eye(3)[2, :]
#         M = [n, t, k]
#         Ontk = M @ [a,b,c]
#         print(Ontk)

def process_sphere_to_sphere_collision(obj1, obj2):
    fDistance = np.sqrt((obj1.p[0] - obj2.p[0])**2 + (obj1.p[2] - obj2.p[2])**2)
    fOverlap = 0.5 * (fDistance - obj1.r - obj2.r)

    obj1.v[0] -= fOverlap * (obj1.p[0] - obj2.p[0]) / fDistance
    obj1.v[2] -= fOverlap * (obj1.p[2] - obj2.p[2]) / fDistance

    obj2.v[0] += fOverlap * (obj1.p[0] - obj2.p[0]) / fDistance
    obj2.v[2] += fOverlap * (obj1.p[2] - obj2.p[2]) / fDistance


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
    for cube in cubes:
        cube.draw()
    for sphere in spheres:
        for sphere2 in spheres:
            if sphere != sphere2:
                if check_sphere_to_sphere_collision(sphere, sphere2):
                    process_sphere_to_sphere_collision(sphere, sphere2)
                    continue
        chceckSphereToCubeCollision(sphere, cubes[0])
        check_sphere_to_cube_collision(sphere, cubes[1])
        sphere.update(0.2)
        sphere.draw()

    check_sphere_to_sphere_collision(spheres[0], spheres[1])
    # updateSphereCollision(sphere)


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
for sphere in spheres:
    sphere.quad = gluNewQuadric()
    gluQuadricNormals(sphere.quad, GLU_SMOOTH)
glutMainLoop()