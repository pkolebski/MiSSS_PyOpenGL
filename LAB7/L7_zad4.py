from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np

bound = 1

# zmień teksturę
def keypress(key, x, y):
    global bound
    bound = 1 - bound
    glBindTexture(GL_TEXTURE_2D, bound)

def create_triangles(p,a, b, c):
    glTexCoord2f(0.5, 0.0)
    glVertex3fv(p[a])
    glTexCoord2f(0.0, 1.0)
    glVertex3fv(p[b])
    glTexCoord2f(1.0, 1.0)
    glVertex3fv(p[c])


def Polygon():

    t = (1.0 + np.sqrt(5.0)) / 2.0

    punkts = [
     [-1, t, 0],
     [1, t, 0],
     [-1, -t, 0],
     [1, -t, 0],
     [0, -1, t],
     [0, 1, t],
     [0, -1, -t],
     [0, 1, -t],
     [t, 0, -1],
     [t, 0, 1],
     [-t, 0, -1],
     [-t, 0, 1]
     ]
    glBegin(GL_TRIANGLES)
    create_triangles(punkts, 0, 11, 5)
    create_triangles(punkts,0, 5, 1)
    create_triangles(punkts,0, 1, 7)
    create_triangles(punkts,0, 7, 10)
    create_triangles(punkts,0, 10, 11)

    create_triangles(punkts,1, 5, 9)
    create_triangles(punkts,5, 11, 4)
    create_triangles(punkts,11, 10, 2)
    create_triangles(punkts,10, 7, 6)
    create_triangles(punkts,7, 1, 8)

    create_triangles(punkts,3, 9, 4)
    create_triangles(punkts,3, 4, 2)
    create_triangles(punkts,3, 2, 6)
    create_triangles(punkts,3, 6, 8)
    create_triangles(punkts,3, 8, 9)

    create_triangles(punkts,4, 9, 5)
    create_triangles(punkts,2, 4, 11)
    create_triangles(punkts,6, 2, 10)
    create_triangles(punkts,8, 6, 7)
    create_triangles(punkts,9, 8, 1)
    glEnd()

# pętla wyświetlająca
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    Polygon()

    glutSwapBuffers()

glutInit(sys.argv)
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Tekstury")
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(keypress)
glClearColor(1.0, 1.0, 1.0, 1.0)
glClearDepth(1.0)
glDepthFunc(GL_LESS)
glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)

# przygotuj tekstury
glBindTexture(GL_TEXTURE_2D, 0)
image = Image.open("tekstura1.bmp")
width = image.size[0]
height = image.size[1]
image = image.tobytes("raw", "RGBX", 0, -1)
glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

glBindTexture(GL_TEXTURE_2D, 1)
image = Image.open("tekstura2.bmp")
width = image.size[0]
height = image.size[1]
image = image.tobytes("raw", "RGBX", 0, -1)
glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

# ustaw projekcję ortograficzną
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-10, 10, -10, 10, 15, 20)
gluLookAt(0.0, 0.0, 15.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
glMatrixMode(GL_MODELVIEW)

glutMainLoop()