from random import randint

class Theme:
	
	# This vars currently unused
	tags = ("lines", "l_pad", "r_pad", "ball")
	elems = tags + ("menu_butts_on", "menu_butts_off", "bg")
	themes = (("white", "yellow", "yellow", "white", "#b9b9b9", "#2b2b2b", "green"),
			  ("white", "white", "white", "red", "white", "#2b2b2b", "black"))
	
	
	def __init__(self):
		self.change_theme()
		self.fixed = []
	
	def change_theme(self, bg="green", lines="white", l_pad="yellow", 
						r_pad="yellow", text="white",
						ball="white", menu_butts_on="#b9b9b9", 
						menu_butts_off="#2b2b2b", canva=None):
		self.bg = bg
		self.lines = lines
		self.l_pad = l_pad
		self.r_pad = r_pad
		self.text = text
		self.ball = ball
		self.menu_butts_on = menu_butts_on
		self.menu_butts_off = menu_butts_off
		
		self.full_theme = {"bg":bg, "lines": lines, "r_pad":r_pad, "l_pad":l_pad, 
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
		
	def randomize(self, canva=None):
		# Oh, yeah, I'm good designer
		for key in self.full_theme:
			self.full_theme[key] = Theme._get_random_color()
			
		self.full_theme["l_pad"] = self.full_theme["r_pad"]
			
		self.change_theme(**self.full_theme, canva=canva)
		
		if canva:
			self.rotate_colors(canva)
		
	def _get_random_color():
		color = "#"
		for k in range(3):
			x = randint(0, 0xff)
			color += "{:02x}".format(x)
		return color
	
		
	
