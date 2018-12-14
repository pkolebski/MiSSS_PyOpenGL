from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
# licznik czasu - do wymuszenia częstotliwości odświeżania
tick = 0
speed = 0.1

class AABB(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p3 = p2

# dwa obszary ograniczające o punktach skrajnych p1 i p3
aabb1 = AABB([-2.0, -4.0], [2.0, 4.0])

aabb2 = AABB([-6.0, -1.0], [-4.0, 1.0])

aabb3 = AABB([-6.0, 6.0], [-3.0, 3.0])


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
def ccAABBtoAABB(box1, box2):
    if box1.p3[0] < box2.p1[0] or box1.p1[0] > box2.p3[0]:
        return 0
    if box1.p3[1] < box2.p1[1] or box1.p1[1] > box2.p3[1]:
        return 0
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

    global aabb1, aabb2, aabb3
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    aabb2.p1[0] += 0.1; aabb2.p3[0] += 0.1
    if aabb2.p1[0] > 4.0:
        aabb2.p1[0] = -6.0
        aabb2.p3[0] = -4.0
    dAABB2f(aabb3.p1, aabb3.p3, [0.5, 0.1, 0.5])
    dAABB2f(aabb2.p1, aabb2.p3, [0, 0.8, 0])
    dAABB2f(aabb1.p1, aabb1.p3, [0.5, 0.5, 0.5])
    txt = ''
    if ccAABBtoAABB(aabb1, aabb2):
        txt += "1x2, "
    if ccAABBtoAABB(aabb2, aabb3):
        txt += "2x3, "
    if ccAABBtoAABB(aabb1, aabb3):
        txt += "1x3, "

    sys.stdout.write(txt + '\n')

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