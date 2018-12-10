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
    # (x**2 + y**2 - a*x)**2 = (a**2) * (x**2 + y**2)
    shad = compileProgram(
    compileShader("""
    uniform vec2 ures;
    
    float getf(vec2 st) {
        return (((int(st.x)^2) + (int(st.y)^2))^2) + 4 * 1 * int(st.x) * ((int(st.x)^2) + (int(st.y)^2)) - 4*(1^2)*(int(st.y)^2);
        
    }
    void main() {
        vec2 st = gl_FragCoord.xy/ures ;
        float val = getf(st) ;
        gl_FragColor = vec4(val, 1.0, 1.0, 1.0) ;
    } """, GL_FRAGMENT_SHADER), )
    ures = glGetUniformLocation(shad, "ures")
    print(ures)
    glutMainLoop()
main()

# (((int(st.x)^2) + (int(st.y)^2))^2) + 4 * 1 * int(st.x) * ((int(st.x)^2) + (int(st.y)^2)) - 4*(1^2)*(int(st.y)^2)