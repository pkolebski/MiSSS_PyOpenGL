from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *

shad = None 
ures = None 
winwidht = None 
winheight = None

def paint():
    global shad, ures, winwidht, winheight
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, -0.0, -4.0)
    glUseProgram(shad)
    glUniform2f(ures, winwidth//2, winheight//2)
    glBegin(GL_POLYGON)
    glVertex2f(-5.0, -2.0)
    glVertex2f(5.0, -2.0)
    glVertex2f(5.0, 2.0)
    glVertex2f(-5.0, 2.0)
    glEnd()
    # glutSolidSphere(1.0, 32, 32)
    glutSwapBuffers()
def main():
    global shad, ures, winwidth, winheight
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
    glMatrixMode(GL_MODELVIEW)
    shad = compileProgram(
    compileShader("""
    #extension GL_EXT_gpu_shader4 : enable
    uniform vec2 ures;
    
    float getf(vec2 st) {
    float x = st.x * 20 - 10;
    float y = st.y * 20 - 10;
    float a = 2;
        if (abs(pow((pow(x, 2.) + pow(y,2.)), 2.) + 4*a*x*(pow(x,2.)+pow(y, 2.))-4*pow(a,2.) *pow(y,2.)) < 4.) {
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
    print(ures)
    glutMainLoop()
main()

