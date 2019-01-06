from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
import numpy as np
from utils import Sphere, Cube, normalize
from Collision import chceckSphereToCubeCollision

tick = 0
myszkax = 429
myszkay = 418

which_ball = 0
hitting_angle = 0
power=0

distance = 30
cubes = []
spheres = []
cubes.append(Cube(0, 2, -10, 10, -10, 10, color=[0, 1, 0]))
cubes.append(Cube(-2, 4, -12, -10, -12, 12))  # prawa ograniczenie: -10
cubes.append(Cube(-2, 4, 12, 10, -12, 12))  # lewa ograniczenie: 10
cubes.append(Cube(-2, 4, 10, -10, -12, -10))  # tylnia ograniczenie: -10
cubes.append(Cube(-2, 4, 10, -10, 12, 10))  # przednia ograniczenie: 10
spheres.append(Sphere(v=[5, 0, 5], p=[-5, 3, -5], col=[1, 0, 0]))
spheres.append(Sphere(v=[2, 0, 4], p=[5, 3, 5], col=[0, 0, 1]))
spheres.append(Sphere(v=[7, 0, 5], p=[3, 3, 0], col=[1, 0, 0.5]))


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
    global sphere, Bat
    if key == b'+':
        sphere.s += 0.1
    if key == b'-':
        sphere.s -= 0.1
    if key == b',':
        sphere.gravity += 1
    if key == b'.':
        sphere.gravity -= 1
    if key == b't':
        sphere.v = [np.random.rand(1)*3,0,np.random.rand(1)*3]
    if key == b'q':
        global which_ball
        global hitting_angle
        global power
        which_ball += 1
        hitting_angle=0
    if key == b'f':
        hitting_angle += 0.1

        if hitting_angle>=6.27:
            hitting_angle=0
            power = 0
    if key == b'g':
        hitting_angle -= 0.1
        if hitting_angle<=0:
            hitting_angle=06.28
    if key ==b'p':
        power+=1
        if power>10:
            power=0
    if key == b'v':
        global chosen_sphere
        hit_ball(hitting_angle,power)


def check_sphere_to_sphere_collision(obj1, obj2):
    return abs((obj1.p[0] - obj2.p[0]) ** 2 + (obj1.p[2] - obj2.p[2]) ** 2) <= (obj1.r + obj2.r) ** 2

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

# def static_collision(obj1, obj2):
#     fDistance = np.sqrt((obj1.p[0] - obj2.p[0]) ** 2 + (obj1.p[2] - obj2.p[2]) ** 2)
#     fOverlap = 0.5 * (fDistance - obj1.r - obj2.r)
#
#     obj1.v[0] -= obj1.s * fOverlap * (obj1.p[0] - obj2.p[0]) / fDistance
#     obj1.v[2] -= obj1.s * fOverlap * (obj1.p[2] - obj2.p[2]) / fDistance
#
#     obj2.v[0] += obj2.s * fOverlap * (obj1.p[0] - obj2.p[0]) / fDistance
#     obj2.v[2] += obj2.s * fOverlap * (obj1.p[2] - obj2.p[2]) / fDistance

def dynamic_collision(obj1, obj2):
    # dystans pomiedzy kulkami
    fDistance = np.sqrt((obj1.p[0] - obj2.p[0]) ** 2 + (obj1.p[2] - obj2.p[2]) ** 2)

    # wektory normalne
    nx = (obj1.p[0] - obj2.p[0]) / fDistance
    nz = (obj1.p[2] - obj2.p[2]) / fDistance

    # wektory t
    tx = -nz
    tz = nx

    # dot product t
    dpTan1 = obj1.v[0] * tx + obj1.v[2] * tz
    dpTan2 = obj2.v[0] * tx + obj2.v[2] * tz

    # dot product normal
    dpNorm1 = obj1.v[0] * nx + obj1.v[2] * nz
    dpNorm2 = obj2.v[0] * nx + obj2.v[2] * nz

    # conservation of momentum
    m1 = (dpNorm1 * (obj1.m - obj2.m) + 1.5 * obj2.m * dpNorm2) / (obj1.m + obj2.m)
    m2 = (dpNorm2 * (obj2.m - obj1.m) + 1.5 * obj1.m * dpNorm1) / (obj1.m + obj2.m)

    obj1.v[0] = obj1.s * tx * dpTan1 + nx * m1
    obj1.v[2] = obj1.s * tz * dpTan1 + nz * m1
    obj2.v[0] = obj1.s * tx * dpTan2 + nx * m2
    obj2.v[2] = obj1.s * tz * dpTan2 + nz * m2


def cue_hit(angle):
    return [cos(angle%6.24), 0, sin(angle%6.24) ]

def hit_ball(angle,pow):
    hit = cue_hit(angle)
    hit[0] *=pow
    hit[2] *=pow
    spheres[which_ball%3].v += hit

def Bat_update(bat, angle):
    temp = cue_hit(angle)
    bat.left = bat.left * temp[0]
    bat.right = bat.right * temp[0]
    bat.back = bat.back * temp[2]
    bat.front = bat.front * temp[2]

# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick
    ltime = time.clock()
    if ltime < tick + 0.1:  # max 10 ramek / s
        return False
    tick = ltime
    return True

# pętla wyświetlająca
def display():
    global sphere, myszkax, myszkay, distance,hitting_angle,which_ball,power
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
    fill = False
    i=1
    for sphere in spheres:
        sphere.update(0.2, cubes[0].down)
        chceckSphereToCubeCollision(sphere, cubes[0])
        for sphere2 in spheres:
            if sphere != sphere2:
                if check_sphere_to_sphere_collision(sphere, sphere2):
                    dynamic_collision(sphere, sphere2)

        sphere.col = sphere.orginal_col
        spheres[which_ball % 3].col = np.random.rand(3)

        Cs = spheres[which_ball % 3].p
        Bat = Cube(0,1,100,100,100,100, color=[0, 0, 0], fill=fill)
        Bat.draw()

        if abs(spheres[which_ball % 3].v[0]) <= 0.1  or abs(spheres[which_ball % 3].v[2]) <= 0.1:
            i+=1

        if abs(spheres[which_ball % 3].v[0]) <= 0.1 and i > 2 or abs(spheres[which_ball % 3].v[2]) <= 0.1 and i >2:
            fill = True
            Bat = Cube(Cs[1], Cs[1] + 1, Cs[0] - 0.5, Cs[0] + 0.5, Cs[2] + 7, Cs[2] + 1, color=[0, 0, 0], fill=fill)
            Bat_update(Bat, hitting_angle)
            Bat.draw()

        elif abs(spheres[which_ball % 3].v[0]) > 0.1 or abs(spheres[which_ball % 3].v[2]) > 0.1:
            fill = False
            i=1

        print(hitting_angle, power)
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
for sphere in spheres:
    sphere.quad = gluNewQuadric()
    gluQuadricNormals(sphere.quad, GLU_SMOOTH)

glutMainLoop()
