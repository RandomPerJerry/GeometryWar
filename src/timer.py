from pygame.time import get_ticks

class Timer:
	def __init__(self, duration, func = None, repeat = False):
		self.duration = duration
		self.func = func
		self.start_time = 0
		self.time_left = 0
		self.active = False
		self.repeat = repeat

	def activate(self):
		self.active = True
		self.start_time = get_ticks()
		self.time_left = self.duration

	def deactivate(self):
		self.active = False
		self.start_time = 0
		self.time_left = 0
		if self.repeat:
			self.activate()

	def update(self):
		current_time = get_ticks()
		self.time_left = self.duration - (current_time - self.start_time)
		if self.time_left <= 0:
			if self.func and self.start_time != 0:
				self.func()
			self.deactivate()