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
    def calculate_r3(self, alpha, beta, gamma):
        return np.array([
            [ np.cos(gamma) * np.cos(alpha) - np.cos(beta) * np.sin(alpha) * np.sin(gamma),  np.cos(gamma) * np.sin(alpha) + np.cos(beta) * np.cos(alpha) * np.sin(gamma), np.sin(gamma) * np.sin(beta)],
            [-np.sin(gamma) * np.cos(alpha) - np.cos(beta) * np.sin(alpha) * np.cos(gamma), -np.sin(gamma) * np.sin(alpha) + np.cos(beta) * np.cos(alpha) * np.cos(gamma), np.cos(gamma) * np.sin(beta)],
            [np.sin(beta) * np.sin(alpha), -np.sin(beta) * np.cos(alpha), np.cos(beta)]
        ])

class Scene(Figure):
    pass


class Tetrahedron(Figure):
    def __init__(self, v=[1,1,1], points=None, links=None, mass=10, color=[1, 1, 0.5], fill=True):
        vertices = np.array([
            [5, 5, 0],
            [-5, 5, 0],
            [0, -3, 0],
            [0, 0, 5],
        ], dtype=np.float32) + np.array([15, 0, 0]) if points is None else points

        links = np.array([
            [0, 1, 2],
            [1, 3, 2],
            [3, 0, 2],
            [0, 3, 1],
        ]) if links is None else links
        super().__init__(vertices, links, color=color, fill=fill)
        self.mass = mass
        self.mass_center = np.mean(self.vertices)
        self.linear_velocity = np.array(v, dtype=np.float32)
        self.angular_velocity = np.array([0,0,0], dtype=np.float32)
        self.r = np.mean(self.vertices[0:3])

        self.h = distance_point_wall(self.vertices[-1, :], self.vertices[:3, :])
        self.momentum = self.mass * self.linear_velocity
        self.O = np.array([0, 0, 0], dtype=np.float32)
        self.s = 0.9
        self.u = 0.2
        self.inertia_tensor = [
            [0.6 * self.mass * self.h ** 2 + 0.15 * self.mass * self.r ** 2, 0, 0],
            [0, 0.6 * self.mass * self.h ** 2 + 0.15 * self.mass * self.r ** 2, 0],
            [0, 0, 0.3 * self.mass * self.r ** 2]
        ]
        self.W_matrix=np.array([
            [0, -self.angular_velocity[2], self.angular_velocity[1]],
            [self.angular_velocity[2], 0, -self.angular_velocity[0]],
            [-self.angular_velocity[1],self.angular_velocity[0], 0 ]
        ])
        self.oldR = np.eye(3)
        self.H = self.inertia_tensor @ self.angular_velocity

    def update(self, dt):

        self.W_matrix = np.array([
            [0, -self.angular_velocity[2], self.angular_velocity[1]],
            [self.angular_velocity[2], 0, -self.angular_velocity[0]],
            [-self.angular_velocity[1], self.angular_velocity[0], 0]
        ])

        self.resistance(dt)
        self.mass_center = np.mean(self.vertices, 0)

        self.vertices -= self.mass_center
        R =  self.gram_schmidt(self.calculate_r3(*self.angular_velocity * dt))
        for i in range(len(self.vertices)):
            self.vertices[i, :] = R @ self.vertices[i, :]
        self.vertices += self.mass_center

        self.vertices += dt * self.linear_velocity

        # self.netforce = 3 * (self.mass/1000*(self.oldvelocity-self.linear_velocity)*dt)
        # self.O = np.sum([self.netforce*(vertice-self.mass_center) for vertice in self.vertices ])
        # self.H = (self.oldO-self.O)*dt
        # self.inertia_tensor = R @ self.inertia_tensor @ np.transpose(R)
        # self.angular_velocity = np.linalg.inv(self.inertia_tensor) * self.H

    def resistance(self, dt):
        self.linear_velocity -= np.array([0, (dt * 0.9 * self.mass), 0])
        self.linear_velocity *= 0.9
        self.angular_velocity *= 0.9

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
                    print("Kolizja")

    def collision(self, wall, point, dt):
        self.vertices -= dt * self.linear_velocity
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

        self.draw_ntk(crossingPoint, n, t, k)

        M = normalize(np.array([n, t, k])) * [1, 1, -1]
        G = M @ self.inertia_tensor @ np.transpose(M)
        self.Q1 = np.linalg.inv(G)

        v_ntk1 = M @ np.array(self.linear_velocity)
        v_ntk2 = np.zeros(3)

        m_ = 1.0 / self.mass

        r = crossingPoint - self.mass_center
        self.r_ntk = self.to_ntk(r, M)
        w_ntk = self.to_ntk(self.angular_velocity, M)

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

        self.angular_velocity = self.base(e, M)
        self.linear_velocity = self.base(v, M)
        self.H = self.inertia_tensor @ self.angular_velocity

        print(self.H)

    def base(self, obj, M):
        return np.linalg.inv(M) @ obj

    def to_ntk(self, obj, M):
        return M @ obj

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

    def Calculate_critical_P1P2(self, Q1, Q2, r_ntk, r_ntk2, v_ntk1, v_ntk2, w_ntk, w_ntk2, m_):
        def get_h(a, b, c, d, e):
            if e == 0:
                return r_ntk[a] * Q1[b, c] * r_ntk[d]
            else:
                return r_ntk2[a] * Q2[b, c] * r_ntk2[d]

        Zt = v_ntk1[1] - v_ntk2[1] - r_ntk2[0] * w_ntk2[2] + r_ntk2[2] * w_ntk2[0] + r_ntk[0] * w_ntk[2] - r_ntk[2] * w_ntk[
            0]
        Zk = v_ntk1[2] - v_ntk2[2] - r_ntk2[0] * w_ntk2[1] + r_ntk2[1] * w_ntk2[0] + r_ntk[0] * w_ntk[1] - r_ntk[1] * w_ntk[
            0]
        znt = -get_h(0, 2, 1, 2, 1) + get_h(0, 2, 2, 2, 1) + get_h(2, 0, 1, 2, 1) - get_h(2, 0, 2, 1, 1) - get_h(0, 2, 1, 2,
                                                                                                                 0) + get_h(
            0, 2, 2, 2, 0) + get_h(2, 0, 1, 2, 0) - get_h(2, 0, 2, 1, 0)
        ztt = get_h(0, 2, 0, 2, 1) - get_h(0, 2, 2, 0, 1) - get_h(2, 0, 0, 2, 1) + get_h(2, 0, 2, 0, 1) + get_h(0, 2, 0, 2,
                                                                                                                0) - get_h(
            0, 2, 2, 0, 0) - get_h(2, 0, 0, 2, 0) + get_h(2, 0, 2, 0, 0) - m_
        zkt = -get_h(0, 2, 0, 1, 1) + get_h(0, 2, 1, 0, 1) + get_h(2, 0, 0, 1, 1) - get_h(2, 0, 1, 0, 1) - get_h(0, 2, 0, 1,
                                                                                                                 0) + get_h(
            0, 2, 1, 0, 0) + get_h(2, 0, 0, 1, 0) - get_h(2, 0, 1, 0, 0)
        znk = get_h(0, 1, 1, 2, 1) - get_h(0, 1, 2, 1, 1) - get_h(1, 0, 1, 2, 1) + get_h(1, 0, 2, 1, 1) + get_h(0, 1, 1, 2,
                                                                                                                0) - get_h(
            0, 1, 2, 1, 0) - get_h(1, 0, 1, 2, 0) + get_h(1, 0, 2, 1, 0)
        ztk = -get_h(0, 1, 2, 2, 1) + get_h(0, 1, 2, 0, 1) + get_h(1, 0, 0, 2, 1) - get_h(1, 0, 2, 0, 1) - get_h(0, 1, 2, 2,
                                                                                                                 0) + get_h(
            0, 1, 2, 0, 0) + get_h(1, 0, 0, 2, 0) - get_h(1, 0, 2, 0, 0)
        zkk = get_h(0, 1, 0, 1, 1) - get_h(0, 1, 1, 0, 1) - get_h(1, 0, 0, 1, 1) + get_h(1, 0, 1, 0, 1) + get_h(0, 1, 0, 1,
                                                                                                                0) - get_h(
            0, 1, 1, 0, 0) - get_h(1, 0, 0, 1, 0) + get_h(1, 0, 1, 0, 0) - m_
        At = (Zt * zkk - Zk * zkt) / ztt * zkk - ztk * zkt
        Bt = -(znt * zkk - znk * zkt) / (ztt * zkk - ztk * zkt)
        Ak = (Zk * ztt - Zt * ztk) / (zkk * ztt - zkt * ztk)
        Bk = -(znk * ztt - znt * ztk) / (zkk * ztt - zkt * ztk)
        A1 = np.array([
            -r_ntk[2] * At + r_ntk[1] * Ak,
            -r_ntk[0] * Ak,
            r_ntk[0] * At
        ])
        A2 = np.array([
            r_ntk2[2] * At - r_ntk2[1] * Ak,
            r_ntk2[0] * Ak,
            -r_ntk2[0] * At
        ])
        B1 = np.array([
            -r_ntk[2] * Bt + r_ntk[1] * Bk,
            r_ntk[2] - r_ntk[0] * Bk,
            -r_ntk[1] + r_ntk[0] * Bt
        ])
        B2 = np.array([
            r_ntk2[2] * Bt - r_ntk2[1] * Bk,
            -r_ntk2[2] + r_ntk2[0] * Bk,
            r_ntk2[1] - r_ntk2[0] * Bt
        ])
        P_n = (self.s + 1) * ((v_ntk2[0] - v_ntk1[0] - r_ntk[2] * w_ntk[1] + r_ntk[1] * w_ntk[2] + r_ntk2[2] * w_ntk2[1] -
                               r_ntk2[1] * w_ntk2[2] - r_ntk[2] * Q1[1, :] @ A1 - r_ntk[1] * Q1[2, :] @ A1 - r_ntk2[2] * Q2[
                                                                                                                         1,
                                                                                                                         :] @ A2 +
                               r_ntk2[1] * Q2[2, :] @ A2) / (
                                          m_ + r_ntk[2] * Q1[1, :] @ B1 - r_ntk[1] * Q1[2, :] @ B1 - r_ntk2[2] * Q2[1,
                                                                                                                 :] @ B2 +
                                          r_ntk2[1] * Q2[2, :] @ B2))
        P_t = At + Bt * P_n
        P_k = Ak + Bk * P_n

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

    def Calculate_max_P2(self, v_ntk1, v_ntk2, w_ntk1, w_ntk2, r_ntk1, r_ntk2, Q1, Q2, m_):
        phi_n = v_ntk1[0] - v_ntk2[0] - w_ntk1[2] * r_ntk1[1] + w_ntk1[1] * r_ntk1[2] + w_ntk2[2] * r_ntk2[1] - w_ntk2[1] * r_ntk2[2]
        phi_t = v_ntk1[1] - v_ntk2[1] - w_ntk1[2] * r_ntk1[0] - w_ntk1[0] * r_ntk1[2] - w_ntk2[2] * r_ntk2[0] + w_ntk2[0] * r_ntk2[2]
        phi_k = v_ntk1[2] - v_ntk2[1] - w_ntk1[1] * r_ntk1[0] + w_ntk1[0] * r_ntk1[1] + w_ntk2[1] * r_ntk2[0] - w_ntk2[0] * r_ntk2[1]
        u_t = np.abs(self.u * (phi_t)/(np.sqrt(phi_t**2 + phi_k**2))) * np.sign(phi_t/phi_n)
        u_k = np.abs(self.u * (phi_k)/(np.sqrt(phi_t**2 + phi_k**2))) * np.sign(phi_k/phi_n)
        C1 = np.array([
            -r_ntk1[2] * u_t + r_ntk1[1] * u_k,
             r_ntk1[2] - r_ntk1[0]*u_k,
            -r_ntk1[1] + r_ntk1[0]*u_t
        ])

        C2 = np.array([
            r_ntk2[2] * u_t - r_ntk2[1] * u_k,
            -r_ntk2[2] * u_t + r_ntk2[0] * u_k,
            r_ntk2[1] - r_ntk2[0] * u_t
        ])

        P_n1 = (v_ntk2[0] - v_ntk1[0] - r_ntk1[2] * w_ntk1[1] + r_ntk1[1] * w_ntk1[2] + r_ntk2[2] * w_ntk2[1] - r_ntk2[1] * w_ntk2[2])
        P_n2 = m_ + r_ntk1[2] * Q1[1, :] @ C1 - r_ntk1[1] * Q1[2, :] @ C1 - r_ntk2[2] * Q2[1, :] @ C2 + r_ntk2[1] * Q2[2, :] @ C2
        P_n = (self.s + 1) * (P_n1 / P_n2)
        P_t = P_n * u_t
        P_k = P_n * u_k

        return np.array([P_n, P_t, P_k])

    def get_h(self, a, b, c, d):
        return self.r_ntk[a] * self.Q1[b,c] * self.r_ntk[d]

    def draw_ntk(self, p, *ntk):
        glLoadIdentity()
        color = np.eye(3)
        for v, c in zip(ntk, color):
            glColor3fv(c)
            glBegin(GL_LINES)
            glVertex3fv(p)
            glVertex3fv(p + v * 10)
            glEnd()

def distance_point_wall(point, wall):
    a, b, c = normalize(np.cross(wall[0] - wall[1], wall[1] - wall[2]))
    return np.abs(a * (point[0] - wall[0, 0]) + b * (point[1] - wall[0, 1]) + c * (point[2] - wall[0, 2]) / np.linalg.norm(np.array([a, b, c])))

