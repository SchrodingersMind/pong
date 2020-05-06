import random

class Ball(object):
	def __init__(self, canva, l_pad_id, r_pad_id, game, sizes, theme):
		self.c = canva
		
		self.x_speed = sizes.BALL_X_SPEED
		self.y_speed = sizes.BALL_Y_SPEED
				
		self.l_pad_id = l_pad_id
		self.r_pad_id = r_pad_id
		
		self.game = game
		self.ss = sizes	# Class with bunch of objects sizes
		
		self.id = self.c.create_oval((self.ss.WIDTH-self.ss.BALL_RADIUS)/2,
									(self.ss.HEIGHT-self.ss.BALL_RADIUS)/2,
									(self.ss.WIDTH+self.ss.BALL_RADIUS)/2,
									(self.ss.HEIGHT+self.ss.BALL_RADIUS)/2, fill=theme, tag="ball")

		
		self.side = self._get_side()
		
	def spawn_ball(self):
		# Called at start of match or after goal 
		
		# Set ball at the center
		half_width = self.ss.WIDTH/2
		half_height = self.ss.HEIGHT/2
		half_size = self.ss.BALL_RADIUS/2
		#self.c.coords(self.id, half_width-half_size,
		#				half_height-half_size,
		#				half_width+half_size,
		#				half_height+half_size)
		self.c.ball_coords(self.id, half_width, half_height)
		# Set direction to looser and slow down x_speed to initial, y_speed to zero (should move horizontally)
		self.x_speed = -self.ss.INITIAL_SPEED if self.x_speed < 0 else self.ss.INITIAL_SPEED
		self.y_speed = 0
		
		
	def bounce(self, action, alpha=None, add_speed=None):
		# action = "strike" if bounce from pad else "ricochet"
		# 0 <= alpha <= 1	-	change of y_speed 
		# add_speed		- 	impulse added by pad
		if action == "strike":
			self.y_speed = alpha*30 - 15 + add_speed
			if abs(self.x_speed) < self.ss.BALL_MAX_SPEED:
				self.x_speed *= -self.ss.BALL_SPEED_UP
			else:
				self.x_speed = -self.x_speed
		else:
			self.y_speed = -self.y_speed
			
	def move(self):
		ball_left, ball_top, ball_right, ball_bot = self.c.coords(self.id)
		ball_center = (ball_top + ball_bot) / 2
 	

		# If nothing special - move ball
		if ball_right + self.x_speed < self.ss.RIGHT_TAB and \
				ball_left + self.x_speed > self.ss.PAD_W:
			self.c.move(self.id, self.x_speed, self.y_speed)
		# Touched left or right line (inner side of pad)
		elif ball_right == self.ss.RIGHT_TAB or ball_left == self.ss.PAD_W:
			off = 3
			# Right side
			if ball_right > self.ss.WIDTH / 2:
				# Check if ball center is between top and bottom of pad
				# off added for cases, for ex. when pad bottom between ball top and center
				if self.c.get_top(self.r_pad_id)-off <= ball_center <= self.c.get_down(self.r_pad_id)+off:
					alpha = (ball_center - self.c.get_top(self.r_pad_id)) / self.ss.PAD_H
					add_speed = self.game.right_pad.speed / 3
					self._change_side()
					self.bounce("strike", alpha, add_speed)
				else:
					# Right user loose, respawn ball
					self.game.win("left")
			else:
				# And left
				if self.c.get_top(self.l_pad_id)-off <= ball_center <= self.c.get_down(self.l_pad_id)+off:
					alpha = (ball_center - self.c.get_top(self.l_pad_id)) / self.ss.PAD_H
					add_speed = self.game.left_pad.speed / 3
					self._change_side()
					self.bounce("strike", alpha, add_speed)
				else:
					self.game.win("right")
		# Executed, when ball moves out from field
		# Move it to the edge
		else:
			if ball_right > self.ss.WIDTH / 2:
				self.c.move(self.id, self.ss.RIGHT_TAB-ball_right, self.y_speed)
			else:
				self.c.move(self.id, -ball_left+self.ss.PAD_W, self.y_speed)
		# Bounce from top or bottom
		if ball_top + self.y_speed < 0 or ball_bot + self.y_speed > self.ss.HEIGHT:
			self.bounce("ricochet")
			
		
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
			
