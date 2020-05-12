from extend import PositionList

class Size:
	def __init__(self):
		self.WIDTH = 900
		self.HEIGHT = 400
		
		# WIDTH/HEIGHT must be primay the same (because ball must be circle)
		self.SCREEN_SIZES = PositionList([(800, 350), (self.WIDTH, self.HEIGHT), (1000, 450), (1200, 540)], 1)
		
		self.PAD_W = 10
		self.PAD_H = 100
		self.PAD_SPEED = 24
	
		self.BALL_RADIUS = 30
		# Ball speed will increase after touching with paddle
		self.BALL_SPEED_UP = 1.06
		
		self.BALL_MAX_SPEED = 60
		self.INITIAL_SPEED = 30
		self.BALL_X_SPEED = self.BALL_Y_SPEED = self.INITIAL_SPEED
		
		self.RIGHT_TAB = self.WIDTH-self.PAD_W
		
	def scale(self, xscale, yscale):
		
		self.WIDTH *= xscale
		self.HEIGHT *= yscale
		
		self.PAD_W *= xscale
		self.PAD_H *= yscale

		self.PAD_SPEED *= yscale
	
	
		self.BALL_MAX_SPEED *=  (xscale+yscale)/2
		self.BALL_RADIUS *= (xscale+yscale)/2
		
		self.INITIAL_SPEED *= (xscale+yscale)/2
		self.BALL_X_SPEED *= xscale
		self.BALL_Y_SPEED *= yscale
		
		self.RIGHT_TAB *= xscale


