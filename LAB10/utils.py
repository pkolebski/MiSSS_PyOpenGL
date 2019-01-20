import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *



def normalize(vec):
    return vec / np.linalg.norm(vec)


class Figure:
    def __init__(self, points=None, links=None, color=[1, 1, 1], fill=True):
        self.vertices = 2 * np.array([
            [7, -10, -10],
            [15, 10, -10],
            [-10, 10, -10],
            [-10, -10, -10],
            [7, -10, 10],
            [15, 10, 10],
            [-10, -10, 10],
            [-10, 10, 10]], dtype=np.float32
        ) if points is None else points
        self.links = np.array([
            [0, 1, 2, 3],
            [4, 5, 7, 6],
            [0, 1, 5, 4],
            [2, 3, 6, 7],
            [0, 3, 6, 4],
            [1, 2, 7, 5]]
        ) if links is None else links
        self.color = color
        self.fill = fill

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

    def calculate_r2(self, alfa, beta, gamma):
        return np.array(
            [[np.cos(beta) * np.cos(gamma),
              -np.cos(beta) * np.sin(gamma),
              np.sin(beta)],

             [np.sin(alfa) * np.sin(beta) * np.cos(gamma) + np.cos(alfa) * np.sin(gamma)
                 , -np.sin(alfa) * np.sin(beta) * np.sin(gamma) + np.cos(alfa) * np.cos(gamma)
                 , -np.sin(alfa) * np.cos(beta)],

             [-np.cos(alfa) * np.sin(beta) * np.cos(gamma) + np.sin(alfa) + np.sin(gamma)
                 , np.cos(alfa) * np.sin(beta) * np.sin(gamma) + np.sin(alfa) * np.cos(gamma),
              np.cos(alfa) * np.cos(beta)]])

class Scene(Figure):
    pass


