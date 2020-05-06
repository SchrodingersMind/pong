from sizes import Size
from theme import Theme
from ball import Ball
from pad import Pad
from menu import StopMenu, StartMenu
from buffs import Buffs

from tkinter import *

# TODO's
# - add scale - DONE
# - add music - AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# - add settings
# - - theme			- DONE
# - - sound on/off	- DEL
# - - screen size	- DONE
# - startup menu
# - - play standart		- DONE
# - - player vs computer - DONE
# - - help 				- +-
# - set ball as image
# - add bonuses and (de)buffs - DONE

class ExCanvas(Canvas):
	""" Make life better and code more understable """
	def get_top(self, item_id):
		return self.bbox(item_id)[1]
	def get_down(self, item_id):
		return self.bbox(item_id)[3]
	def get_left(self, item_id):
		return self.bbox(item_id)[0]
	def get_right(self, item_id):
		return self.bbox(item_id)[2]
		
	def get_x_center(self, item_id):
		return (self.get_left(item_id) + self.get_right(item_id)) / 2
	def get_y_center(self, item_id):
		return (self.get_top(item_id) + self.get_down(item_id)) / 2
		
	def get_height(self, item_id=None):
		if not item_id:
			# Return height of canvas
			return int(self.config()["height"][-1])
		else:
			return self.get_down(item_id) - self.get_top(item_id)
			
	def scale_center(self, item_id, xscale, yscale=None):
		""" Scale object, don't changing it's center """
		if not yscale:
			yscale = xscale
		old_x = self.get_x_center(item_id)
		old_y = self.get_y_center(item_id)
		self.scale(item_id, 0, 0, xscale, yscale)
		new_x = self.get_x_center(item_id)
		new_y = self.get_y_center(item_id)
		dx, dy = old_x-new_x, old_y-new_y
		self.move(item_id, dx, dy)
		
	def ball_coords(self, item_id, x, y, r=None):
		""" Set ball center at (x,y) and radius to r """
		if not r:
			# Move ball without changing radius
			cur_x = self.get_x_center(item_id)
			cur_y = self.get_y_center(item_id)
			self.move(item_id, x-cur_x, y-cur_y)
		else:
			self.coords(item_id, x-r, y-r, x+r, y+r)
			
	def check_collision(self, id1, id2, balls=True):
		""" id1,2 - items id
			balls - if True, do check by centers and 
						compare it with radius(height/2)
					otherwise, compare like squares
		"""
		if balls:
			#print(self.bbox(id2), self.bbox(id1))
			dist = (self.get_height(id1) + self.get_height(id2)) / 2
			dy = self.get_y_center(id1) - self.get_y_center(id2)
			dx = self.get_x_center(id1) - self.get_x_center(id2)
			return dist**2 > dy**2 + dx**2
		else:
			elems = self.find_overlapping(*self.bbox(id1))
			return id2 in elems
		

