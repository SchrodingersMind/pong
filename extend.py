
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