class Tetrahedron(Figure):
    def __init__(self, acceleration=[0,0,0], v=[1,1,1], points=None, links=None, mass=3, color=[1, 1, 0.5], fill=True):
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
        self.angular_velocity = np.array([0,1,0], dtype=np.float32)
        self.r = np.mean(self.vertices[0:3])
        self.h = distance_point_wall(self.vertices[-1, :], self.vertices[:3, :])
        self.p = self.vertices
        self.momentum = self.mass * self.linear_velocity
        self.O = np.array([0, 0, 0], dtype=np.float32)
        self.s = 0.9
        self.u = 0.2
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
        self.oldR = np.eye(3)

    def update(self, dt):
        self.W_matrix = [
            [0, -self.angular_velocity[2], self.angular_velocity[1]],
            [self.angular_velocity[2], 0, -self.angular_velocity[0]],
            [-self.angular_velocity[1], self.angular_velocity[0], 0]
        ]
        self.gravity(dt)
        self.oldvelocity = self.linear_velocity
        self.oldO = self.O
        # self.linear_velocity += dt * self.acceleration
        self.p = self.vertices
        self.mass_center = np.mean(self.p, 0)
        self.p -= self.mass_center
        R =  self.gram_schmidt(self.calculate_r2(*self.angular_velocity * dt))

        for i in range(len(self.p)):
            self.p[i, :] = R @ self.p[i, :]
        self.p += self.mass_center
        print(self.angular_velocity)
        self.p += dt * self.linear_velocity
        self.vertices = self.p
        self.momentum = self.mass * self.linear_velocity


        # self.netforce = 3 * (self.mass/1000*(self.oldvelocity-self.linear_velocity)*dt)
        # self.O = np.sum([self.netforce*(vertice-self.mass_center) for vertice in self.vertices ])
        # self.H = (self.oldO-self.O)*dt
        self.J = R @ self.inertia_tensor @ np.transpose(R)
        # self.angular_velocity = np.linalg.inv(self.J) @ self.H

    def gravity(self, dt):
        self.linear_velocity -= np.array([0, (dt * 0.9), 0])

    def gram_schmidt(self, R):
        u1 = normalize(R[0])
        y = R[1] - np.dot(R[1], u1) * u1
        u2 = normalize(y)
        z = R[2] - np.dot(R[2], u1) * u1 + np.dot(R[2], u2) * u2
        u3 = normalize(z)
        return np.array([u1, u2, u3])

    def check_collisions(self, obj):
        for link in obj.links:
            for point in self.vertices:
                if distance_point_wall(point, obj.vertices[link]) < 1:
                    self.collision(obj.vertices[link], point, 0.2)

    def collision(self, wall, point, dt):
        self.p -= dt * self.linear_velocity
        normWall = normalize(np.cross(wall[0] - wall[1], wall[1] - wall[2]))
        u = normWall @ wall[0]

        temp = ((u - normWall[0]*point[0] - normWall[1]*point[1] - normWall[2]*point[2] ) / np.sum(normWall**2))
        x0 = point[0] + normWall[0] * temp
        x1 = point[1] + normWall[1] * temp
        x2 = point[2] + normWall[2] * temp
        crossingPoint = np.array([x0, x1, x2])

        n = crossingPoint - point
        if np.abs(n[0]) <= np.abs(n[1]) and np.abs(n[0]) <= np.abs(n[2]):
            t = np.array([0, n[2], -n[1]])
        elif np.abs(n[1]) <= np.abs(n[0]) and np.abs(n[1]) <= np.abs(n[2]):
            t = np.array([-n[2], 0, n[0]])
        elif np.abs(n[2]) <= np.abs(n[0]) and np.abs(n[2]) <= np.abs(n[1]):
            t = np.array([n[1], -n[0], 0])
        k = np.cross(n, t)

        me = (self.p + crossingPoint) / 2

        M = normalize(np.array([n, t, k])) * [1, 1, -1]

        v_ntk1 = M @ np.array(self.linear_velocity)
        v_ntk2 = np.zeros(3)

        G = M @ self.J @ np.transpose(M)
        m_ = 1/self.mass
        self.Q1 = np.linalg.inv(self.J)

        r = crossingPoint - self.mass_center
        self.r_ntk = M @ r
        w_ntk = M @ self.angular_velocity

        PC = self.Calculate_critical_P(v_ntk1, v_ntk2, w_ntk, m_)
        PM = self.Calculate_max_P(v_ntk1, v_ntk2, w_ntk, m_)

        v = (PM / self.mass) + v_ntk1
        v1 = (PC / self.mass) + v_ntk1
        if np.sign(np.linalg.norm(v_ntk1[1:])) != np.sign(np.linalg.norm(v[1:])) :
            v = v1
            P = PC
        else:
            P = PM

        e = (self.Q1 * self.r_ntk) @ P + w_ntk

        self.angular_velocity = np.linalg.inv(M) @ e

        self.linear_velocity = np.linalg.inv(M) @ v


    def Calculate_velocity(self, P):
        pass

    def Calculate_critical_P(self, v_ntk1, v_ntk2, w_ntk, m_):
        Zt = v_ntk1[1] + self.r_ntk[0]*w_ntk[2] - self.r_ntk[2]*w_ntk[0]
        Zk = v_ntk1[2] - self.r_ntk[0]*w_ntk[1] + self.r_ntk[1]*w_ntk[0]
        znt = -self.get_h(0,2,1,2) + self.get_h(0,2,2,2) + self.get_h(2,0,1,2) - self.get_h(2,0,2,1)
        ztt =  self.get_h(0,2,0,2) - self.get_h(0,2,2,0) - self.get_h(2,0,0,2) + self.get_h(2,0,2,0) - m_
        zkt = -self.get_h(0,2,0,1) + self.get_h(0,2,1,0) + self.get_h(2,0,0,1) - self.get_h(2,0,1,0)
        znk =  self.get_h(0,1,1,2) - self.get_h(0,1,2,1) - self.get_h(1,0,1,2) + self.get_h(1,0,2,1)
        ztk = -self.get_h(0,1,2,2) + self.get_h(0,1,2,0) + self.get_h(1,0,0,2) - self.get_h(1,0,2,0)
        zkk =  self.get_h(0,1,2,1) - self.get_h(0,1,1,0) - self.get_h(1,0,0,1) + self.get_h(1,0,1,0) - m_
        At = (Zt*zkk - Zk*zkt) / ztt*zkk - ztk*zkt
        Bt = -(znt*zkk - znk*zkt) / (ztt*zkk - ztk*zkt)
        Ak = (Zk*ztt - Zt*ztk) / (zkk*ztt - zkt*ztk)
        Bk = -(znk*ztt - znt*ztk) / (zkk*ztt - zkt*ztk)
        A1 = np.array([
            -self.r_ntk[2]*At + self.r_ntk[1]*Ak,
            -self.r_ntk[0]*Ak,
            self.r_ntk[0]*At
        ])
        B1 = np.array([
            -self.r_ntk[2] * Bt + self.r_ntk[1] * Bk,
            self.r_ntk[2] - self.r_ntk[0]*Bk,
            -self.r_ntk[1] + self.r_ntk[0]*Bt
        ])
        P_n = (self.s + 1) * ((v_ntk2[0] - v_ntk1[0] - self.r_ntk[2]*w_ntk[1] + self.r_ntk[1]*w_ntk[2] - (self.r_ntk[2]*self.Q1[1,:]@A1 - self.r_ntk[1]*self.Q1[2,:]@A1)) / (m_ + self.r_ntk[2]*self.Q1[1,:]@B1 - self.r_ntk[1]*self.Q1[2,:]@B1))
        P_t = At + Bt*P_n
        P_k = Ak + Bk*P_n

        return np.array([P_n, P_t, P_k])

    def Calculate_max_P(self, v_ntk1, v_ntk2, w_ntk, m_):
        phi_n = v_ntk1[0] - w_ntk[2]*self.r_ntk[1] + w_ntk[1]*self.r_ntk[2]
        phi_t = v_ntk1[1] - w_ntk[2]*self.r_ntk[0] - w_ntk[0]*self.r_ntk[2]
        phi_k = v_ntk1[2] - w_ntk[1]*self.r_ntk[0] + w_ntk[0]*self.r_ntk[1]
        u_t = np.abs(self.u * (phi_t)/(np.sqrt(phi_t**2 + phi_k**2))) * np.sign(phi_t/phi_n)
        u_k = np.abs(self.u * (phi_k)/(np.sqrt(phi_t**2 + phi_k**2))) * np.sign(phi_k/phi_n)
        C1 = np.array([
            -self.r_ntk[2]*u_t + self.r_ntk[1]*u_k,
            self.r_ntk[2] - self.r_ntk[0]*u_k,
            -self.r_ntk[1] + self.r_ntk[0]*u_t
        ])
        P_n = (self.s + 1)* ((v_ntk2[0] - v_ntk1[0] - self.r_ntk[2]*w_ntk[1] + self.r_ntk[1]*w_ntk[2])/(m_ + self.r_ntk[2]*self.Q1[1,:]@C1 - self.r_ntk[1]*self.Q1[2,:]@C1))
        P_t = P_n * u_t
        P_k = P_n * u_k

        return np.array([P_n, P_t, P_k])

    def get_h(self, a, b, c, d):
        return self.r_ntk[a] * self.Q1[b,c] * self.r_ntk[d]

def distance_point_wall(point, wall):
    a, b, c = normalize(np.cross(wall[0] - wall[1], wall[1] - wall[2]))
    return np.abs(a * (point[0] - wall[0, 0]) + b * (point[1] - wall[0, 1]) + c * (point[2] - wall[0, 2]) / np.linalg.norm(np.array([a, b, c])))