class Game:
	
	def __init__(self):
		
		self.ss = Size()
		self.pos_whs_iter = 0
		
		self.theme = Theme()
		
		# TODO use it, add buff's set, improve last one
		### CRAZY COULD BE:
			# 0 - Boring. Very boring. Classical pong
			# 1 - Better than prev. Buffs appeared 1 time a 30*250 ms
			# 2 - If you don't know what to choose, use it. Buffs appeared 1 time a 30*100 ms
			# 3 - <del>CRAZIEST</del> FUNNIEST CHOICE EVER. BUFFS APEARED 1 TIME A 0.3 S
			# 4 - epileptic
			
		self.CRAZY = 3
		
	
		###			Drawable and Window params
		# root window
		self.root = Tk()
		self.root.title("Pong")
		
		self.__init_canva()
		###			End of previous part
		
		self.c.bind("<KeyPress>", self.key_pressed)
		
		self.c.bind("<KeyRelease>", self.key_released)
		
		
		
		###			Game's options		
		self.player_1_score = 0
		self.player_2_score = 0
		
		self.game_stopped = True
		
		self.root.mainloop()
	
	def run(self, vs_bot):
		self.vs_bot = vs_bot
		self.left_pad.bot = vs_bot
		self._stop_cont_game()
		self.cur_menu = self.stop_menu
		self.main()
	
	def main(self):
		if not self.game_stopped:
			self.ball.move()
			self.right_pad.move(speed_up=self.buffs.r_pad_speed_up)
			self.buffs.update(self.ball.id, self.ball.side)
			if self.vs_bot:
				self.left_pad.move(self.c.get_y_center(self.ball.id), \
									self.buffs.l_pad_speed_up)
			else:
				self.left_pad.move(speed_up=self.buffs.l_pad_speed_up)
		# recall himself every 30 ms
		self.root.after(30, self.main)
	
	def win(self, player):
		self.update_score(player)
		self.ball.spawn_ball()
		
	def update_score(self, player):
		if player == "right":
			self.player_1_score += 1
			self.c.itemconfig(self.p_1_text, text=self.player_1_score)
		else:
			self.player_2_score += 1
			self.c.itemconfig(self.p_2_text, text=self.player_2_score)
			
			
	def key_pressed(self, event):	
		if not self.game_stopped:
			# If ball and pads can move
			self.left_pad.button_press(event.keysym)
			self.right_pad.button_press(event.keysym)
			if event.keysym == "Escape":
				# Show/Hide menu window and stop/start game
				self._stop_cont_game()
		else:
			# Send this key to menu widget
			self.cur_menu.check_keys(event.keysym)

			
			
	def key_released(self, event):
		if not self.game_stopped:
			self.left_pad.button_release(event.keysym)
			self.right_pad.button_release(event.keysym)

	
	def rotate_size(self, d_iter):
		# d_iter - changing offset for iterator -1 or 1
		w,h = self.ss.POSSIBLE_WHS[self.pos_whs_iter]
		self.pos_whs_iter += d_iter
		self.pos_whs_iter %= len(self.ss.POSSIBLE_WHS)
		new_w, new_h = self.ss.POSSIBLE_WHS[self.pos_whs_iter]
		xscale, yscale = new_w/w, new_h/h
		self._resize(xscale, yscale)
		
				
	def _resize(self, xscale, yscale):
		self.c.config(width=self.ss.WIDTH*xscale, height=self.ss.HEIGHT*yscale)
		self.c.scale(ALL, 0, 0, xscale, yscale)
		self.ss.scale(xscale, yscale)
		
		
	def rotate_colors(self):
		self.stop_menu.rotate_colors()
		self.theme.rotate_colors(self.c)
	
			
	# Used for testing, shoud be deleted	
	def print_help(self):
		print("TODO!! Print it on main window")
		print("Controls: left player - W/S, right - key Up/Down")
		print("When played against bot you are right")
		print("After start, press Esc to see more options")	
		
	def _stop_cont_game(self):
		if self.game_stopped:
			self.c.itemconfig(self.cur_menu.id, state=HIDDEN)
		else:
			self.c.itemconfig(self.cur_menu.id, state=NORMAL)
		self.game_stopped = not self.game_stopped
	
		
	def __init_canva(self):
		# Canvas object
		self.c = ExCanvas(self.root, width=self.ss.WIDTH, height=self.ss.HEIGHT, background=self.theme.bg)
		self.c.pack(expand=True)
		 
	 
		# left line
		self.c.create_line(self.ss.PAD_W, 0, self.ss.PAD_W, self.ss.HEIGHT, fill=self.theme.line, tag="line")
		# right line
		self.c.create_line(self.ss.WIDTH-self.ss.PAD_W, 0, self.ss.WIDTH-self.ss.PAD_W, 
							self.ss.HEIGHT, fill=self.theme.line, tag="line")
		# central line
		self.c.create_line(self.ss.WIDTH//2, 0, self.ss.WIDTH//2, 
							self.ss.HEIGHT, fill=self.theme.line, tag="line")
		
		
		self.buffs = Buffs(self.ss, self)
		
		# Work with Pads
		left_pad_id = self.c.create_rectangle(0, 0, self.ss.PAD_W, 
										self.ss.PAD_H, width=1, fill=self.theme.l_pad, tag="l_pad")
		 
		right_pad_id = self.c.create_rectangle(self.ss.WIDTH-self.ss.PAD_W, 0, self.ss.WIDTH, 
									  self.ss.PAD_H+100, width=1, fill=self.theme.r_pad, tag="r_pad")
								  
		self.left_pad = Pad(left_pad_id, self.c, self.ss, ("w", "s"))
		self.right_pad = Pad(right_pad_id, self.c, self.ss, ("Up", "Down"))
		
		
		self.ball = Ball(self.c, left_pad_id, right_pad_id, self, self.ss, self.theme.ball)
		
		
	
		# TODO change font
		# Show players score
		self.p_1_text = self.c.create_text(self.ss.WIDTH*5/6, self.ss.PAD_H/4,
										 text=0,
										 font="Colibri 20",
										 fill="white",
										 tag="text")
		 
		self.p_2_text = self.c.create_text(self.ss.WIDTH/6, self.ss.PAD_H/4,
										  text=0,
										  font="Colibri 20",
										  fill="white",
										  tag="text")
		
		# Now unused								  
		self.start_text = self.c.create_text(self.ss.WIDTH/2, self.ss.HEIGHT/3,
											text="Press any key to start\r\n(Later use Esc to call menu)",
											font="Colibri 20",
											justify=CENTER,
											fill="white",
											state=HIDDEN)
		
		# Menu creating
		stop_menu_id = self.c.create_window((self.ss.WIDTH/2, self.ss.HEIGHT/2))
		self.stop_menu = StopMenu(stop_menu_id, self)
		self.c.itemconfig(stop_menu_id, window=self.stop_menu, state=HIDDEN)
		
		start_menu_id = self.c.create_window((self.ss.WIDTH/2, self.ss.HEIGHT/2))
		self.start_menu = StartMenu(start_menu_id, self)
		self.c.itemconfig(start_menu_id, window=self.start_menu) 
		
		self.cur_menu = self.start_menu
										  
		self.c.focus_set()
		
	



game = Game()



