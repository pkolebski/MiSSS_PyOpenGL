def chceckSphereToCubeCollision(sphere, cube):

    if sphere.p[1] - sphere.r < cube.up:
        sphere.v[1] = -sphere.s * sphere.v[1]
        sphere.p[1] += cube.up - (sphere.p[1] - sphere.r)

    if sphere.p[0] + sphere.r > cube.front:
        sphere.v[0] = -sphere.s * sphere.v[0]
        sphere.p[0] += cube.front - (sphere.p[0] + sphere.r)

    if sphere.p[0] - sphere.r < cube.back:
        sphere.v[0] = -sphere.s * sphere.v[0]
        sphere.p[0] -= (sphere.p[0] - sphere.r) - cube.back

    if sphere.p[2] - sphere.r < cube.left:
        sphere.v[2] = -sphere.s * sphere.v[2]
        sphere.p[2] -= cube.left - (sphere.p[2] + sphere.r)

    if sphere.p[2] + sphere.r > cube.right:
        sphere.v[2] = -sphere.s * sphere.v[2]
        sphere.p[2] -= (sphere.p[2] + sphere.r) - cube.right