import pygame
import math
from VOBJ import createVector
import VOBJ
import GEWY

WIDTH = 600
HEIGHT = 600
FPS = 30

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()     ## For syncing the FPS

class Board:
	def __init__(self, cs: int):
		self.width    = 8
		self.height   = 8
		self.cellSize = cs
		self.grid: list = [[0,1,0,0,0,1,1,1],
						   [0,1,0,0,1,1,0,1],
						   [0,1,0,0,0,0,0,1],
						   [0,1,0,0,0,1,0,0],
						   [0,1,0,1,1,1,0,1],
						   [0,0,0,1,0,0,0,1],
						   [1,1,1,1,0,1,0,1],
						   [0,0,0,0,0,1,1,1]]

	def show_board(self, screen):
		cs = self.cellSize
		for y in range(8):
			for x in range(8):
				if self.grid[y][x] == 1:
					pygame.draw.rect(screen, (50,50,50), pygame.Rect(x*cs, y*cs, cs, cs))

class Player:
	def __init__(self, start_x, start_y, col):
		self.pos = createVector(start_x, start_y)
		self.vel = createVector()
		self.radius = 25
		self.speed = 5
		self.col: tuple = col

	def Handle_movement(self, board, keysPressed, screen, dispView: True):
		if keysPressed[pygame.K_w]:
			self.vel.y -= 1
		if keysPressed[pygame.K_a]:
			self.vel.x -= 1
		if keysPressed[pygame.K_s]:
			self.vel.y += 1
		if keysPressed[pygame.K_d]:
			self.vel.x += 1

		cs = board.cellSize  # using cs to shorten code

		clamped_points = [  # set preset points of all 4 surrounding walls of demo
		createVector(VOBJ.clamp(self.pos.x, -1, WIDTH+1), VOBJ.clamp(self.pos.y, -1, 0)),
		createVector(VOBJ.clamp(self.pos.x, WIDTH, WIDTH+1), VOBJ.clamp(self.pos.y, -1, HEIGHT+1)),
		createVector(VOBJ.clamp(self.pos.x, -1, WIDTH+1), VOBJ.clamp(self.pos.y, HEIGHT, HEIGHT+1)),
		createVector(VOBJ.clamp(self.pos.x, -1, 0), VOBJ.clamp(self.pos.y, -1, HEIGHT+1))]

		# Calculate player's cell coordinates
		player_pos = createVector(int(self.pos.x // cs), int(self.pos.y // cs))

		for y in range(player_pos.y - 1, player_pos.y + 2):  # loop over adjacent cell coordinates
			for x in range(player_pos.x - 1, player_pos.x + 2):

				if board.grid[VOBJ.clamp(y, 0, 7)][VOBJ.clamp(x, 0, 7)] == 1:  # only look at walls
					# clamp between left, right, up and down of cell
					clamp_point = createVector(VOBJ.clamp(self.pos.x, x*cs, (x+1)*cs), 
											   VOBJ.clamp(self.pos.y, y*cs, (y+1)*cs))
					# draw small grey circle
					if dispView: pygame.draw.circle(screen, (130,130,130), (clamp_point.x,clamp_point.y), 5)
					clamped_points.append(clamp_point)  # store points for iteration

		# loop over each clamped point
		for idx, point in enumerate(clamped_points):
			vPointToPlayer = point - self.pos  # get vector from player to point
			DistToPlayer = vPointToPlayer.mag()  # get mag for overlap calc
			if DistToPlayer - self.radius < 0 and DistToPlayer:  # make sure Dist > 0
				vPointToPlayer.normalize()
				vPointToPlayer *= DistToPlayer - self.radius  # scale by overlap
				self.pos += vPointToPlayer


	def update(self):
		if self.vel.mag(): self.vel.normalize()
		self.vel *= self.speed
		self.pos += self.vel
		self.vel *= 0

	def __show_view(self, screen, board: Board):
		cs = board.cellSize
		player_pos = createVector(int(self.pos.x // cs), int(self.pos.y // cs))
		for y in range(player_pos.y - 1, player_pos.y + 2):
			for x in range(player_pos.x - 1, player_pos.x + 2):
				pygame.draw.rect(screen, (255,0,0), pygame.Rect(x*cs, y*cs, cs, cs), 1)

	def show(self, screen, board: Board, dispView: True):
		if dispView: self.__show_view(screen, board)
		pygame.draw.circle(screen, self.col, (self.pos.x, self.pos.y), self.radius)

def main():

	# GUI n SHIIIIIII
	show_special_button = GEWY.Button(10, 10, 25, 25, "Show View")
	show_rainbow_button = GEWY.Button(10, 45, 25, 25, "rainbow")
	show_special_wrapper = GEWY.Wrapper(20, 40, 105, 80, [show_special_button, show_rainbow_button], "View Options")
	GEWY.GUI_OBJECTS.append(show_special_wrapper)

	speed_slider = GEWY.VariableSlider(5, 32, 200, 1, 15, "Speed", True, 5)
	player_colour_slider = GEWY.ColourSlider(10, 80, 200, 25, 15, (0,255,0))
	speed_slider_wrapper = GEWY.Wrapper(10, 40, 230, 200, [speed_slider, player_colour_slider], "Player Options")
	GEWY.GUI_OBJECTS.append(speed_slider_wrapper)

	Tabs = GEWY.TabSystem(textColour=(0,0,0))  # mufuckiiin tab system
	Tabs.addTab(show_special_wrapper)
	Tabs.addTab(speed_slider_wrapper)
	GEWY.GUI_OBJECTS.append(Tabs)

	main_board = Board(75)
	player = Player(WIDTH/2, 250, (0,255,0))
	ColIDX = 0  

	# Game loop
	running = True
	while running:

		pygame.display.set_caption(f'Collision Demo: {round(clock.get_fps(), 2)}')

		col = GEWY.hsv2rgb(ColIDX % 360, 100, 100)  # hsv is easy to make rainbow

		player.speed = speed_slider.returnValue()
		player.col = player_colour_slider.returnColour() if not show_rainbow_button.returnState() else col

		#1 Process input/events
		clock.tick(FPS)     ## will make the loop run at the same speed all the time
		for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
			## listening for the the X button at the top
			if event.type == pygame.QUIT:
				running = False

			mVec = pygame.mouse.get_pos()  # get mouse position
			GEWY.handleEvents(event, mVec, screen)  # let GEWY handle all interactions
		keysPressed = pygame.key.get_pressed()

		#3 Draw/render
		screen.fill(WHITE)

		main_board.show_board(screen)

		player.Handle_movement(main_board, keysPressed, screen, show_special_button.returnState())
		player.show(screen, main_board, show_special_button.returnState())
		player.update()

		# Done after drawing everything to the screen
		GEWY.display(screen)  # displays all GEWY elements
		pygame.display.flip()   

		ColIDX += 2  # speed of rainbow 
		ColIDX %= 360  # keep idx between 0 and 360

	pygame.quit()

if __name__ == "__main__":
	main()
