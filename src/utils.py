
__all__ = ["double_exponential_decay", "exponential_decay", "heaviside_step"] 
import numbers 
import math 


def heaviside_step(x): 
	r""" 
	The Heaviside step function. 

	Parameters 
	----------
	x : float 
		Some real number. 

	Returns 
	-------
	y : float 
		1 if x >= 0, 0 otherwise. 
	""" 
	return int(x >= 0) 


class exponential_decay: 

	r""" 
	A simple exponential decay function. 

	Parameters 
	----------
	normalization : real number [default : 1] 
		The attribute ``normalization``. See below. 
	timescale : real number [default : 1] 
		The attribute ``timescale``. See below. 

	Attributes 
	----------
	normalization : real number [default : 1] 
		The value of the exponential at time = 0, in the same units that the 
		y-axis is interpreted as having. 
	timescale : real number [default : 1] 
		The e-folding timescale (positive for exponential decay, negative for 
		exponential growth), in the same units as the times this object will 
		be called with. 

	Calling 
	-------
	Call this object as you would any other function of time. 

		Parameters: 

			- time : real number 
				The timestamp in the same units as the attribute ``timescale``. 

		Returns: 

			- f : real number 
				The value of the exponential function :math:`f(x)`, defined 
				according to :math:`f(x) = Ae^{-t / \tau}`, where :math:`A` is 
				the attribute ``normalization``, and :math:`\tau` is the 
				attribute ``timescale``. 
	""" 

	def __init__(self, normalization = 1, timescale = 1): 
		self.normalization = 1 
		self.timescale = 1 

	def __call__(self, time): 
		return self.normalization * math.exp(-time / self.timescale) 

	@property 
	def normalization(self): 
		r""" 
		Type : float 

		Default : 1 

		The value of the exponential at time = 0, in arbitrary units. 
		""" 
		return self._normalization 

	@normalization.setter 
	def normalization(self, value): 
		if isinstance(value, numbers.Number): 
			self._normalization = float(value) 
		else: 
			raise TypeError("""Attribute 'normalization' must be a numerical \
value. Got: %s""" % (type(value))) 

	@property 
	def timescale(self): 
		r""" 
		Type : float 

		Default : 1 

		The e-folding timescale. Positive values denote exponential decay; 
		negative values denote exponential growth. 
		""" 
		return self._timescale 

	@timescale.setter 
	def timescale(self, value): 
		if isinstance(value, numbers.Number): 
			self._timescale = float(value) 
		else: 
			raise TypeError("""Attribute 'timescale' must be a numerical \
value. Got: %s""" % (type(value))) 


class double_exponential_decay: 

	r""" 
	A double exponential decay function. 

	Parameters 
	----------
	onset : real number [default : 0] 
		The attribute ``onset``. See below. 

	Attributes 
	----------
	first : ``exponential_decay`` 
		The first of the two exponential decay episodes 
	second : ``exponential_decay`` 
		The second of the two exponential decay episodes 
	onset : real number [default : 0] 
		The time of the onset of the second exponential decay, in arbitrary 
		units. 

	Calling 
	-------
	Call this object as you would any other function of time. 

		Parameters: 

			- time : real number 
				Time in the same units as the attribute ``onset`` and the 
				timescales associated with the attributes ``first`` and 
				``second``. 

		Returns: 

			- y : real number 
				The value of the double exponential defined via 
				:math:`f(t) + H(t - t_o)g(t - t_o)`, where :math:`f` and 
				:math:`g` are the attributes ``first`` and ``second``, 
				respectively, :math:`t_o` is the attribute ``onset``, and 
				:math:`H` is the Heaviside step function. 

	Notes 
	-----
	This object makes use of composition to store the two individual 
	exponential decays. 
	""" 

	def __init__(self, onset = 0): 
		self.first = exponential_decay() 
		self.second = exponential_decay() 
		self.onset = onset 

	def __call__(self, time): 
		return (self.first.__call__(time) + heaviside_step(time - self.onset) * 
			self.second.__call__(time - self.onset)) 

	@property 
	def first(self): 
		r""" 
		Type : ``exponential_decay`` 

		The first of the two exponential decay functions. 
		""" 
		return self._first 

	@first.setter 
	def first(self, value): 
		if isinstance(value, exponential_decay): 
			self._first = value 
		else: 
			raise TypeError("""Attribute 'first' must be of type \
'exponential_decay'. Got: %s""" % (type(value))) 

	@property 
	def second(self): 
		r""" 
		Type : ``exponential_decay`` 

		The second of the two exponential decay functions, which will be 
		forced to a value of zero before the time denoted by the attribute 
		``onset``. 
		""" 
		return self._second 

	@second.setter 
	def second(self, value): 
		if isinstance(value, exponential_decay): 
			self._second = value 
		else: 
			raise TypeError("""Attribute 'second' must be of type \
'exponential_decay'. Got: %s""" % (type(value))) 

	@property 
	def onset(self): 
		r""" 
		Type : float 

		Default : 0 

		The time of onset of the second exponential decay, in the same units 
		as the time coordinate that this object will be called with. 
		""" 
		return self._onset 

	@onset.setter 
	def onset(self, value): 
		if isinstance(value, numbers.Number): 
			self._onset = float(value) 
		else: 
			raise TypeError("""Attribute 'onset' must be a numerical \
value. Got: %s""" % (type(value))) 

