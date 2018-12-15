from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time

# licznik czasu - do wymuszenia częstotliwości odświeżania
tick = 0

# klasa pomocnicza, pozwalająca na odwoływanie się do słowników przez notację kropkową
class dd(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
# dwa obszary ograniczające o punktach skrajnych p1 i p3
aabb1 = {"p1":[-2.0, -4.0], "p3":[2.0, 4.0]}
aabb1 = dd(aabb1)
aabb2 = {"p1":[-6.0, -1.0], "p3":[-4.0, 1.0]}
aabb2 = dd(aabb2)
aabb3 = {"p1":[-6.0, -1.0], "p3":[-4.0, 1.0]}
aabb3 = dd(aabb3)
speed = 0.1

def keyboard(key, x, y):
    global aabb3, speed
    ch = key.decode("utf-8")
    if ch == 'w':
        aabb3.p1[1] += speed
        aabb3.p3[1] += speed
    elif ch == 's':
        aabb3.p1[1] -= speed
        aabb3.p3[1] -= speed
    elif ch == 'a':
        aabb3.p1[0] -= speed
        aabb3.p3[0] -= speed
    elif ch == 'd':
        aabb3.p1[0] += speed
        aabb3.p3[0] += speed

# funkcja rysująca jeden obszar ograniczający AABB w 2d
def dAABB2f(p1, p3, col):
    p2 = p1[:]
    p2[0] = p3[0]
    p4 = p1[:]
    p4[1] = p3[1]
    glColor3fv(col)
    glBegin(GL_POLYGON)
    glVertex2fv(p1)
    glVertex2fv(p2)
    glVertex2fv(p3)
    glVertex2fv(p4)
    glEnd()
    pass

# funkcja sprawdzająca warunki zachodzenia na siebie dwóch AABB
def ccAABBtoAABB(p1, p3, q1, q3):
    if (p3[0] < q1[0] or p1[0] > q3[0]): return 0
    if (p3[1] < q1[1] or p1[1] > q3[1]): return 0
    return 1

# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick
    ltime = time.clock()
    if (ltime < tick + 0.1): # max 10 ramek / s
        return False
    tick = ltime
    return True

# pętla wyświetlająca
def display():
    if not cupdate():
        return
    
    global aabb1, aabb2
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    aabb2.p1[0] += 0.1
    aabb2.p3[0] += 0.1
    if (aabb2.p1[0] > 4.0):
        aabb2.p1[0] = -6.0
        aabb2.p3[0] = -4.0
    dAABB2f(aabb3.p1, aabb3.p3, [0.5, 0.2, 0.3])
    dAABB2f(aabb2.p1, aabb2.p3, [0, 0.8, 0])
    dAABB2f(aabb1.p1, aabb1.p3, [0, 0.5, 0.5])
    
    txt = "-"
    if ccAABBtoAABB(aabb1.p1, aabb1.p3, aabb2.p1, aabb2.p3):
        txt += "aabb1 x aabb2, "
    if ccAABBtoAABB(aabb3.p1, aabb3.p3, aabb2.p1, aabb2.p3):
        txt += "aabb3 x aabb2, "
    if ccAABBtoAABB(aabb1.p1, aabb1.p3, aabb3.p1, aabb3.p3):
        txt += "aabb1 x aabb3, "
    txt += "\n"
    sys.stdout.write(txt)
    
    glFlush()
    
glutInit()
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Kolizje 01")
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(keyboard)

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
