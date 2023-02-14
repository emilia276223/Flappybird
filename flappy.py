import pygame as pg
import random

HIGHT = 900
SPEED = 10
WIDTH = 1500
BIRD_COL = WIDTH / 3 - 9

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

		if self.jump > 0: self.hight -= 10
		else: self.hight += 10

		self.sleep()


class Board():
	def __init__(self):
		self.TOWERS = []

		first = []
		first.append(WIDTH - 10)
		first.append(random.randint(40, HIGHT - 130))
		# self.TOWERS.append(first)

		second = []
		second.append(WIDTH - 360)
		second.append(random.randint(max(40, first[1] - 200), min((HIGHT - 130), first[1] + 200)))
		self.TOWERS.append(second)
		self.TOWERS.append(first)

		self.BIRD_COLOR = (220, 50, 120)
		self.bird_appearance = pg.Rect(BIRD_COL, 0, 10, 10)

		self.TOWER_COLOR = (30, 200, 30)
		self.TOWER_WIDTH = 40
		self.brick = pg.Rect(0,0,self.TOWER_WIDTH, 10)
		
		self.screen = pg.display.set_mode((WIDTH,HIGHT))

		self.space = 90

	def draw_box(self):
		pass

	def draw_brick(self, x, y):
		self.brick.x = x
		self.brick.y = y
		pg.draw.rect(self.screen,self.TOWER_COLOR, self.brick)

	def draw_rest(self, bird_h):
		self.screen.fill((40, 40, 40))

		self.draw_box()
		self.tower_generator()

		self.bird_appearance.y = bird_h
		pg.draw.rect(self.screen, self.BIRD_COLOR, self.bird_appearance)

		pg.display.flip()

	def tower_generator(self):

		for tower in self.TOWERS: tower[0] -= 7
		
		# byc moze wygenerowanie nowej
		last = self.TOWERS[-1]
		if last[0] <= WIDTH - 350:
			#wygenerowanie nowej
			new = []
			new.append(WIDTH - 10)
			new_place = random.randint(40, HIGHT - 90)
			if new_place > last[1] + 200:
				new_place = last[1] + 200

			if new_place < last[1] - 200:
				new_place = last[1] - 200

			new.append(new_place)
			self.TOWERS.append(new)

		#wyswietlenie
		for tower in self.TOWERS:
			for i in range(0, tower[1], 10): self.draw_brick(tower[0], i)
			for i in range(tower[1] + self.space, HIGHT - 10, 10): self.draw_brick(tower[0], i)
		

	def collision(self, bird_h):
		if bird_h >= HIGHT: return True
		if bird_h <= 0: return True

		for tower in self.TOWERS:
			if tower[0] <= BIRD_COL + 10 and tower[0] + self.TOWER_WIDTH >= BIRD_COL:
				if bird_h <= tower[1] or bird_h >= tower[1] + self.space:
					return True
			
		return False

	
class Game():
	def __init__(self):
		pg.init()
		self.bird = Bird()
		self.board = Board()
		
	def play(self):
		x = 0
		while True:
			x += 1
			if x > 50:
				self.bird.speed += 0.1
				x = 0			

			for event in pg.event.get():# sprawdzamy czy cos sie wydarzylo
				if event.type == pg.QUIT: #umozliwienie zamnkniecia okna
					pg.quit()
					exit()

			self.board.draw_rest(self.bird.hight)
			self.bird.make_move()

			if self.board.collision(self.bird.hight):
				print("GAME OVER")
				pg.quit()
				exit()
				return

new_game = Game()
new_game.play()
