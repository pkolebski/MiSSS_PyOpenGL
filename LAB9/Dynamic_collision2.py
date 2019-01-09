def dynamic_collision2(obj1, obj2, dt):

    obj1.p -= dt * obj1.v
    obj2.p -= dt * obj2.v
    # dystans pomiedzy kulkami
    fDistance = np.sqrt((obj1.p[0] - obj2.p[0]) ** 2 + (obj1.p[2] - obj2.p[2]) ** 2)

    # wektory normalne
    nx = (obj1.p[0] - obj2.p[0]) / fDistance
    nz = (obj1.p[2] - obj2.p[2]) / fDistance

    # wektory t
    tx = -nz
    tz = nx

    # dot product t
    dpTan1 = obj1.v[0] * tx + obj1.v[2] * tz
    dpTan2 = obj2.v[0] * tx + obj2.v[2] * tz

    # dot product normal
    dpNorm1 = obj1.v[0] * nx + obj1.v[2] * nz
    dpNorm2 = obj2.v[0] * nx + obj2.v[2] * nz

    # conservation of momentum
    m1 = (dpNorm1 * (obj1.m - obj2.m) + 1 * obj2.m * dpNorm2) / (obj1.m + obj2.m)
    m2 = (dpNorm2 * (obj2.m - obj1.m) + 1 * obj1.m * dpNorm1) / (obj1.m + obj2.m)

    obj1.v[0] = obj1.s * tx * dpTan1 + nx * m1
    obj1.v[2] = obj1.s * tz * dpTan1 + nz * m1
    obj2.v[0] = obj1.s * tx * dpTan2 + nx * m2
    obj2.v[2] = obj1.s * tz * dpTan2 + nz * m2