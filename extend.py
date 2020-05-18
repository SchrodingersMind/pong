from tkinter import Canvas

class PositionList(list):
	def __init__(self, base_list, cur_iter=0):
		self.extend(base_list)
		self.n = len(base_list)
		self.it = cur_iter
		
	def next(self, step=1):
		self.it += step
		# Don't work if step > 2*n
		if self.it < 0:
			self.it += self.n
		elif self.it >= self.n:
			self.it -= self.n 
		return self[self.it]
	
	def prev(self, step=1):
		return self.next(-step)
		
	def get(self):
		return self[self.it]


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
			
	def create_ball(self, x, y, r, **kwargs):
		""" Create ball item on canvas (using create_oval method) 
			So additional options could be retrieved from it documentation
		"""
		return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
			
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

