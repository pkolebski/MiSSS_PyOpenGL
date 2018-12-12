import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def Figure3D(n, cmode, v, s, c, scale):
    v = v * scale
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

def Polygon(L, n):
    for j in range(n):
        x = np.sin(j / n * 2 * np.pi)*L
        y = np.cos(j / n * 2 * np.pi)*L
        glVertex3f(x, y, 0.0)

def Cube(scale, color):
    vertices = np.array([
        [0.5, -0.5, -0.5],
        [0.5, 0.5, -0.5],
        [-0.5, 0.5, -0.5],
        [-0.5, -0.5, -0.5],
        [0.5, -0.5, 0.5],
        [0.5, 0.5, 0.5],
        [-0.5, -0.5, 0.5],
        [-0.5, 0.5, 0.5]]
    )
    edges = np.array([
        [0,1,2,3],
        [4,5,7,6],
        [0,1,5,4],
        [2,3,6,7],
        [0,3,6,4],
        [1,2,7,5]
        ])

    for i in range(6):
        glBegin(GL_POLYGON)
        glColor3fv(color[i])
        for j in range(4):
            glVertex3fv(vertices[edges[i, j]])
        glEnd()
    # edges = np.array([
    #     [0, 1],
    #     [0, 3],
    #     [0, 4],
    #     [2, 1],
    #     [2, 3],
    #     [2, 7],
    #     [6, 3],
    #     [6, 4],
    #     [6, 7],
    #     [5, 1],
    #     [5, 4],
    #     [5, 7]]
    # )
    # vertices *= scale
    # glBegin(GL_LINES)
    # for edge in edges:
    #     for vertex in edge:
    #         glVertex3fv(vertices[vertex])
    # glEnd()