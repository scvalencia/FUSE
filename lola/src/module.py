class Module(object):

	SECTIONS = ['MODULE', 'DESCRIPTION', 'PICTURE', 'INPUT', 'MODULES', 'CIRCUIT', 'OUTPUT']

	def __init__(self, filename):

		self.filename = filename
		self.label = ''
		self.description = ''
		self.image = ''
		self.ins = []
		self.modules = []
		self.outs = []	
		self.file_array = []	
		self.done = False

	def get_filename(self):

		return filename

	def get_label(self):

		return self.label

	def get_description(self):

		return self.description

	def get_image(self):

		return self.image

	def get_inputs(self):

		return self.ins

	def get_modules(self):

		return self.modules

	def get_outputs(self):

		return self.outs

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

	def process_file(self):

		program = {}
		
		file_object = open(self.filename, 'r')

		done = False

		self.file_array = file_object.readlines()
		self.file_array = filter(lambda x : x.strip() != '\n', self.file_array)

		file_object.close()

		size = len(self.file_array)

		i = 0
		dummy = i

		while not done:
			line = self.file_array[i].strip().split(':')
			identifier = line[0]
			if identifier in self.SECTIONS:
				program[identifier] = i
				dummy = i
			i += 1

			if i == size:
				done = True

		return program

	def set_enviroment(self):

		env = {}

		self.set_modules()

		print self.modules

	def set_modules(self):

		program = self.process_file()

		i = program['MODULES']
		i += 1
		while i != program['CIRCUIT'] - 1:
			line = self.file_array[i].strip().split(':')
			parse = line[0].split(',')

			for itm in parse:

				itm = itm.strip()
				kind = line[1].strip()
				self.modules.append((itm, kind))

			i += 1




class ModuleConnector(object):

	def __init__(self, fmodule, tmodule):

		self.fmodule = fmodule
		self.tmodule = tmodule

f = Module('src/sample.lola')
f.set_enviroment()