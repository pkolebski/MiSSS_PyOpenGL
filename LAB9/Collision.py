def chceck(sphere, cube):
    if sphere.p[1] - sphere.r < cube.up:
        sphere.v[1] = -sphere.s * sphere.v[1]
        sphere.p[1] += cube.up - (sphere.p[1] - sphere.r)

def chceck2(sphere, cube): #lewa sciana
    if sphere.p[2] - sphere.r < cube.right:
        sphere.v[2] = -sphere.s * sphere.v[2]
        sphere.p[2] += cube.right - (sphere.p[2] - sphere.r)

def chceck3(sphere, cube): #prawa sciana
    if sphere.p[2] + sphere.r > cube.right:
        sphere.v[2] = -sphere.s * sphere.v[2]
        sphere.p[2] -= (sphere.p[2] + sphere.r) - cube.right

def chceck4(sphere, cube): #tył
    if sphere.p[0] + sphere.r > cube.front:
        sphere.v[0] = -sphere.s * sphere.v[0]
        sphere.p[0] -= (sphere.p[0] + sphere.r) - cube.front

def chceck5(sphere, cube): #przód
    if sphere.p[0] - sphere.r < cube.front:
        sphere.v[0] = -sphere.s * sphere.v[0]
        sphere.p[0] += cube.front - (sphere.p[0] - sphere.r)