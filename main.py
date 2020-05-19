from tkinter import *
from random import randint

from sizes import Size
from theme import Theme
from ball import Ball
from pad import Pad
from menu import StopMenu, StartMenu, OptionMenu
from buffs import Buffs
from extend import PositionList, ExCanvas, Player


# TODO's
# - add scale - DONE
# - add music - AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# - add settings
# - - theme			- +-
# - - sound on/off	- DEL (in Linux most libraries didn't work from-the-box)
# - - screen size	- DONE
# - startup menu
# - - play standart		- DONE
# - - player vs computer - DONE
# - - help 				- +-
# - set ball as image
# - add bonuses and (de)buffs - DONE
# - options menu (with size, theme, crazy params)
# - add coments


class Game:
	
	def __init__(self):
		
		self.ss = Size()
		
		self.theme = Theme()
		
		### CRAZY COULD BE:
			# 0 - Boring. Very boring. Classical pong
			# 1 - Better than prev. Buffs appeared 1 time a 30*250 ms
			# 2 - If you don't know what to choose, use it. Buffs appeared 1 time a 30*100 ms
			# 3 - <del>CRAZIEST</del> FUNNIEST CHOICE EVER. BUFFS APEARED 1 TIME A 0.3 S
			# 4 - epileptic
			
		self.CRAZY = PositionList(("Classic", "Soft", "Normal", "Best", "Hard"), 2) 

		# root window
		self.root = Tk()
		self.root.title("FPong")
		self.root.geometry("+0+0")
		self.root.iconphoto(False, PhotoImage(file="./images/window_icon.png"))
		self.root.resizable(False, False)
		
		# Create Canvas wit elements on it
		self.__init_canva()

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
			self.buffs.update(self.ball.id)
			if self.vs_bot:
				self.left_pad.move(self.c.get_y_center(self.ball.id), \
									self.buffs.l_pad_speed_up)
			else:
				self.left_pad.move(speed_up=self.buffs.l_pad_speed_up)
		# recall himself every 30 ms
		self.after_id = self.root.after(30, self.main)
	
	def win(self):
		self._increase_score(self.player.id)
		self.ball.respawn_ball()
		
	def loose(self):
		self._increase_score(self.player.other.id)
		
	def _increase_score(self, player):
		if player == Player.LEFT:
			self.player.l_player.score += 1
			self.c.itemconfig(self.pl_l_text, text=self.player.l_player.score)
		else:
			self.player.r_player.score += 1
			self.c.itemconfig(self.pl_r_text, text=self.player.r_player.score)
			
			
	def _key_pressed(self, event):	
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

			
			
	def _key_released(self, event):
		if not self.game_stopped:
			self.left_pad.button_release(event.keysym)
			self.right_pad.button_release(event.keysym)

	def show_options_menu(self, hide=False):
		self.c.itemconfig(self.cur_menu.id, state=HIDDEN)
		if not hide:
			self.cur_menu = self.options_menu
		else:
			self.cur_menu = self.start_menu
		self.c.itemconfig(self.cur_menu.id, state=NORMAL)
		
	def update_size(self):
		new_w, new_h = self.ss.SCREEN_SIZES.get()
		xscale = new_w / self.ss.WIDTH
		yscale = new_h / self.ss.HEIGHT
		self._resize(xscale, yscale)
		
				
	def _resize(self, xscale, yscale):
		self.c.config(width=self.ss.WIDTH*xscale, height=self.ss.HEIGHT*yscale)
		self.c.scale(ALL, 0, 0, xscale, yscale)
		self.ss.scale(xscale, yscale)
		
	def update_crazy(self):
		self.buffs.init_buffs()
		
		
	def update_theme(self):
		if not self.theme.randomed:
			self.theme.choose_theme()
		self.rotate_colors()
		
	def rotate_colors(self):
		self.start_menu.rotate_colors()
		self.stop_menu.rotate_colors()
		self.options_menu.rotate_colors()
		self.theme.rotate_colors()
		
	def move_screen(self):
		left = 0
		right = self.root.winfo_screenwidth() - int(self.ss.WIDTH)
		top = 0
		bottom = self.root.winfo_screenheight() - int(self.ss.HEIGHT)
		new_x = randint(left, right)
		new_y = randint(top, bottom)
		self.root.geometry(f"+{new_x}+{new_y}")
		
	def _stop_cont_game(self):
		if self.game_stopped:
			self.c.itemconfig(self.cur_menu.id, state=HIDDEN)
		else:
			self.c.itemconfig(self.cur_menu.id, state=NORMAL)
		self.game_stopped = not self.game_stopped
	
			
	# Used for testing, shoud be changed	
	def print_help(self):
		# TODO!! Print it on main window
		print("Welkome to the F(unny)Pong")
		print()
		print("Controls: left player - W/S, right - key Up/Down")
		print("When playing against bot you are on the right")
		print("At the time of game you could press Esc to go to the menu")
		print()
		print("There are 5 modes: Classic, Soft, Normal, Best, Hard")
		print("\tClassic - Without buffs")
		print("\tSoft - Sometimes minor buffs appear(Speed_up, Slow_down, Enlarge, Shrink)(all about pad)")
		print("\tNormal - Buffs pops up more frequently, and to previous list added (Small_ball, Big_ball, Random)")
		print("\tBest - Frequency increases, added (Rotate, Die)")
		print("\t\t\tMaybe I played this game so many times(while debugging) so that all the previous modes became boring")
		print("\t\t\t<Best> is the best - In My Humble Oppinion")
		print("\tHard - Added (Teleport, Splash, Move)")
		print()
		print("Note: in most cases buffs affect the player who touched the ball last")
		print("Except some general (Small_ball, Big_ball, Teleport, Move)")
		print()
		print("Some non-intuitive buffs:")
		print("\tRandom - (question mark) execute random buff")
		print("\tRotate - change pad control keys (when you press Up, it moves down) and color to dark-green")
		print("\tTeleport - change balls position")
		print("\tSplash - (white, green, red, black stripes) Cause blinking in your area")
		print("\tMove - (four arrows) Screen moves several times")	
		
	
	def reinit(self):
		self.__init_canva()
		
	def __init_canva(self):
		# Canvas object
		self.c = ExCanvas(self.root, width=self.ss.WIDTH, 
							height=self.ss.HEIGHT, background=self.theme["bg"])
		self.c.pack()#expand=True)
		 
		# central line
		self.c.create_line(self.ss.WIDTH//2, 0, self.ss.WIDTH//2, 
							self.ss.HEIGHT, fill=self.theme["line"], tag="line")
							
		self.c.create_ball(self.ss.WIDTH//2, self.ss.HEIGHT//2, self.ss.BALL_RADIUS/2, 
							fill=self.theme["line"], width=0, tag="line")
		
		
		self.__init_players_score()
		
		# Work with Pads
		left_pad_id = self.c.create_rectangle(0, 0, self.ss.PAD_W, 
											self.ss.PAD_H, width=1, 
											fill=self.theme["l_pad"], tag="l_pad")
		 
		right_pad_id = self.c.create_rectangle(self.ss.WIDTH-self.ss.PAD_W, 0, self.ss.WIDTH, 
									  		self.ss.PAD_H, width=1, 
									  		fill=self.theme["r_pad"], tag="r_pad")
								  
		self.left_pad = Pad(left_pad_id, self.c, self.ss, ("w", "s"), Player.LEFT)
		self.right_pad = Pad(right_pad_id, self.c, self.ss, ("Up", "Down"), Player.RIGHT)
		
		self.player = Player(self.left_pad, self.right_pad)
		
		self.ball = Ball(self.c, self.player, self, self.ss, self.theme["ball"])
		
		
		self.buffs = Buffs(self.ss, self)
		
		# Menu creating
		stop_menu_id = self.c.create_window((self.ss.WIDTH/2, self.ss.HEIGHT/2))
		self.stop_menu = StopMenu(stop_menu_id, self)
		self.c.itemconfig(stop_menu_id, window=self.stop_menu, state=HIDDEN)
		
		options_menu_id = self.c.create_window((self.ss.WIDTH/2, self.ss.HEIGHT/2))
		self.options_menu = OptionMenu(options_menu_id, self)
		self.c.itemconfig(options_menu_id, window=self.options_menu, state=HIDDEN)
		
		start_menu_id = self.c.create_window((self.ss.WIDTH/2, self.ss.HEIGHT/2))
		self.start_menu = StartMenu(start_menu_id, self)
		self.c.itemconfig(start_menu_id, window=self.start_menu) 
		
		self.cur_menu = self.start_menu
										  
		self.c.focus_set()
		self.theme.set_canvas(self.c)
		
		self.c.bind("<KeyPress>", self._key_pressed)
		self.c.bind("<KeyRelease>", self._key_released)
		
		self.game_stopped = True
		
	def __init_players_score(self):
		# Show players score
		self.pl_r_text = self.c.create_text(self.ss.WIDTH*4/5, self.ss.PAD_H/3,
											text=0, fill="white",
											font="Colibri 25", tag="text")
		 
		self.pl_l_text = self.c.create_text(self.ss.WIDTH/5, self.ss.PAD_H/3,
											text=0, fill="white",
											font="Colibri 25", tag="text")
		
	

if __name__ == "__main__":
	game = Game()



