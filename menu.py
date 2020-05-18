from tkinter import *


class RotateButton(Button):
	def __init__(self, frame, func_left, func_right, func_apply, func_text, **kwargs):
		""" func_left - function to call, when user on it button and press key Left
			func_right - the same for Right
			func_text - function to get text for current button state
		"""
		# Now text changed automatically
		self.f_left = lambda: (func_left(), self.set_text())
		self.f_right = lambda: (func_right(), self.set_text())
		self.f_text = func_text
		Button.__init__(self, frame, text=func_text(), command=func_apply, **kwargs)
	
	def set_text(self):
		self.config(text=self.f_text())

class BaseMenu(Frame):
	def __init__(self, buttons, menu_id, norm_color="#b9b9b9", dis_color="#2b2b2b"):
		Frame.__init__(self, bg="")
		
		self.norm_color = norm_color
		self.dis_color = dis_color
		self.butts = []
		for text, funcs in buttons:
			if isinstance(funcs, tuple):
				b = RotateButton(self, *funcs, text, padx=20, bg=self.dis_color, activebackground=self.norm_color)
			else:
				b = Button(self, text=text, command=funcs, padx=20, bg=self.dis_color, activebackground=self.norm_color)
			b.bind("<Enter>", self.swap_active)		# trigers when mouse entered on this object
			b.pack(anchor=CENTER, fill=X, pady=10)
			self.butts.append(b)
			
		self.butts[0].config(bg=self.norm_color)
		self.active = 0
		self.n_butts = len(self.butts)
			
		self.id = menu_id
		#self.pack()
		
	def check_keys(self, key):
		cur_butt = self.butts[self.active]
		if key == "Up":
			self.move_up()
		elif key == "Down":
			self.move_down()
		elif key == "Return":
			self.choose()
			
		elif isinstance(cur_butt, RotateButton):
			if key == "Left":
				cur_butt.f_left()
			elif key == "Right":
				cur_butt.f_right()
			
	def move_down(self):
		self.swap_active(self.active+1)
	
	def move_up(self):
		self.swap_active(self.active-1)
		
	def choose(self):
		self.butts[self.active].invoke()
		
	def swap_active(self, en_ind):
		self.butts[self.active].config(bg=self.dis_color)
		if type(en_ind) == int:
			# When clicked Up/Down
			self.active = en_ind%self.n_butts
		else:
			# When mouse enter the button
			self.active = self.butts.index(en_ind.widget)
		self.butts[self.active].config(bg=self.norm_color)
		
	def rotate_buttons_color(self, norm_color, dis_color):
		# Should be called to change color
		self.norm_color = norm_color
		self.dis_color = dis_color
		for butt in self.butts:
			butt.config(bg=self.dis_color, activebackground=self.norm_color)
		self.butts[self.active].config(bg=self.norm_color)
		
	def set_button_text(self, text, pos=None):
		# if pos not set, change text for active button
		if not pos:
			pos = self.active
		self.butts[pos].config(text=text)
			

class StartMenu(BaseMenu):
	def __init__(self, menu_id, game_class):
		self.game = game_class
		
		buttons = (("Play vs opponent", lambda: game_class.run(False)),
					("Play vs computer", lambda: game_class.run(True)),
					("Options", game_class.show_options_menu),
					("Help", game_class.print_help),
					("Quit", game_class.root.quit))
					
		norm_color = self.game.theme["menu_butts_on"]
		dis_color = self.game.theme["menu_butts_off"]
		BaseMenu.__init__(self, buttons, menu_id)
		
	def rotate_colors(self):
		# Change buttons color
		norm_color = self.game.theme["menu_butts_on"]
		dis_color = self.game.theme["menu_butts_off"]
		self.rotate_buttons_color(norm_color, dis_color)
			
			
