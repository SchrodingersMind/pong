from random import randint

class Theme:
	
	# This vars currently unused
	tags = ("line", "l_pad", "r_pad", "ball")
	elems = tags + ("menu_butts_on", "menu_butts_off", "bg")
	
	# Yeah, I'm the best designer ever 
	# ...
	# (silent crying)
	themes = {"Default":{"bg": "black", "line": "white", "l_pad": "#30E3D2", "r_pad": "#30E3D2", 
							"text": "#30E3D2", "ball": "#FB43E7", "menu_butts_on": "#b9b9b9", 
							"menu_butts_off": "#2b2b2b"},
			  "Classic":{"bg": "black", "line": "black", "l_pad": "white", "r_pad": "white", 
							"text": "#5353C3", "ball": "#5353C3", "menu_butts_on": "#414132", 
							"menu_butts_off": "#1C1B1A"},
			  "Light":{"bg": "white", "line": "#F3CB27", "l_pad": "#58C8B2", "r_pad": "#58C8B2", 
							"text": "#5C821A", "ball": "#73D216", "menu_butts_on": "#fac364", 
							"menu_butts_off": "#C17D11"},
			  "Pingpong":{"bg": "green", "line": "white", "l_pad": "yellow", "r_pad": "yellow", 
							"text": "white", "ball": "white", "menu_butts_on": "#b9b9b9", 
							"menu_butts_off": "#2b2b2b"},
			  "Sea":{"bg": "#021e50", "line": "#030050", "r_pad": "#ebed13", "l_pad": "#ebed13", 
							"text": "#fc7eaf", "ball": "#a3c2d8", "menu_butts_on": "#0CA314", 
							"menu_butts_off": "#06500A"},
			  "Casual":{"bg": "#0759f8", "line": "#492f08", "r_pad": "#4DCC12", "l_pad": "#4DCC12", 
			  				"text": "#40e9de", "ball": "#ec2f61", "menu_butts_on": "#392AFF", 
			  				"menu_butts_off": "#271daf"}}
			  				
	theme_names = list(themes.keys())
	n_themes = len(theme_names)
			  
	
	
	def __init__(self):
		self.cur_theme = "Default"
		self.choose_theme()
		self.fixed = []
	
	def change_theme(self, bg="green", line="white", l_pad="yellow", 
						r_pad="yellow", text="white",
						ball="white", menu_butts_on="#b9b9b9", 
						menu_butts_off="#2b2b2b", canva=None):
		self.bg = bg
		self.line = line
		self.l_pad = l_pad
		self.r_pad = r_pad
		self.text = text
		self.ball = ball
		self.menu_butts_on = menu_butts_on
		self.menu_butts_off = menu_butts_off
		
		self.full_theme = {"bg":bg, "line": line, "r_pad":r_pad, "l_pad":l_pad, 
							"text":text, "ball":ball, "menu_butts_on":menu_butts_on, 
							"menu_butts_off":menu_butts_off}
							
		if canva:
			self.rotate_colors(canva)
		
	def rotate_colors(self, canva):
		
		for key in self.full_theme:
			for elem in canva.find_withtag(key):
				canva.itemconfig(elem, fill=self.full_theme[key])
				
		canva.config(bg=self.bg)
		# NOTE: menu buttons will be configured in SMenu class
		
	def choose_theme(self):
		self.change_theme(**Theme.themes[self.cur_theme])
		
	def next_theme(self):
		next_ind = Theme.theme_names.index(self.cur_theme)+1
		next_ind %= Theme.n_themes
		self.cur_theme = Theme.theme_names[next_ind]
		self.choose_theme()
		 
		
	def randomize(self, canva=None):
		# Oh, yeah, I"m good designer
		for key in self.full_theme:
			if key not in self.fixed:
				self.full_theme[key] = Theme._get_random_color()
			
		self.full_theme["l_pad"] = self.full_theme["r_pad"]
			
		self.change_theme(**self.full_theme, canva=canva)

		
	def _get_random_color():
		color = "#"
		for k in range(3):
			x = randint(0, 0xff)
			color += "{:02x}".format(x)
		return color
	
		
	
