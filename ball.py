import random

class Ball(object):
	def __init__(self, canva, l_pad_id, r_pad_id, game, sizes, color):
		self.c = canva
		
		self.x_speed = sizes.BALL_MIN_SPEED
		self.y_speed = 0
				
		self.l_pad_id = l_pad_id
		self.r_pad_id = r_pad_id
		
		self.game = game
		self.ss = sizes	# Class with bunch of objects sizes
		
		self.id = self.c.create_ball(self.ss.WIDTH/2, self.ss.HEIGHT/2, 
										self.ss.BALL_RADIUS, fill=color, tag="ball")

		
		self.side = self._get_side()
		
	def respawn_ball(self):
		# Called at start of match or after goal 
		
		# Set ball at the center
		half_width = self.ss.WIDTH/2
		half_height = self.ss.HEIGHT/2

		self.c.ball_coords(self.id, half_width, half_height)
		# Set direction to looser and slow down x_speed to initial, y_speed to zero (should move horizontally)
		self.x_speed = -self.ss.BALL_MIN_SPEED if self.x_speed < 0 else self.ss.BALL_MIN_SPEED
		self.y_speed = 0
		
	def move(self):
		b_left, b_top, b_right, b_bot = self.c.bbox(self.id)
		b_center_y = (b_top + b_bot) / 2
 	
		off = self.ss.BALL_RADIUS / 2
		# If nothing special - move ball
		if b_right + self.x_speed <= self.ss.RIGHT_TAB and \
				b_left + self.x_speed >= self.ss.PAD_W:
			self.c.move(self.id, self.x_speed, self.y_speed)
		# Touched left or right line (inner side of pad)
		elif b_right >= self.ss.RIGHT_TAB:
			# Right side
			# Check if ball center is between top and bottom of pad
			# off added for cases, for ex. when pad bottom between ball top and center
			if self.c.check_collision(self.id, self.r_pad_id, balls=True):
				alpha = (b_center_y - self.c.get_top(self.r_pad_id)) / self.c.get_height(self.r_pad_id)
				add_speed = self.game.right_pad.speed / 2
				self._change_side()
				self._bounce("pad", alpha, add_speed)
			else:
				# Right user loose, respawn ball
				self.game.win("left")
		elif b_left <= self.ss.PAD_W:
			# And left
			if self.c.check_collision(self.id, self.l_pad_id, balls=True):
				alpha = (b_center_y - self.c.get_top(self.l_pad_id)) / self.c.get_height(self.l_pad_id)
				add_speed = self.game.left_pad.speed / 2
				self._change_side()
				self._bounce("pad", alpha, add_speed)
			else:
				self.game.win("right")
		# Executed, when ball moves out from field
		# Move it to the edge
		elif b_right > self.ss.WIDTH / 2:
			self.c.move(self.id, self.ss.RIGHT_TAB-b_right, self.y_speed)
		else:
			self.c.move(self.id, -b_left+self.ss.PAD_W, self.y_speed)

		# bounce from top or bottom
		if (b_top + self.y_speed < 0 and self.y_speed < 0) or \
				(b_bot + self.y_speed > self.ss.HEIGHT and self.y_speed > 0):
			self._bounce("wall")
			
		
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
		
	
	def _bounce(self, source, alpha=None, add_speed=None):
		# source = "pad" if bounce from pad else "wall"
		# 0 <= alpha <= 1	-	change of y_speed 
		# add_speed		- 	impulse added by pad
		if source == "pad":
			self.y_speed = alpha*30 - 15 + add_speed
			if abs(self.x_speed) < self.ss.BALL_MAX_SPEED:
				self.x_speed *= -self.ss.SPEED_UP_BALL
			else:
				self.x_speed = -self.x_speed
		else:
			self.y_speed = -self.y_speed
			
	def _get_side(self):
		if self.x_speed > 0:
			return "left"
		elif self.x_speed < 0:
			return "right"
			
	def _change_side(self):
		if self.side == "left":
			self.side = "right"
		else:
			self.side = "left"
			
