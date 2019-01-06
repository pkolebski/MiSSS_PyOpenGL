import numpy as np

def find_intersection_point(triangle, p0, p1):
    a, b, c = triangle

    n = np.cross(b-a, c-a)
    n = n/np.linalg.norm(n)
    I = np.array([0, 0, 0])
    u = p1-p0
    w = p0 - a

    D = n @ u
    N = - n@w
    check = 0
    if abs(D) < 10e-7:
        if N == 0:
            check = 2
        else:
            check = 0

    sI = N/D
    I = p0 + np.array(sI) * np.array(u)

    if sI < 0 or sI > 1:
        check = 3
    else:
        check = 1
    print(sI, check, I)
    return sI, check


#przeciena
t1 = find_intersection_point(np.array([[1,0,0],[0,1,0],[0,0,1]]), np.array([0,0,0]), np.array([1,1,1]))
#nie przecina
t2 = find_intersection_point(np.array([[1,0,0],[0,1,0],[0,0,1]]), np.array([0,0,0]), np.array([-0.1,1,1]))

P2 = (-0.05263158, 0.52631579, 0.52631579)