from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import time

# obsługa myszki
myszkax = 400;
myszkay = 300;

def myszka(x, y):
    global myszkax, myszkay;
    myszkax = x;
    myszkay = y
    glutPostRedisplay(); # zaznacz, że okno wymaga przerysowania

def rysuj():
    t = time.time()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); # czyszczenie sceny
    glLoadIdentity(); # resetowanie widoku

    glTranslatef(0, 0, np.sin(t))

    glTranslatef(-4.0, -2.0, -12.0) # przesunięcie widoku
    glRotatef(-400 + myszkax, 0.0, 1.0, 0.0); # obrót
    glRotatef(-300 + myszkay, 0.0, 1.0, 0.0); # obrót

    glBegin(GL_POLYGON)  # rysowanie trójkąta
    for i in range(6):
        glColor3f(rn[i, 0], rn[i, 1], rn[i, 2])
        glVertex3f(vertexes[i][0], vertexes[i][1], vertexes[i][2])
    glEnd()

    glColor3f(1.0, 0.5, 0.5) # kolor
    glBegin(GL_POLYGON) # rysowanie trójkąta
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(1.205, -1.0, 0.0)
    glVertex3f(-1.205, -1.0, 0.0)
    glEnd() # koniec rysowania trójkąta

    glColor3f(0.0, 0.5, 0.5);
    glTranslatef(2.0, 2.0, 2.0) # przesunięcie widoku
    glBegin(GL_POLYGON) # rysowanie trójkąta
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(1.205, -1.0, 0.0)
    glVertex3f(-1.205, -1.0, 0.0)
    glEnd() # koniec rysowania trójkąta

    glColor3f(1.0, 1.5, 0.5);
    glTranslatef(2.0, 2.0, 2.0) # przesunięcie widoku
    glBegin(GL_POLYGON) # rysowanie trójkąta
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(1.205, -1.0, 0.0)
    glVertex3f(-1.205, -1.0, 0.0)
    glEnd() # koniec rysowania trójkąta

    glColor3f(1.0, 0.5, 1.0);
    glTranslatef(3.0, -2.0, 0.0) # przesunięcie widoku
    glBegin(GL_QUADS) # rysowanie prostokąta
    glVertex3f(-1.0, 1.0, 0.0);
    glVertex3f(1.0, 1.0, 0.0);
    glVertex3f(1.0, -1.0, 0.0);
    glVertex3f(-1.0, -1.0, 0.0);
    glEnd() # koniec rysowania prostokąta

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

    glClearColor(0.0, 1.0, 1.0, 1.0);
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