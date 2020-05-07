from random import randint

class Theme(dict):
	# TODO REWRITE IT
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
		dict.__init__(self)
		self.fixed = {}
		self.cur_theme = "Default"
		self.choose_theme()
		
	def set_canvas(self, canva):
		self.c = canva
		
	def change_theme(self, bg="green", line="white", l_pad="yellow", 
						r_pad="yellow", text="white",
						ball="white", menu_butts_on="#b9b9b9", 
						menu_butts_off="#2b2b2b"):
							
		self.update({"bg":bg, "line": line, "r_pad":r_pad, "l_pad":l_pad, 
						"text":text, "ball":ball, "menu_butts_on":menu_butts_on, 
						"menu_butts_off":menu_butts_off})
		self.set_fixed()
		
	def rotate_colors(self, elem_tag=None):
		if elem_tag:
			for elem in self.c.find_withtag(elem_tag):
				self.c.itemconfig(elem, fill=self[elem_tag])
			if elem_tag == "bg":
				self.c.config(bg=self["bg"])
		else:
			for key in self:
				for elem in self.c.find_withtag(key):
					self.c.itemconfig(elem, fill=self[key])
					
			self.c.config(bg=self["bg"])
		# NOTE: menu buttons will be configured in SMenu class
		
	def choose_theme(self):
		self.change_theme(**Theme.themes[self.cur_theme])
		
	def next_theme(self):
		next_ind = Theme.theme_names.index(self.cur_theme)+1
		next_ind %= Theme.n_themes
		self.cur_theme = Theme.theme_names[next_ind]
		self.choose_theme()
		
	def pin_color(self, elem_tag, new_color):
		if elem_tag in self.fixed:
			old_color = self.fixed[elem_tag][0]
		else:
			old_color = self[elem_tag]
		
		self.fixed[elem_tag] = [old_color, new_color]
		self[elem_tag] = new_color
		self.rotate_colors(elem_tag)
		
		
	def unpin_color(self, elem_tag):
		if elem_tag in self.fixed:
			self[elem_tag] = self.fixed[elem_tag][0]
			self.fixed.pop(elem_tag)
		self.rotate_colors(elem_tag)
			
			
	def set_fixed(self):
		for tag in self.fixed:
			self.fixed[tag][0] = self[tag]
			self[tag] = self.fixed[tag][1]
		 
		
	def randomize(self):
		# Oh, yeah, I'm good designer
		for key in self:
			if key not in self.fixed:
				self[key] = Theme._get_random_color()
			
		# Make the same color for left and right pad	
		if "l_pad" not in self.fixed:
			if "r_pad" not in self.fixed:
				self["l_pad"] = self["r_pad"]
			else:
				self["l_pad"] = self.fixed["r_pad"][0]
		elif "r_pad" not in self.fixed:
			self.fixed["l_pad"][0] = self["r_pad"]

		
	def _get_random_color():
		color = "#"
		for k in range(3):
			x = randint(0, 0xff)
			color += "{:02x}".format(x)
		return color
	
		
	
