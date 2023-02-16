import pygame as pg
import random

SIZE = HIGHT, WIDTH = (900, 1500)
SPEED = 10
BIRD_COL = WIDTH / 3 - 9
BIRD_HEIGHT = 30
BIRD_WIDTH = 30
TOWER_SPACE = BIRD_HEIGHT * 2 + 70
BIRD_MOVE = 10


class Bird():
	def __init__(self):
		self.jump = 0
		self.hight = HIGHT / 2
		self.clock = pg.time.Clock()
		self.speed = 1.0

	def sleep(self):
		czas = self.clock.tick()/1000
		while czas < (0.08 / self.speed): czas += self.clock.tick()/1000

	def make_move(self):
		if self.jump > 0: self.jump -= 1

		keys = pg.key.get_pressed()

		if self.jump == 0:
			if keys[pg.K_SPACE]:
				self.jump = 4

		if self.jump > 0: self.hight -= BIRD_MOVE
		else: self.hight += BIRD_MOVE

		self.sleep()

class Towers():
	def __init__(self):
		self.TOWER_DIFFERENCE = 350
		self.MAX_HEIGHT_DIFFERENCE = 200

		self.TOWERS = []
		self.new_tower(self.TOWER_DIFFERENCE)
		self.new_tower(0)
	
	def new_tower(self, place = 0):
		new = []
		new.append(WIDTH - 10 - place)
		if len(self.TOWERS) > 0:
			last = self.TOWERS[-1]
			new.append(random.randint(max(40, last[1] - self.MAX_HEIGHT_DIFFERENCE), min((HIGHT - 130), last[1] + self.MAX_HEIGHT_DIFFERENCE)))
		else: new.append(random.randint(40, HIGHT - 40 - TOWER_SPACE))
		self.TOWERS.append(new)

	def make_move(self):
		#przesuniecie wszystkich
		for tower in self.TOWERS: tower[0] -= 7
		
		#wygenerowanie nowej ?
		last = self.TOWERS[-1]
		if last[0] <= WIDTH - self.TOWER_DIFFERENCE:
			self.new_tower(0)



class Board():
	def __init__(self):
		self.screen = pg.display.set_mode((WIDTH,HIGHT))
		pg.display.set_caption("Flappy bird")

		#images
		self.bird_1 = pg.image.load("duck_3_1.png")
		self.bird_1_location = self.bird_1.get_rect()
		self.bird_1_location = (BIRD_COL, HIGHT / 2)
		self.bird_2 = pg.image.load("duck_3_2.png")
		self.bird_2_location = self.bird_2.get_rect()
		self.bird_2_location = (BIRD_COL, HIGHT / 2)
		self.bird_type = 1

		#background
		self.background = pg.image.load("Flappy_bird_background.png")
		self.game_over_screen = pg.image.load("GameOver.png")

		#towers
		self.Towers = Towers()
		self.TOWER_COLOR = (30, 200, 30)
		self.TOWER_WIDTH = 40
		self.brick = pg.Rect(0,0,self.TOWER_WIDTH, 10)

	def draw_box(self):
		self.screen.blit(self.background, (0,0))

	def draw_brick(self, x, y):
		self.brick.x = x
		self.brick.y = y
		pg.draw.rect(self.screen,self.TOWER_COLOR, self.brick)

	def draw_bird(self, new_bird_h):

		if(self.bird_type == 1):
			self.bird_1_location = (BIRD_COL, new_bird_h)
			self.screen.blit(self.bird_1, self.bird_1_location)

		else:
			self.bird_2_location = (BIRD_COL, new_bird_h)
			self.screen.blit(self.bird_2, self.bird_2_location)

	def draw_rest(self, new_bird_h):
		self.draw_box()
		self.tower_generator()
		self.draw_bird(new_bird_h)
		
		pg.display.update()

	def tower_generator(self):
		self.Towers.make_move()
		#wyswietlenie
		for tower in self.Towers.TOWERS:
			for i in range(0, tower[1], 10): self.draw_brick(tower[0], i)
			for i in range(tower[1] + TOWER_SPACE, HIGHT - 10, 10): self.draw_brick(tower[0], i)

	def collision(self, bird_h): #byc moze powinno zostac przeniesione do towers
		if bird_h >= HIGHT: return True
		if bird_h <= 0: return True

		for tower in self.Towers.TOWERS:
			if tower[0] <= BIRD_COL + BIRD_WIDTH and tower[0] + self.TOWER_WIDTH >= BIRD_COL:
				if bird_h <= tower[1] or bird_h >= tower[1] + TOWER_SPACE - BIRD_HEIGHT:
					return True
			
		return False
	
	def game_over(self):
		self.screen.blit(self.game_over_screen, (0, 0))
		pg.display.update()
	
class Game():
	def __init__(self):
		pg.init()
		self.bird = Bird()
		self.board = Board()
		
	def play(self):
		x = 0
		keep_playing = True
		while keep_playing:
			x += 1

			if(x % 5 == 0): #mienianie skrzydel
				self.board.bird_type += 1
				self.board.bird_type %= 2

			if x > 50:#przyspieszanie
				self.bird.speed += 0.1
				x = 0			

			for event in pg.event.get():# sprawdzamy czy cos sie wydarzylo
				if event.type == pg.QUIT: #umozliwienie zamnkniecia okna
					keep_playing = False

			self.board.draw_rest(self.bird.hight)
			self.bird.make_move()

			if self.board.collision(self.bird.hight):
				self.board.draw_rest(self.bird.hight)
				self.board.game_over()
				keep_playing = False
			
		wait = True
		while wait:
			for event in pg.event.get():# sprawdzamy czy cos sie wydarzylo
				if event.type == pg.QUIT: #umozliwienie zamnkniecia okna
					wait = False

			keys = pg.key.get_pressed()
			if keys[pg.K_ESCAPE] or keys[pg.K_RETURN]: wait = False

		pg.quit()
		exit()
		return

new_game = Game()
new_game.play()
