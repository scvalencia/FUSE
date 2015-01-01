class module(object):

	def __init__(self, filename):

		self.label = ''
		self.ins = []
		self.outs = []
		self.modules = []
		self.filename = filename
		self.image = ''
		self.done = False

	def get_label(self):

		return self.label

	def get_inputs(self):

		return self.ins

	def get_outputs(self):

		return self.outs

	def get_filename(self):

		return filename

	def set_input(self, value):

		if value not in [0, 1]:
			raise ValueError("Pin value must be 0, or 1")

		else:
			self.ins.append(value)

	def length_input(self):

		return len(self.ins)

	def length_output(self):

		return len(self.outs)

	def clean(self):

		self.ins = []

	def process_file():
		pass

class ModuleConnector(object):

	def __init__(self, fmodule, tmodule):

		self.fmodule = fmodule
		self.tmodule = tmodule