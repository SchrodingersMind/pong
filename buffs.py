from random import choice, randint
from tkinter import PhotoImage, NORMAL
from os import sep

from theme import get_random_color
from extend import Player

class Buff:
	# Constant object, that store in Buffs.buffs list
	def __init__(self, image, image_duration, effect_duration, func, args=0, repeated=0):
		""" Create object, that represent buff """
		self._image = PhotoImage(file="images"+sep+image)
		self.image_duration = image_duration
		
		self.effect_duration = effect_duration
		
		self._func = func
		self._args = args
		self._repeat = repeated
		
		
class AliveBuff:
	# Object, that currently take part in game (shown or makes effect)
	STATE_POPS_UP = 0
	STATE_ACTIVATED = 1
	STATE_DEAD = 2
	
	def __init__(self, x, y, canva, base_buff):
		
		self.x = x
		self.y = y
		
		self.opts = base_buff
		
		self.id = canva.create_image((x, y), image=self.opts._image, state=NORMAL)
		self.c = canva
		
		self.state = AliveBuff.STATE_POPS_UP
		self.counter = 0
		
	def update(self):
		self.counter += 1
		
		if self.state == AliveBuff.STATE_POPS_UP and \
				self.counter == self.opts.image_duration:
			self.die()
		elif self.state == AliveBuff.STATE_ACTIVATED:
			if self.counter == self.opts.effect_duration:
				self.die()
			elif self.opts._repeat != 0 and \
					self.counter%self.opts._repeat == 0:
				self._call_func()
		
	def activate(self, *args):
		# Activate effect taken by buff
		self.c.delete(self.id)
		self.state = AliveBuff.STATE_ACTIVATED
		if self.opts._args == 1:
			self.side = args[0]
		self._call_func()
		
		self.counter = 0
		
			
	def _call_func(self, revert=False):
		if self.opts._args == 0:
			self.opts._func(revert=revert)
		elif self.opts._args == 1:
			self.opts._func(self.side, revert=revert)
		else:
			pass	# Silence is golden...
			
	def die(self):
		if self.state == AliveBuff.STATE_POPS_UP:
			self.c.delete(self.id)
		elif self.state == AliveBuff.STATE_ACTIVATED:
			self._call_func(True)
		self.state = AliveBuff.STATE_DEAD
		

