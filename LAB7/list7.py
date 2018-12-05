from OpenGL.GL import * # importowanie GL
from OpenGL.GLUT import * # importowanie GLUT
from OpenGL.GLU import *
from numpy import *

def rysuj():
    glClear(GL_COLOR_BUFFER_BIT) # czyszczenie bufora kolorów
    glFlush() # wymuszenie wyświetlania

glutInit() # inicjalizacja biblioteki
glutInitWindowSize(800, 800) # ustawienie rozmiaru okna
glutInitWindowPosition(0, 0) # ustawienie pozycji okna
glutCreateWindow(b"Lista nr 8") # tytuł okna
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB) # parametry okna
glutDisplayFunc(rysuj) # wybór głównej pętli programu
glClearColor(1.0, 0, 0, 1.0) # ustawienie koloru tła
glutMainLoop() # uruchomienie głównej pętli programu

rysuj()
