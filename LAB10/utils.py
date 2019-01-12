import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def normalize(vec):
	return vec / np.linalg.norm(vec)

class Scene():
	def __init__(self, down, up, left, right, back, front, color=[1, 1, 0.5], fill=True):
		self.down = down
		self.up = up
		self.left = left
		self.right = right
		self.front = front
		self. back = back
		self.color = color
		self.fill = fill

		self.vertices = [
			[front, down, right],
			[back, down, right],
			[back, up, right],
			[front, up, right],
			[front, down, left],
			[back, down, left],
			[back, up, left],
			[front, up, left]]

		self.links = [
			[0, 1, 5, 4],
			[3, 2, 6, 7],
			[4, 5, 6, 7],
			[0, 1, 2, 3],
			[1, 2, 6, 5],
			[0, 3, 7, 4]
		]

	def draw(self):
		glLoadIdentity()
		glColor3fv(self.color)
		if not self.fill: glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
		for link in self.links:
			glBegin(GL_POLYGON)
			for i in range(4):
				glVertex3fv(self.vertices[link[i]])
			glEnd()
		if not self.fill: glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

class Cube(Scene):
	def __init__(self, down, up, left, right, back, front, color=[1, 1, 0.5], fill=True, mass=1, density=1):
		super().__init__(down, up, left, right, back, front, color, fill)
		self.mass = mass
		self.density = density