class Buffs:
	# Speed up pod	- DONE
	# Slow down pod	- DONE
	# Blur enemy's side - DONE
	# Change pad size - DONE
	# Speed up ball - MAYBE DEL
	# Change pad's control keys - DONE
	# Change ball size - DONE
	# One-time block at center
	# Timed block behind pod
	# Ball change direction and speed to random
	# "Drunk" ball
	
	def __init__(self, sizes, game):
		
		self.ss = sizes
		self.game = game
		self.c = game.c
		
		self.init_buffs()
		
		self._active_buffs = []
		
		# Maybe save it in Pad class??
		self.l_pad_speed_up = 1
		self.r_pad_speed_up = 1
		
		self.l_pad_rotated = False
		self.r_pad_rotated = False
		
		# Here store ids of black rectangulars, in order to than remove it
		self._blured = [] 
		
		self.l_splash_id = 0
		self.r_splash_id = 0
		
		self.l_pad_h = 1
		self.r_pad_h = 1
		
		
	def update(self, ball_id):
		# Add buff to the screen
		if self._freq != 0 and randint(1, self._freq) == 1:
			buff = choice(self._buffs)
			x_coord = randint(0, self.ss.WIDTH*3//5) + self.ss.WIDTH/5
			y_coord = randint(50, int(self.ss.HEIGHT)-50)
			self._active_buffs.append(AliveBuff(x_coord, y_coord, self.c, buff))
			
		# Remove dead
		self._active_buffs = [buff for buff in self._active_buffs if buff.state != AliveBuff.STATE_DEAD]
		
		# Update all
		for buff in self._active_buffs:
			if buff.state == AliveBuff.STATE_POPS_UP and \
					self.c.check_collision(ball_id, buff.id):
				buff.activate(self.game.player.id)
			buff.update()
			
	def desactivate(self):
		""" Clear all buff from game """
		for buff in self._active_buffs:
			buff.die()
		
		self._freq = 0
		
					### It would called when ball enters buffs image zone ###
	
	def _speed_up_pad(self, side, revert=False):
		if side == Player.LEFT:
			self.l_pad_speed_up *= 2 if not revert else 0.5
		elif side == Player.RIGHT:
			self.r_pad_speed_up *= 2 if not revert else 0.5
		
	def _slow_down_pad(self, side, revert=False):
		# Ha-ha, I am genius, again
		self._speed_up_pad(side, not revert)
			
	def _blur(self, side, revert=False):
		""" Blur opponent field """
		if side == Player.LEFT:
			if not revert:
				rect_id = self.c.create_rectangle(self.ss.WIDTH/2, 0,
												  self.ss.RIGHT_TAB, self.ss.HEIGHT,
												  fill="black")
				self._blured.append(rect_id)
			else:
				rect_id = self._blured.pop(0)
				self.c.delete(rect_id)
		elif side == Player.RIGHT:
			if not revert:
				rect_id = self.c.create_rectangle(self.ss.PAD_W, 0,
												  self.ss.WIDTH/2, self.ss.HEIGHT,
												  fill="black")
				self._blured.append(rect_id)
			else:
				rect_id = self._blured.pop(0)
				self.c.delete(rect_id)
				
	def _enlarge(self, side, revert=False):
		""" Make pad bigger """
		scale = 2 if not revert else 0.5
		if side == Player.LEFT:
			self.c.scale_center(self.game.left_pad.id, 1, scale)
		elif side == Player.RIGHT:
			self.c.scale_center(self.game.right_pad.id, 1, scale)
		
	def _shrink(self, side, revert=False):
		""" Opposite to previous """
		self._enlarge(side, not revert)
			
	def _ball_small(self, revert=False):
		""" The same for ball """
		if not revert and self.ss.BALL_RADIUS > 3:
			self.ss.BALL_RADIUS /= 2
			self.c.scale_center(self.game.ball.id, 0.5)
		elif self.ss.HEIGHT/4 > self.ss.BALL_RADIUS:
			self.ss.BALL_RADIUS *= 2
			self.c.scale_center(self.game.ball.id, 2)
			
	def _ball_big(self, revert=False):
		self._ball_small(not revert)
		
	def _ball_teleport(self, revert=False):
		""" Teleport to radom location without changing speed or direction """
		if not revert:
			self.game.ball.teleport()
			
	def _die(self, side, revert=False):
		if not revert:
			self.game.loose()
				
	def _rotate(self, side, revert=False):
		""" Change controls (Up/Down) for pad in <side> """
		if side == Player.LEFT:
			self.game.left_pad.rotate_controls()
			self.l_pad_rotated = not self.l_pad_rotated
			if self.l_pad_rotated:
				self.game.theme.pin_color("l_pad", "#327045")
			else:
				self.game.theme.unpin_color("l_pad")
		else:
			self.game.right_pad.rotate_controls()
			self.r_pad_rotated = not self.r_pad_rotated
			if self.r_pad_rotated:
				self.game.theme.pin_color("r_pad", "#327045")
			else:
				self.game.theme.unpin_color("r_pad")
			
	def _choose_random_buff(self, side, revert=False):
		if not revert:
			buff = choice(self._buffs)
			a_buff = AliveBuff(0, 0, self.c, buff)
			a_buff.activate(side)
			self._active_buffs.append(a_buff)
			
	def _splash(self, side, revert=False):
		def __check(side_check, spl_id):
			if side == side_check:
				if revert:
					self.c.delete(spl_id)
					return 0
				elif spl_id == 0:
					new_id = self.c.create_rectangle((0, 0, self.ss.WIDTH/2, self.ss.HEIGHT), 
																			fill="white")
					if side == Player.RIGHT:
						self.c.move(new_id, self.ss.WIDTH/2, 0)
					self.c.tag_lower(new_id)
					return new_id
				else:
					self.c.itemconfig(spl_id, fill=get_random_color())
			return spl_id
			
		self.l_splash_id = __check(Player.LEFT, self.l_splash_id)
		self.r_splash_id = __check(Player.RIGHT, self.r_splash_id)
		
	def _move_screen(self, revert=False):
		if not revert:
			self.game.move_screen()
			
						###		End of buffs effects section	### 

	def init_buffs(self):
		
		buffs_1 = ( ("green.png", 180, 100, self._speed_up_pad, 1),
					("red.png", 180, 100, self._slow_down_pad, 1),
					("enlarge.png", 140, 90, self._enlarge, 1),
					("shrink.png", 140, 90, self._shrink, 1) )
					   	
		buffs_2 = ( ("ball_red.png", 200, 130, self._ball_small),
					("ball_green.png", 200, 130, self._ball_big),
					("question.png", 200, 1, self._choose_random_buff, 1) )
		
		buffs_3 = ( ("rotate.png", 200, 100, self._rotate, 1),  # how to make it more visible????
					#("blur.png", 180, 50, self.blur, 1),	Not shown in some themes ☹️
					("die2.png", 100, 1, self._die, 1) ) 
					
		buffs_4 = ( ("teleport.png", 200, 1, self._ball_teleport),
					("splashes.png", 150, 200, self._splash, 1, 10),
					("move.png", 100, 50, self._move_screen, 0, 20) )
		
		if self.game.CRAZY.it == 0:
			self._freq = 0
			buff_list = []
		elif self.game.CRAZY.it == 1:
			self._freq = 250
			buff_list = buffs_1
		elif self.game.CRAZY.it == 2:
			self._freq = 100
			buff_list = buffs_1 + buffs_2
		elif self.game.CRAZY.it == 3:
			self._freq = 10
			buff_list = buffs_1 + buffs_2 + buffs_3
		elif self.game.CRAZY.it == 4:
			self._freq = 10
			buff_list = buffs_1 + buffs_2 + buffs_3 + buffs_4
			
		self._buffs = [Buff(*arg) for arg in buff_list]


		
