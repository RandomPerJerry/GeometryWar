from pygame.time import get_ticks

class Timer:
	def __init__(self, duration, func = None, repeat = False):
		"""
		Timer class for managing time based events
		
		:param int duration: The duration of the timer in milliseconds
		:param function func: The function to call when the timer is done
		:param bool repeat: Whether the timer should repeat or not
		
		:rtype: None
		"""

		# setting up the timer
		self.duration = duration
		self.func = func
		self.start_time = 0
		self.time_left = 0
		self.active = False
		self.repeat = repeat

	def activate(self):
		"""
		Activate the timer

		:rtype: None
		"""
		self.active = True
		self.start_time = get_ticks()
		self.time_left = self.duration

	def deactivate(self):
		"""
		Deactivate the timer

		:rtype: None
		"""
		self.active = False
		self.start_time = 0
		self.time_left = 0
		if self.repeat:
			self.activate()

	def update(self):
		"""
		Update the timer

		:rtype: None
		"""
		current_time = get_ticks()
		self.time_left = self.duration - (current_time - self.start_time)

		# check if the timer is done
		if self.time_left <= 0:
			if self.func and self.start_time != 0:
				self.func()
			self.deactivate()