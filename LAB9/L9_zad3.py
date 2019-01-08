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
power = 10
i=1
XD = [0, 0, 0]
stick_start_pos = None
juzniewiemjaknazywaczmienne = 3

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
    distance -= b

def myszka(x, y):
    global myszkax, myszkay
    myszkax = x
    myszkay = y
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

        if hitting_angle >= np.pi:
            hitting_angle = -np.pi
            power = 0
    if key == b'g':
        hitting_angle -= 0.1
        if hitting_angle <= -np.pi:
            hitting_angle = np.pi
    if key ==b'p':
        power+=1
        if power>10:
            power=0
    if key == b'v':
        global chosen_sphere, stick_start_pos, juzniewiemjaknazywaczmienne
        stick_start_pos = spheres[which_ball % 3].p
        # hit_ball(hitting_angle,power)
        juzniewiemjaknazywaczmienne = 2.9


def check_sphere_to_sphere_collision(obj1, obj2):
    return abs((obj1.p[0] - obj2.p[0]) ** 2 + (obj1.p[2] - obj2.p[2]) ** 2) <= (obj1.r + obj2.r) ** 2


def dynamic_collision(obj1, obj2, dt):
    obj1.p -= dt * obj1.v
    obj2.p -= dt * obj2.v
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
    m1 = (dpNorm1 * (obj1.m - obj2.m) + 1. * obj2.m * dpNorm2) / (obj1.m + obj2.m)
    m2 = (dpNorm2 * (obj2.m - obj1.m) + 1. * obj1.m * dpNorm1) / (obj1.m + obj2.m)

    obj1.v[0] = obj1.s * tx * dpTan1 + nx * m1
    obj1.v[2] = obj1.s * tz * dpTan1 + nz * m1
    obj2.v[0] = obj1.s * tx * dpTan2 + nx * m2
    obj2.v[2] = obj1.s * tz * dpTan2 + nz * m2


def cue_hit(angle):
    global XD
    XD = [cos(angle), 0, sin(angle)]
    return XD

def hit_ball(angle, pow):
    hit = cue_hit(angle)
    hit[0] *= pow
    hit[2] *= pow
    spheres[which_ball % 3].v += hit

def Bat_update(bat, angle):
    temp = cue_hit(angle)
    bat.left = bat.left * temp[0]
    bat.right = bat.right * temp[0]
    bat.back = bat.back * temp[2]
    bat.front = bat.front * temp[2]

def cupdate():
    global tick
    ltime = time.clock()
    if ltime < tick + 0.1:  # max 10 ramek / s
        return False
    tick = ltime
    return True

def stick_move(bat, bat_end):
    global stick_start_pos, juzniewiemjaknazywaczmienne
    cs = spheres[which_ball % 3].p
    if juzniewiemjaknazywaczmienne > 0:
        juzniewiemjaknazywaczmienne -= 0.4
        bat = Cube(bat.down, bat.up, bat.left, bat.right, bat.back - juzniewiemjaknazywaczmienne, bat.front - juzniewiemjaknazywaczmienne, color=bat.color)

        bat_end.p -= [juzniewiemjaknazywaczmienne, 0, 0]
    else:
        hit_ball(hitting_angle, power)
        juzniewiemjaknazywaczmienne = 3
        stick_start_pos = None
    return bat, bat_end


def display():
    global sphere, myszkax, myszkay, distance, hitting_angle, which_ball, power, i, stick_start_pos
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
        sphere.update(0.2, cubes[0].up)
        chceckSphereToCubeCollision(sphere, cubes[0])
        for sphere2 in spheres:
            if sphere != sphere2:
                if check_sphere_to_sphere_collision(sphere, sphere2):
                    # dynamic_collision(sphere, sphere2, 0.2)
                    sphere_to_sphere_collision(sphere, sphere2, 0.2)

        sphere.col = sphere.orginal_col
        spheres[which_ball % 3].col = [1, 1, 1]



        print(hitting_angle, power)
        sphere.draw()
    cue_hit(hitting_angle)
    global XD, stick_start_pos, juzniewiemjaknazywaczmienne
    Cs = spheres[which_ball % 3].p

    Bat = Cube(Cs[1], Cs[1] + 1, Cs[2] - 0.5, Cs[2] + 0.5, Cs[0] - 7, Cs[0] - 2, color=[0, 0, 0], fill=True)
    bat_end = Sphere(p=Cs + [-2, 0.5, 0], r=0.8)
    bat_end.quad = gluNewQuadric()
    gluQuadricNormals(bat_end.quad, GLU_SMOOTH)
    if juzniewiemjaknazywaczmienne != 3:
        Bat, bat_end = stick_move(Bat, bat_end)
    Bat.draw(np.rad2deg(-hitting_angle), Cs)
    bat_end.draw(np.rad2deg(-hitting_angle), Cs)

    glutSwapBuffers()
    # glFlush()

def sphere_to_sphere_collision(sphere1, sphere2, dt):
    sphere1.p -= dt * sphere1.v
    sphere2.p -= dt * sphere2.v

    # n = np.array([sphere2.p[0] - sphere1.p[0], sphere2.p[1] - sphere1.p[1], sphere2.p[2] - sphere1.p[2]])
    n = sphere2.p - sphere1.p
    # if np.linalg.norm((sphere1.v - sphere2.v) * n) < 0:
    #     print('wybrane')
    # else:
    #     n = sphere1.p - sphere2.p
    #     print('XD2')
    if np.abs(n[0]) <= np.abs(n[1]) and np.abs(n[0]) <= np.abs(n[2]):
        t = np.array([0, n[2], -n[1]])
    elif np.abs(n[1]) <= np.abs(n[0]) and np.abs(n[1]) <= np.abs(n[2]):
        t = np.array([-n[2], 0, n[0]])
    elif np.abs(n[2]) <= np.abs(n[0]) and np.abs(n[2]) <= np.abs(n[1]):
        t = np.array([n[1], -n[0], 0])
    k = np.cross(n, t)
    P = normalize(np.array([n, t, k])) * [1, 1, -1]

    u1 = P @ np.array(sphere1.v)
    u2 = P @ np.array(sphere2.v)

    I_n = (sphere1.m * sphere2.m * (u2[0] - u1[0]) * (1 + sphere1.s)) / (sphere1.m + sphere2.m)

    v1 = [(I_n + sphere1.m * u1[0]) / sphere1.m, u1[1], u1[2]]
    v2 = [(-I_n + sphere2.m * u2[0]) / sphere2.m, u2[1], u2[2]]

    sphere1.v = v1 @ np.linalg.inv(P)
    sphere2.v = v2 @ np.linalg.inv(P)

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