class StopMenu(BaseMenu):
	# Pops up when user press Esc key
	def __init__(self, menu_id, game_class):
		self.game = game_class
		wh_funcs = (self.game.ss.SCREEN_SIZES.prev, 
					self.game.ss.SCREEN_SIZES.next, 
					self.game.update_size)
		theme_funcs = (self.game.theme.prev_theme,
						self.game.theme.next_theme,
						self.game.update_theme)

		buttons = (("Continue", self.back),
						 (self._wh_to_str, wh_funcs),
						 (self._theme_to_str, theme_funcs),
						 ("Randomize colors", self.randomize_colors),
						 ("Main menu", self.go_main_menu),
						 ("Quit", game_class.root.quit))
						 
		norm_color = self.game.theme["menu_butts_on"]
		dis_color = self.game.theme["menu_butts_off"]
		BaseMenu.__init__(self, buttons, menu_id, norm_color, dis_color)
		
	def rotate_colors(self):
		# Change buttons color
		norm_color = self.game.theme["menu_butts_on"]
		dis_color = self.game.theme["menu_butts_off"]
		self.rotate_buttons_color(norm_color, dis_color)
		
	def check_keys(self, key):
		BaseMenu.check_keys(self, key)				
		if key == "Escape":
			self.back()
		
	def back(self):
		self.game.update_size()
		self.game.update_theme()
		self.game._stop_cont_game()
		
	def rotate_theme(self):
		self.game.theme.next_theme()
		self.game.rotate_colors()
		
	def randomize_colors(self):
		self.game.theme.randomize()
		self.game.rotate_colors()
		
	def go_main_menu(self):
		self.game.root.after_cancel(self.game.after_id)
		self.game.buffs.desactivate()
		#self.game.c.delete(ALL)
		self.game.c.destroy()
		self.game.reinit()
		
	def _wh_to_str(self):
		# Return string for rotate_size_Button
		width, height = self.game.ss.SCREEN_SIZES.get()
		return "< "+str(width)+"x"+str(height)+" >"
		
	def _theme_to_str(self):
		return "< Theme: "+self.game.theme.cur_theme+" >"
	
				
	
class OptionMenu(BaseMenu):
	def __init__(self, menu_id, game_class):
		self.game = game_class
		
		wh_funcs = (self.game.ss.SCREEN_SIZES.prev, 
					self.game.ss.SCREEN_SIZES.next, 
					self.game.update_size)
		crazy_funcs = (self.game.CRAZY.prev,
						self.game.CRAZY.next,
						self.game.update_crazy)
		theme_funcs = (self.game.theme.prev_theme,
						self.game.theme.next_theme,
						self.game.update_theme)
						
		buttons = ((self._wh_to_str, wh_funcs), 
					(self._crazy_to_str, crazy_funcs), 
					(self._theme_to_str, theme_funcs),
					("Back", self.back))
		norm_color = self.game.theme["menu_butts_on"]
		dis_color = self.game.theme["menu_butts_off"]
		BaseMenu.__init__(self, buttons, menu_id, norm_color, dis_color)
		
		
	def rotate_colors(self):
		# Change buttons color
		norm_color = self.game.theme["menu_butts_on"]
		dis_color = self.game.theme["menu_butts_off"]
		self.rotate_buttons_color(norm_color, dis_color)
		
	def check_keys(self, key):
		BaseMenu.check_keys(self, key)
				
		if key == "Escape":
			# Save state and return to menu
			self.back()
			
	def back(self):
		self.game.update_size()
		self.game.update_crazy()
		self.game.update_theme()
		self.game.show_options_menu(hide=True)
		
		
	def _wh_to_str(self):
		# Return string for rotate_size_Button
		width, height = self.game.ss.SCREEN_SIZES.get()
		return "< "+str(width)+"x"+str(height)+" >"
		
	def _crazy_to_str(self):
		return "< Mode: "+self.game.CRAZY.get()+" >"
	
	def _theme_to_str(self):
		return "< Theme: "+self.game.theme.cur_theme+" >"
