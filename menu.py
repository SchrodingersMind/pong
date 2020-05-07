from tkinter import *


class BaseMenu(Frame):
	def __init__(self, buttons, menu_id):
		Frame.__init__(self, bg="")
		
		self.norm_color = "#b9b9b9"
		self.dis_color = "#2b2b2b"
		self.butts = []
		for ind, opts in enumerate(buttons):
			text, function = opts
			b = Button(self, text=text, command=function, padx=20, bg=self.dis_color, activebackground=self.norm_color)
			b.bind("<Enter>", self.swap_active)		# trigers when mouse entered on this object
			b.pack(anchor=CENTER, fill=X, pady=10)
			self.butts.append(b)
			
		self.butts[0].config(bg=self.norm_color)
		self.active = 0
		self.n_butts = len(self.butts)
			
		self.id = menu_id
		#self.pack()
		
	def check_keys(self, key):
		if key == "Up":
			self.move_up()
		elif key == "Down":
			self.move_down()
		elif key == "Return":
			self.choose()
				
	def move_down(self):
		self.swap_active(self.active+1)
	
	def move_up(self):
		self.swap_active(self.active-1)
		
		
	def choose(self):
		self.butts[self.active].invoke()
		
	def swap_active(self, en_ind):
		self.butts[self.active].config(bg=self.dis_color)
		if type(en_ind) == int:
			self.active = en_ind%self.n_butts
		else:
			self.active = self.butts.index(en_ind.widget)
		self.butts[self.active].config(bg=self.norm_color)
			
			
			
class StopMenu(BaseMenu):
	# Pops up when user press Esc key
	def __init__(self, menu_id, game_class):
		
		self.game = game_class
		buttons = (("Continue", game_class._stop_cont_game),
						 (self._get_wh_to_str(), lambda: None),
						 ("Randomize colors", self.randomize_colors),
						 ("Rotate theme", self.rotate_theme),
						 ("Quit", game_class.root.quit))
						 
		BaseMenu.__init__(self, buttons, menu_id)
		
		self.norm_color = self.game.theme["menu_butts_on"]
		self.dis_color = self.game.theme["menu_butts_off"]
		
	def check_keys(self, key):
		BaseMenu.check_keys(self, key)
		
		if self.active == 1:
			if key == "Left":
				self.game.rotate_size(-1)
				self.butts[1].config(text=self._get_wh_to_str())
			elif key == "Right":
				self.game.rotate_size(1)
				self.butts[1].config(text=self._get_wh_to_str())
				
		if key == "Escape":
			self.game._stop_cont_game()
				
				
		
	def _get_wh_to_str(self):
		# Return string for rotate_size_Button
		width, height = self.game.ss.POSSIBLE_WHS[self.game.pos_whs_iter]
		return "< "+str(width)+"x"+str(height)+" >"
		
	def rotate_theme(self):
		self.game.theme.next_theme()
		self.game.rotate_colors()
		
	def randomize_colors(self):
		self.game.theme.randomize()
		self.game.rotate_colors()
		
	def rotate_colors(self):
		# Change buttons color
		self.norm_color = self.game.theme["menu_butts_on"]
		self.dis_color = self.game.theme["menu_butts_off"]
		for butt in self.butts:
			butt.config(bg=self.dis_color, activebackground=self.norm_color)
		self.butts[self.active].config(bg=self.norm_color)
	
		
class StartMenu(BaseMenu):
	def __init__(self, menu_id, game_class):
		buttons = (("Play vs opponent", lambda: game_class.run(False)),
					("Play vs computer", lambda: game_class.run(True)),
					("Help", game_class.print_help),
					("Quit", game_class.root.quit))
		BaseMenu.__init__(self, buttons, menu_id)
		
		self.game = game_class
		

