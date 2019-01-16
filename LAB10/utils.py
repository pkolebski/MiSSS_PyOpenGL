import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *



def normalize(vec):
    return vec / np.linalg.norm(vec)


class Figure:
    def __init__(self, points=None, links=None, color=[1, 1, 1], fill=True):
        self.vertices = 3*np.array([
            [7, -10, -10],
            [15, 10, -10],
            [-10, 10, -10],
            [-10, -10, -10],
            [7, -10, 10],
            [15, 10, 10],
            [-10, -10, 10],
            [-10, 10, 10]]
        ) if points is None else points
        self.links = np.array([
            [0, 1, 2, 3],
            [4, 5, 7, 6],
            [0, 1, 5, 4],
            [2, 3, 6, 7],
            [0, 3, 6, 4],
            [1, 2, 7, 5]
        ]) if links is None else links
        self.color = color
        self.fill = fill

    def check_collisions(self, obj):
        for link in obj.links:
            for point in self.vertices:
                if distance_point_wall(point, obj.vertices[link]) < 0.4:
                    print("kolizja")

    def draw(self):
        glLoadIdentity()
        glColor3fv(self.color)
        if not self.fill: glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for link in self.links:
            glBegin(GL_POLYGON)
            for i in range(len(link)):
                glVertex3fv(self.vertices[link[i]])
            glEnd()
        if not self.fill: glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def calculate_r(self, alpha, beta, gamma):
        return np.array(
            [[np.cos(beta) * np.cos(gamma),                                                 -np.cos(beta) * np.sin(gamma),                                                 np.sin(beta)             ],
             [np.sin(alpha) * np.sin(beta) + np.cos(alpha) * np.sin(gamma),                  -np.sin(alpha) * np.sin(beta) * np.sin(gamma) + np.cos(alpha) * np.cos(gamma), -np.sin(alpha) * np.cos(beta)],
             [-np.cos(alpha) * np.sin(beta) * np.cos(gamma) + np.sin(alpha) * np.sin(gamma), np.cos(alpha) * np.sin(beta) * np.sin(gamma) + np.sin(alpha) * np.cos(gamma),  np.cos(alpha) * np.cos(beta)]
             ], dtype=np.float32)


class Scene(Figure):
    pass


