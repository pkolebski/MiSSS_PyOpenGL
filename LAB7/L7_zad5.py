from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *

shad = None 
ures = None 
winwidht = None 
winheight = None
line_size = 1
line_size_location = None

def keyboard(key, x, y):
    global line_size
    ch = key.decode("utf-8")
    if ch == 'a':
        line_size *= 2
        return
    elif ch == 's':
        line_size *= 0.5
        return
    line_size = int(ch)


def paint():
    global shad, ures, winwidht, winheight, line_size, line_size_location
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, -0.0, -4.0)
    glUseProgram(shad)
    glUniform2f(ures, winwidth//2, winheight//2)
    glUniform1f(line_size_location, line_size)
    glBegin(GL_POLYGON)
    glVertex2f(-5.0, -2.0)
    glVertex2f(5.0, -2.0)
    glVertex2f(5.0, 2.0)
    glVertex2f(-5.0, 2.0)
    glEnd()
    # glutSolidSphere(1.0, 32, 32)
    glutSwapBuffers()
def main():
    global shad, ures, winwidth, winheight, line_size, line_size_location
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    winwidth = glutGet(GLUT_SCREEN_WIDTH)
    winheight = glutGet(GLUT_SCREEN_HEIGHT)
    glutInitWindowSize(winwidth//2, winheight//2)
    glutInitWindowPosition(winwidth//4, winheight//4)
    glutCreateWindow(b"my02")
    glClearColor(1.0, 0.0, 0.0, 0.5)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(50.0, float(winwidth/winheight), 0.1, 100.0)
    glutDisplayFunc(paint)
    glutIdleFunc(paint)
    glutKeyboardFunc(keyboard)
    glMatrixMode(GL_MODELVIEW)
    shad = compileProgram(
    compileShader("""
    #extension GL_EXT_gpu_shader4 : enable
    uniform vec2 ures;
    uniform float line_size;
    
    float getf(vec2 st) {
    float x = st.x * 20 - 10;
    float y = st.y * 20 - 10;
    float a = 2;
        if (abs(pow((pow(x, 2.) + pow(y, 2.)), 2.) + 4. * a * x * (pow(x, 2.) + pow(y, 2.)) - 4. * pow(a, 2.) * pow(y, 2.)) < line_size) {
            return 1.0;
        }
        return 0.0;
       
    }
    void main() {
        vec2 st = gl_FragCoord.xy/ures;
        float val = getf(st);
        gl_FragColor = vec4(val, 20., 20., 20.0);
    } """, GL_FRAGMENT_SHADER), )
    ures = glGetUniformLocation(shad, "ures")
    line_size_location = glGetUniformLocation(shad, "line_size")
    print(ures)
    glutMainLoop()
main()

