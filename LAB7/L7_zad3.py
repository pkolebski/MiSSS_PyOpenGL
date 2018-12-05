from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import time, datetime

# obsługa myszki
myszkax = 400;
myszkay = 300;

def myszka(x, y):
    global myszkax, myszkay;
    myszkax = x;
    myszkay = y
    glutPostRedisplay(); # zaznacz, że okno wymaga przerysowania

def Figure3D(n, cmode, v, s, c):
    glBegin(GL_TRIANGLES)
    for i in range(n):      # tworzymy n ścian trójkątnych
        if(cmode):                    # tryb koloru
            glColor3fv(c[i])          # kolor wg numeru ściany
        for j in range(3):
            glVertex3fv(v[ s[i][j] ])

        else:                          # false - kolor wierzchołków
            for j in range(3):
                glColor3fv(c[ s[i][j] ]) # kolor wg numeru wierzchołka
                glVertex3fv(v[ s[i][j] ])

    glEnd()

def Cube():
    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    )
    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7)
    )
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def rysuj():
    t = datetime.datetime.now()
    t = t.microsecond/10000 * 3.6 #zmieniaj tylko zera

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); # czyszczenie sceny
    glLoadIdentity(); # resetowanie widoku

    glTranslatef(0.0, -2.0, -12.0) # przesunięcie widoku
    glRotatef(-400 + myszkax, 0.0, 1.0, 0.0); # obrót
    glRotatef(-300 + myszkay, 0.0, 1.0, 0.0); # obrót
    glRotatef(t, 0.0, 1.0, 0.0);  # obrót

    #Cube()

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
    c = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 1.0, 0.0],
    ])

    glTranslatef(0, 0, -1)
    for i in range(2):
        Figure3D(4,i,v,s,c)
        glTranslatef(2, 0, 0)


    glutSwapBuffers(); # zamiana buforów - wyświetlenie trójkątów i prostokąta

def program02():
    glutInit(sys.argv); # przekazanie argumentów z wiersza poleceń do GLUT
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);
    # kolory rgb, podwójne buforowanie, bufor głębokości

    glutInitWindowSize(800, 600);
    glutInitWindowPosition(300, 300);
    glutCreateWindow(b"Zadanie nr 2");

    glutDisplayFunc(rysuj);
    glutIdleFunc(rysuj);
    glutMotionFunc(myszka);

    glClearColor(0.0, 0.0, 0.0, 0.0);
    glClearDepth(1.0);
    glDepthFunc(GL_LESS); # parametr bufora głębokości
    glEnable(GL_DEPTH_TEST);
    glMatrixMode(GL_PROJECTION); # tryb projekcji
    glLoadIdentity(); # resetuj projekcję

    gluPerspective(50.0, float(800) / float(600), 0.1, 100.0)
        # rzutowanie perspektywiczne

    glMatrixMode(GL_MODELVIEW); # tryb widoku
    glutMainLoop();

rn = np.random.rand(6, 3)
theta = 2 * np.pi / 6
r2 = 1
vertexes = [((np.cos(theta * i) * r2) + 4, (np.sin(theta * i) * r2), 0) for i in range(6)]

program02();