from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import time, datetime
from utils import Cube, Polygon, Figure3D

color = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 1.0, 0.0],
    ])

st = True
ct = True
old_st = 0
t_size = [1, 1, 1]
k_size = [1, 1, 1]

def keyboard(key, x, y):
    global color, k_size, t_size, rotation_mode
    global st, ct
    ch = key.decode("utf-8")

    if ch == chr(27):
        print("elÓWA")
        sys.exit()
    if ch == 'c':
        color = np.random.rand(4, 3)
        print(color)
    if ch == 's':
        st = not st
    if ch == 't':
        ct = not ct
    if ch == 'z':
        k_size = np.random.rand(3) * 3
    if ch == 'x':
        t_size = np.random.rand(3) * 3

def reset_view():
    glLoadIdentity()
    glTranslatef(0.0, -2.0, -12.0)

def rysuj():
    global t, t2
    if st:
        t += 1
    if ct:
        t2 += 1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # czyszczenie sceny
    reset_view()

    glRotatef(t % 360, 0.0, 1.0, 0.0)  # obrót
    glTranslatef(-2, 0, 1)
    Cube(k_size)
    reset_view()
    glRotatef(t2 % 360, 0.0, 1.0, 0.0)  # obrót
    glTranslatef(4, 0, -2)
    Figure3D(4, 1, v, s, color, t_size)


    glutSwapBuffers(); # zamiana buforów - wyświetlenie trójkątów i prostokąta

def program02():
    glutInit(sys.argv); # przekazanie argumentów z wiersza poleceń do GLUT
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);
    # kolory rgb, podwójne buforowanie, bufor głębokości

    glutInitWindowSize(800, 600);
    glutInitWindowPosition(300, 300)
    glutCreateWindow(b"Zadanie nr 2")

    glutDisplayFunc(rysuj)
    glutIdleFunc(rysuj)
    glutKeyboardFunc(keyboard)

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS) # parametr bufora głębokości
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION) # tryb projekcji
    glLoadIdentity() # resetuj projekcję

    gluPerspective(50.0, float(800) / float(600), 0.1, 100.0)
        # rzutowanie perspektywiczne

    glMatrixMode(GL_MODELVIEW) # tryb widoku
    glutMainLoop()

v = np.array([              #wierzchołki
        [0.5, -0.5, 0.5],
        [-0.5, 0.5, 0.5],
        [0.5, 0.5, -0.5],
        [-0.5, -0.5, -0.5],
    ])
s = np.array([
        [0, 1, 2],
        [1, 3, 2],
        [3, 0, 2],
        [0, 3, 1],
    ])

rotation_mode = 1
t, t2 = 0, 0

rn = np.random.rand(6, 3)
theta = 2 * np.pi / 6
r2 = 1
vertexes = [((np.cos(theta * i) * r2) + 4, (np.sin(theta * i) * r2), 0) for i in range(6)]

program02()