class Tetrahedron(Figure):
    def __init__(self, acceleration=[1,1,1], v=[0, 0, 0], points=None, links=None, mass=3, color=[1, 1, 0.5], fill=True):
        vertices = np.array([
            [5, 5, 0],
            [-5, 5, 0],
            [0, -3, 0],
            [0, 0, 5],
        ], dtype=np.float32) if points is None else points

        links = np.array([
            [0, 1, 2],
            [1, 3, 2],
            [3, 0, 2],
            [0, 3, 1],
        ]) if links is None else links
        super().__init__(vertices, links, color=color, fill=fill)
        self.mass = mass
        self.mass_center = np.mean(self.vertices)
        self.acceleration = np.array(acceleration, dtype=np.float32)
        self.linear_velocity = np.array(v, dtype=np.float32)
        self.angular_velocity = np.array([0.5, 0.1, 0.4], dtype=np.float32)
        self.r = np.mean(self.vertices[0:3])
        self.h = distance_point_wall(self.vertices[-1, :], self.vertices[:3, :])
        self.p = self.vertices
        self.momentum = self.mass * self.linear_velocity
        self.O = np.array([0, 0, 0], dtype=np.float32)
        self.s = 0.9
        self.inertia_tensor = [
            [0.6 * self.mass * self.h ** 2 + 0.15 * self.mass * self.r ** 2, 0, 0],
            [0, 0.6 * self.mass * self.h ** 2 + 0.15 * self.mass * self.r ** 2, 0],
            [0, 0, 0.3 * self.mass * self.r ** 2]
        ]

        self.W_matrix=[
            [0, -self.angular_velocity[2], self.angular_velocity[1]],
            [self.angular_velocity[2], 0, -self.angular_velocity[0]],
            [-self.angular_velocity[1],self.angular_velocity[0], 0 ]
        ]

    def update(self, dt):
        self.oldvelocity = self.linear_velocity
        self.oldO=self.O
        self.linear_velocity += dt * self.acceleration
        self.p = self.p @ self.calculate_r(*self.angular_velocity)
        self.p += dt * self.linear_velocity
        self.vertices = self.p
        self.mass_center = np.mean(self.vertices)
        self.momentum = self.mass * self.linear_velocity


        self.netforce = 3 * (self.mass/1000*(self.oldvelocity-self.linear_velocity)*dt)
        self.O = np.sum([self.netforce*(vertice-self.mass_center) for vertice in self.vertices ])
        self.H = (self.oldO-self.O)*dt
        self.J = self.calculate_r(*self.angular_velocity)@self.inertia_tensor@np.transpose(self.calculate_r(*self.angular_velocity))
        self.w = np.linalg.inv(self.J) * self.H

    def sphere_to_sphere_collision(self, wall, dt):
        wallM = 1e10
        self.p -= dt * self.v
        normWall = np.cross(wall[0] - wall[1], wall[1] - wall[2])
        u = normWall @ wall[0]

        temp = ((u - normWall[0]*self.p[0] - normWall[1]*self.p[1] - normWall[2]*self.p[2] ) / np.sum(normWall**2))
        x0 = self.p[0] + normWall[0] * temp
        x1 = self.p[1] + normWall[1] * temp
        x2 = self.p[2] + normWall[2] * temp
        crossingPoint = np.array([x0, x1, x2])

        n = crossingPoint - self.p
        if np.abs(n[0]) <= np.abs(n[1]) and np.abs(n[0]) <= np.abs(n[2]):
            t = np.array([0, n[2], -n[1]])
        elif np.abs(n[1]) <= np.abs(n[0]) and np.abs(n[1]) <= np.abs(n[2]):
            t = np.array([-n[2], 0, n[0]])
        elif np.abs(n[2]) <= np.abs(n[0]) and np.abs(n[2]) <= np.abs(n[1]):
            t = np.array([n[1], -n[0], 0])
        k = np.cross(n, t)

        me = (self.p + crossingPoint) / 2

        M = normalize(np.array([n, t, k])) * [1, 1, -1]

        v_ntk1 = M @ np.array(self.v)
        v_ntk2 = np.zeros(3)

        G = M @ self.inertia_tensor @ np.transpose(M)
        m_ = 1/self.mass
        Q1 = np.linalg.inv(self.inertia_tensor)

        r = crossingPoint - self.mass_center
        r_ntk = M @ r
        w_ntk = M @ self.angular_velocity
        Zt = v_ntk1[1] + r_ntk[0]*w_ntk[2] - r_ntk[2]*w_ntk[0]
        Zk = v_ntk1[2] - r_ntk[0]*w_ntk[1] + r_ntk[1]*w_ntk[0]
        At = (Zt*zkk - Zk*zkt) / ztt*zkk - ztk*zkt
        Bt = -(znt*zkk - znk*zkt) / (ztt*zkk - ztk*zkt)
        Ak = (Zk*ztt - Zt*ztk) / (zkk*ztt - zkt*ztk)
        Bk = -(znk*ztt - znt*ztk) / (zkk*ztt - zkt*ztk)
        A1 = np.array([
            -r_ntk[2]*At + r_ntk[1]*Ak,
            -r_ntk[0]*Ak,
            r_ntk[0]*At
        ])
        B1 = np.array([
            -r_ntk[2] * Bt + r_ntk[1] * Bk,
            r_ntk[2] - r_ntk[0]*Bk,
            -r_ntk[1] + r_ntk[0]*Bt
        ])
        P_n = (self.s + 1) * ((v_ntk2[0] - v_ntk1[0] - r_ntk[2]*w_ntk[1] + r_ntk[1]*w_ntk[2] - (r_ntk[2]*Q1[1,:]@A1 - r_ntk[1]*Q1[2,:]@A1)) / (m_ + r_ntk[2]*Q[1,:]@B1 - r_ntk[1]*Q1[2,:]@B1))

        v1 = [(I_n + self.m * v_ntk1[0]) / self.m, v_ntk1[1], v_ntk1[2]]
        v2 = [(-I_n + wallM * v_ntk2[0]) / wallM, v_ntk2[1], v_ntk2[2]]

        self.v = v1 @ np.linalg.inv(M)
        wall.v = v2 @ np.linalg.inv(M)

def distance_point_wall(point, wall):
    a, b, c = np.cross(wall[0] - wall[1], wall[1] - wall[2])
    return np.abs(a * (point[0] - wall[0, 0]) + b * (point[1] - wall[0, 1]) + c * (point[2] - wall[0, 2]))
