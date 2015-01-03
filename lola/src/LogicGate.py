import datetime

class LogicGate(object):

	def __init__(self, name):

		self.label = name
		self.image = ''
		self.output = None

	def get_label(self):

		return self.label

	def get_output(self):

		self.output = self.perform_logic()
		return self.output

class BinaryGate(LogicGate):

	def __init__(self, name):

		LogicGate.__init__(self, name)

		self.pin1 = None
		self.pin2 = None

	def set_pin1(self, value):

		if value not in [0, 1]:
			raise ValueError("Pin value must be 0, or 1")

		else:
			self.pin1 = value

	def get_pin1(self):

		return self.pin1

	def set_pin2(self, value):

		if value not in [0, 1]:
			raise ValueError("Pin value must be 0, or 1")

		else:
			self.pin2 = value

	def get_pin2(self):

		return self.pin2

	def set_pin(self, value):

		if value not in [0, 1]:
			raise ValueError("Pin value must be 0, or 1")

		else:
			if self.pin1 == None:
				self.set_pin1(value)

			else:
				if self.pin2 == None:
					self.set_pin2(value)
				else:
					raise RuntimeError("No empty pins in the gate " + self.label)

	def is_complete(self):
		
		return self.pin1 != None and self.pin2 != None

	def clean(self):
		self.pin1 = None
		self.pin2 = None

	def __str__(self):
		ans = ''
		ans += '(' + str(self.pin1) + ', ' + str(self.pin2) + ')'
		return ans

class UnaryGate(LogicGate):

	def __init__(self, name):

		LogicGate.__init__(self, name)

		self.pin = None

	def set_pin(self, value):

		if value not in [0, 1]:
			raise ValueError("Pin value must be 0, or 1")

		else:
			if self.pin == None:
				self.pin = value
			else:
				raise RuntimeError("No empty pins in the gate " + self.label)

	def get_pin(self):

		return self.pin

	def is_complete(self):

		return self.pin != None

	def clean(self):
		self.pin = None

	def __str__(self):
		return '(' + str(self.pin) + ')'

class NAryGate(LogicGate):

	def __init__(self, n, name):

		LogicGate.__init__(self, name)

		self.size = n
		self.used_index = 0
		self.inputs = [None for _ in range(self.size)]

	def set_pin(self, value):

		self.set_pin_at(self.used_index, value)
		self.used_index += 1

	def set_pin_at(self, index, value):

		if index in range(0, self.size):
			if self.inputs[index] == None:

				if value not in [0, 1]:
					raise ValueError("Pin value must be 0, or 1")

				else:
					self.inputs[index] = value

			else:
				raise Exception("Index used")

		else:
			raise IndexError("Index out of range")

	def is_complete(self):

		ans = True

		for itm in self.inputs:
			if itm == None:
				ans = False
				break

		return ans

	def clean(self):

		self.used_index = 0
		self.inputs = [None for _ in range(self.size)] 

	def __str__(self):

		body = ', '.join(map(str, self.inputs))
		ans = '(' + body + ')'
		return ans

class Connector(object):

	def __init__(self, fgate, tgate):

		self.fromgate = fgate
		self.togate = tgate

		self.fromgate.perform_logic()

		out = self.fromgate.output

		tgate.set_pin(out)

class AndGate(BinaryGate):

	def __init__(self, name = "AND" + str(datetime.datetime.now())):

		BinaryGate.__init__(self, name)

	def perform_logic(self):

		if self.pin1 == self.pin2 == 1:
			self.output = 1

		else: 
			self.output = 0

class OrGate(BinaryGate):

	def __init__(self, name = "OR" + str(datetime.datetime.now())):

		BinaryGate.__init__(self, name)

	def perform_logic(self):

		if self.pin1 == 1 or self.pin2 == 1:
			self.output = 1

		else: 
			self.output = 0

class NandGate(BinaryGate):

	def __init__(self, name = "NAND" + str(datetime.datetime.now())):

		BinaryGate.__init__(self, name)

	def perform_logic(self):

		if self.pin1 == 1 and self.pin2 == 1:
			self.output = 0

		else: 
			self.output = 1

class NorGate(BinaryGate):

	def __init__(self, name = "NOR" + str(datetime.datetime.now())):

		BinaryGate.__init__(self, name)

	def perform_logic(self):

		if self.pin1 == 0 and self.pin2 == 0:
			self.output = 1

		else: 
			self.output = 0

class XorGate(BinaryGate):

	def __init__(self, name = "XOR" + str(datetime.datetime.now())):

		BinaryGate.__init__(self, name)

	def perform_logic(self):

		if self.pin1 == self.pin2:
			self.output = 0

		else: 
			self.output = 1

class XnorGate(BinaryGate):

	def __init__(self, name = "XNOR" + str(datetime.datetime.now())):

		BinaryGate.__init__(self, name)

	def perform_logic(self):

		if self.pin1 == self.pin2:
			self.output = 1

		else: 
			self.output = 0

class NotGate(UnaryGate):

	def __init__(self, name = "NOT" + str(datetime.datetime.now())):

		UnaryGate.__init__(self, name)

	def perform_logic(self):

		if self.pin == 1:
			self.output = 0

		else:
			self.output = 1

class NAndGate(NAryGate):
	
	def __init__(self, n, name = "N_AND" + str(datetime.datetime.now())):

		NAryGate.__init__(self, n, name)

	def perform_logic(self):

		ans = 1

		for itm in self.inputs:

			new_object = AndGate()
			new_object.set_pin(itm)
			new_object.set_pin(ans)

			new_object.perform_logic()

			ans = new_object.output

		self.output = ans

class NOrGate(NAryGate):
	
	def __init__(self, n, name = "N_OR" + str(datetime.datetime.now())):

		NAryGate.__init__(self, n, name)

	def perform_logic(self):

		ans = 0

		for itm in self.inputs:

			new_object = OrGate()
			new_object.set_pin(itm)
			new_object.set_pin(ans)

			new_object.perform_logic()

			ans = new_object.output

		self.output = ans

class NNandGate(NAryGate):
	
	def __init__(self, n, name = "N_NAND" + str(datetime.datetime.now())):

		NAryGate.__init__(self, n, name)

	def perform_logic(self):

		ans = 1

		for itm in self.inputs:

			new_object = AndGate()
			new_object.set_pin(itm)
			new_object.set_pin(ans)

			new_object.perform_logic()

			ans = new_object.output

		self.output = 0 if ans == 1 else 1

class NNorGate(NAryGate):
	
	def __init__(self, n, name = "N_NAND" + str(datetime.datetime.now())):

		NAryGate.__init__(self, n, name)

	def perform_logic(self):

		ans = 0

		for itm in self.inputs:

			new_object = OrGate()
			new_object.set_pin(itm)
			new_object.set_pin(ans)

			new_object.perform_logic()

			ans = new_object.output

		self.output = 0 if ans == 1 else 1