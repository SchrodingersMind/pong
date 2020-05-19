import random
from extend import Player

class Ball(object):
	def __init__(self, canva, player, game, sizes, color):
		self.c = canva
		
		self._x_speed = sizes.BALL_MIN_SPEED
		self._y_speed = 0
		if player.get() == Player.RIGHT:
			self._x_speed *= -1 
				
		self.player = player
		
		self.game = game
		self.ss = sizes	# Class with bunch of objects sizes
		
		self.id = self.c.create_ball(self.ss.WIDTH/2, self.ss.HEIGHT/2, 
									self.ss.BALL_RADIUS, fill=color, tag="ball")

		
	def respawn_ball(self):
		# Called at start of match or after goal 
		
		# Set ball at the center
		half_width = self.ss.WIDTH/2
		half_height = self.ss.HEIGHT/2

		self.c.ball_coords(self.id, half_width, half_height)
		# Set direction to looser and slow down x_speed to initial
		# y_speed to zero (should move horizontally)
		self._x_speed = -self.ss.BALL_MIN_SPEED if self._x_speed < 0 else self.ss.BALL_MIN_SPEED
		self._y_speed = 0
		
	def teleport(self):
		""" Change ball position to random """
		half_r = self.ss.BALL_RADIUS//2
		if self.ss.PAD_W*2 + self.ss.BALL_RADIUS >= self.ss.WIDTH or\
				self.ss.BALL_RADIUS >= self.ss.HEIGHT:
			return
		new_x = random.randint(int(self.ss.PAD_W)+half_r, 
							   int(self.ss.RIGHT_TAB)-half_r)
							   
		new_y = random.randint(half_r, 
							   int(self.ss.HEIGHT)-half_r)
							   
		self.c.ball_coords(self.id, new_x, new_y)
		
	def move(self):
		""" Check and change ball position """
		self._vertical_check()
		self._horizontal_check()
		
	def _vertical_check(self):
		""" bounce from top or bottom """
		b_top, b_bottom = self.c.get_top(self.id), self.c.get_down(self.id)
		if (b_top < 0 and self._y_speed < 0) or \
				(b_bottom > self.ss.HEIGHT and self._y_speed > 0):
			self._bounce("wall")
			
	def _horizontal_check(self):
		""" Is ball reaching vertical barrier? """
		b_right, b_left = self.c.get_right(self.id), self.c.get_left(self.id)
		
		if self.player.id == Player.LEFT:
			# Right side
			if b_right + self._x_speed <= self.ss.RIGHT_TAB:
				# If nothing special, move it
				self.c.move(self.id, self._x_speed, self._y_speed)
			elif b_right >= self.ss.RIGHT_TAB:
				# If we crossed the line (now or left user win, or ball touch right pad)
				self._check_pad()
			else:
				# if RIGHT_TAB-ball_speed < ball_right < RIGHT_PAB
				self.c.move(self.id, self.ss.RIGHT_TAB-b_right, self._y_speed)
				# now b_right == RIGHT_TAB

		elif self.player.id == Player.RIGHT:
			# And left
			if b_left + self._x_speed >= self.ss.PAD_W:
				# If nothing special, move it	(Is duplicate comment a good idea??)
				self.c.move(self.id, self._x_speed, self._y_speed)
			elif b_left <= self.ss.PAD_W:
				# If we crossed the line (now or left user win, or ball touch left pad)
				self._check_pad()
			else:
				# if PAD_W < ball_left < PAD_W + ball_speed
				self.c.move(self.id, self.ss.PAD_W-b_left, self._y_speed)
				# now b_left == PAD_W
	
	def _check_pad(self):
		pad = self.player.other.get_pad()
		
		# Check if ball center is between top and bottom of pad
		if self.c.check_collision(self.id, pad.id):
			b_center_y = self.c.get_y_center(self.id)
			alpha = (b_center_y - self.c.get_top(pad.id)) / self.c.get_height(pad.id)
			add_speed = pad.speed / 2
			self._change_side()
			self._bounce("pad", alpha, add_speed)
		else:
			# Right user loose, respawn ball
			self.game.win()
		
	def _bounce(self, source, alpha=None, add_speed=None):
		# source = "pad" if bounce from pad else "wall"
		# 0 <= alpha <= 1	-	change of y_speed 
		# add_speed		- 	impulse added by pad
		if source == "pad":
			alpha_mult = self.ss.HEIGHT/12
			self._y_speed = (alpha-0.5)*alpha_mult + add_speed
			if abs(self._x_speed) < self.ss.BALL_MAX_SPEED:
				self._x_speed *= -self.ss.SPEED_UP_BALL
			else:
				self._x_speed = -self._x_speed
		else:
			self._y_speed = -self._y_speed
			
		
	def _change_side(self):
		self.player.switch()


			
