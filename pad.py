

class Pad(object):
	def __init__(self, mine_id, canva, sizes, controls, p_id, bot=False):
		self.speed = 0
		self.c = canva
		self.id = mine_id
		
		self.ss = sizes
		
		self._key_up = controls[0]
		self._key_down = controls[1]
		
		self.p_id = p_id
		
		self.bot = bot
		
	def move(self, ball_center=None, speed_up=1):
		def get_speed():
			return self.speed * speed_up
			
		if not self.bot:
			# if not (pad out of box and continue moving from box)
			if not (self.c.get_top(self.id) <= 0 and self.speed <= 0) and \
					not (self.c.get_down(self.id) >= self.c.get_height() and \
						self.speed >= 0):
				self.c.move(self.id, 0, get_speed())
		else:
			offset = self.ss.BALL_RADIUS/2
			# Crash when pad_h<15
			if ball_center > self.c.get_down(self.id)-offset:
				self.c.move(self.id, 0, self.ss.PAD_SPEED*speed_up)
			elif ball_center < self.c.get_top(self.id)+offset:
				self.c.move(self.id, 0, -self.ss.PAD_SPEED*speed_up)
				
				
	def button_press(self, keysym):
		if self.bot:
			# Nothing could change AI intentions
			return
			
		if keysym == self._key_up:
			self.speed = -self.ss.PAD_SPEED
		elif keysym == self._key_down:
			self.speed = self.ss.PAD_SPEED
			
	def button_release(self, keysym):
		if self.bot:
			# Nothing could change AI intentions
			return
			
		if keysym == self._key_up or keysym == self._key_down:
			self.speed = 0

	def rotate_controls(self):
		k_up = self._key_up
		self._key_up = self._key_down
		self._key_down = k_up





