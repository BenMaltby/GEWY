import math

class createVector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __repr__(self):
		return f'({self.x}, {self.y})'

	def __add__(self, other):
		if type(other) == createVector:
			return createVector(self.x + other.x, self.y + other.y)
		else: return createVector(self.x + other, self.y + other)

	def __mul__(self, other):
		if type(other) == createVector:
			return createVector(self.x * other.x, self.y * other.y)
		else: return createVector(self.x * other, self.y * other)

	def __sub__(self, other):
		if type(other) == createVector:
			return createVector(self.x - other.x, self.y - other.y)
		else: return createVector(self.x - other, self.y - other)

	def __truediv__(self, other):
		if type(other) == createVector:
			return createVector(self.x / other.x, self.y / other.y)
		else: return createVector(self.x / other, self.y / other)

	def mag(self):
		return math.sqrt(self.x*self.x + self.y*self.y)

	def normalize(self):
		M = self.mag()
		self.x /= M
		self.y /= M

	def setMag(self, n):
		self.normalize()
		self.x *= n
		self.y *= n

def min(a, b):
	return a if a < b else b

def max(a, b):
	return a if a > b else b

def clamp(n, lr, ur):
	return min(max(lr, n), ur)