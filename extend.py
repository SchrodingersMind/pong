from tkinter import Canvas
from enum import Enum

from pad import Pad


class PositionList(list):
    def __init__(self, base_list, cur_iter=0):
        self.extend(base_list)
        self.n = len(base_list)
        self.it = cur_iter

    def next(self, step=1):
        step %= self.n
        self.it += step
        if self.it < 0:
            self.it += self.n
        elif self.it >= self.n:
            self.it -= self.n
        return self[self.it]

    def prev(self, step=1):
        return self.next(-step)

    def get(self):
        return self[self.it]


class PlayerData():
    def __init__(self, player_id, player_class, player_string, score=0):
        self.id = player_id
        self._p_class = player_class
        self._p_str = player_string
        self.score = score

    def __eq__(self, value):
        if isinstance(value, int):
            return self.id == value
        elif isinstance(value, str):
            return self._p_str == value
        elif isinstance(value, Pad):
            return self.id == value.p_id

    def __neq__(self, value):
        if isinstance(value, (int, str, Pad)):
            return not self.__eq__(value)

    def to_str(self):
        return self._p_str

    def get(self):
        return self.id

    def get_pad(self):
        return self._p_class

    def copy(self):
        return PlayerData(self.id, self._p_class, self._p_str)


class Player(PlayerData):
    LEFT = 0
    RIGHT = 1

    def __init__(self, pad_left, pad_right):

        PlayerData.__init__(self, Player.LEFT, pad_left, "left")
        self.l_player = self.copy()

        self.r_player = PlayerData(Player.RIGHT, pad_right, "right")
        self.other = self.r_player

    def switch(self):
        if self.id == Player.LEFT:
            self._reinit(self.r_player)
            self.other = self.l_player
        else:
            self._reinit(self.l_player)
            self.other = self.r_player

    def _reinit(self, player):
        self.id = player.id
        self._p_class = player._p_class
        self._p_str = player._p_str


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
        return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    def scale_center(self, item_id, xscale, yscale=None):
        """ Scale object, don't changing it's center """
        if not yscale:
            yscale = xscale
        old_x = self.get_x_center(item_id)
        old_y = self.get_y_center(item_id)
        self.scale(item_id, 0, 0, xscale, yscale)
        new_x = self.get_x_center(item_id)
        new_y = self.get_y_center(item_id)
        dx, dy = old_x - new_x, old_y - new_y
        self.move(item_id, dx, dy)

    def ball_coords(self, item_id, x, y, r=None):
        """ Set ball center at (x,y) and radius to r """
        if not r:
            # Move ball without changing radius
            cur_x = self.get_x_center(item_id)
            cur_y = self.get_y_center(item_id)
            self.move(item_id, x - cur_x, y - cur_y)
        else:
            self.coords(item_id, x - r, y - r, x + r, y + r)

    def check_collision(self, id1, id2, balls=True):
        """ id1,2 - items id
			balls - if True, do check by centers and 
						compare it with radius(height/2)
					otherwise, compare like squares
		"""
        if balls:
            # print(self.bbox(id2), self.bbox(id1))
            dist = (self.get_height(id1) + self.get_height(id2)) / 2
            dy = self.get_y_center(id1) - self.get_y_center(id2)
            dx = self.get_x_center(id1) - self.get_x_center(id2)
            return dist ** 2 > dy ** 2 + dx ** 2
        else:
            elems = self.find_overlapping(*self.bbox(id1))
            return id2 in elems
