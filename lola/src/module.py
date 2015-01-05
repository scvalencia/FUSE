import os
import sys
import logicgate

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
		self.output = None
		self.arity = (len(self.ins), len(self.outs))

		self.check_file()

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

	def check_file(self):

		ins = []
		outs = []
		used_names = []

		if not os.path.isfile(self.filename):
			print 'MODULE: ' + self.filename
			print 'File does not exists'
			sys.exit()

		if len(self.filename) < 5 or self.filename[-5:].upper() != '.LOLA':
			print 'MODULE: ' + self.filename
			print 'File is not a lola file'
			sys.exit()

		program = self.process_file()

		file_object = open(self.filename, 'r')
		program = self.process_file()

		p1 = 'MODULE' in program
		p2 = 'INPUT' in program
		p3 = 'MODULES' in program
		p4 = 'CIRCUIT' in program
		p5 = 'OUTPUT' in program

		if p1 and p2 and p3 and p4 and p5:

			for itm in self.SECTIONS:

				if itm in program:

					if itm == 'MODULE':
						stop_flag = 'DESCRIPTION' if 'DESCRIPTION' in program else ('PICTURE' if 'PICTURE' in program else 'INPUT')
						i = program[itm] + 1
						while i != program[stop_flag] - 1:
							line = self.file_array[i].strip()
							if line != self.filename[:-5].upper():
								print 'MODULE: ' + self.filename
								print 'Module should be named as file (W/O .lola)'
								sys.exit()
							i += 1

					if itm == 'PICTURE':
						i = program[itm] + 1
						while i != program['INPUT'] - 1:
							image_file = self.file_array[i].strip()

							if not os.path.isfile(image_file):
								print 'MODULE: ' + self.filename
								print 'Picture file does not exists'
								sys.exit()

							self.image = image_file

							i += 1

					if itm == 'INPUT':
						lst = []
						i = program[itm] + 1
						while i != program['MODULES'] - 1:
							line = self.file_array[i].strip()
							lst += map(lambda x : x .strip(), line.split(','))

							i += 1

						for (i, itm1) in enumerate(lst):
							for(j, itm2) in enumerate(lst):
								if i != j and itm1 == itm2:
									print 'MODULE: ' + self.filename
									print 'Repeated input declaration: ' + itm1
									sys.exit()

						ins = lst

					if itm == 'MODULES':

						unary_gates = ['NOT']
						binary_gates = ['XOR', 'XNOR']
						variable_gates = ['AND', 'OR', 'NAND', 'NOR']
						lola_files = filter(lambda x : 'lola' in x.lower(), os.listdir(os.getcwd()))
						lola_files = [_[:-5].upper() for _ in lola_files]
						recognized_modules = unary_gates + binary_gates + variable_gates + lola_files

						i = program[itm] + 1
						while i != program['CIRCUIT'] - 1:
							line = self.file_array[i].strip().split(':')
							parse = line[0].split(',')

							for itm in parse:

								itm = itm.strip()
								kind = line[1].strip()

								if kind[0].isdigit():
									if kind[1:] not in variable_gates:
										print 'MODULE: ' + self.filename
										print 'Not a valid variable input gate: ' + kind
										sys.exit()

								else:
									if kind not in recognized_modules:										
										print 'MODULE: ' + self.filename
										print 'Unrecognized module: ' + kind
										sys.exit()

								if itm in used_names:
									print 'MODULE: ' + self.filename
									print 'Module already declared: ' + itm
									sys.exit()



								used_names.append(itm)

							i += 1

					if itm == 'CIRCUIT':
						i = program[itm] + 1
						while i != program['OUTPUT'] - 1:
							line = self.file_array[i].strip()
							command = line.split()

							if len(command) != 3:

								print 'MODULE: ' + self.filename
								print 'Unrecognized command: ' + line
								sys.exit()

							if command[0] not in ['SET', 'CON']:

								print 'MODULE: ' + self.filename
								print 'Unrecognized command: ' + line
								sys.exit()

							if command[0] == 'SET':
								if command[1] not in ins:

									print 'MODULE: ' + self.filename
									print 'Not declared input: ' + command[1]
									sys.exit()

								if command[-1] not in used_names:

									print 'MODULE: ' + self.filename
									print 'Not declared module: ' + command[-1]
									sys.exit()

							elif command[0] == 'CON':

								if command[1] not in used_names:

									print 'MODULE: ' + self.filename
									print 'Not declared module: ' + command[1]
									sys.exit()

								if command[-1] not in used_names:

									print 'MODULE: ' + self.filename
									print 'Not declared module: ' + command[-1]
									sys.exit()

							i += 1

					if itm == 'OUTPUT':
						i = program[itm] + 1
						while i != len(self.file_array):
							line = self.file_array[i].strip()
							parse = line.split()

							for itm in parse:
								if itm not in used_names:
									print 'MODULE: ' + self.filename
									print 'Not declared module: ' + itm
									sys.exit()

							outs.append(itm)
							i += 1

		else:
			print ('Missed section, ' 
				'mandatory sections are: '
				'module, input, modules, circuit, output'
				'in that order')
			sys.exit()

		self.load_data(ins, outs)

	def load_data(self, ins, outs):

		program = self.process_file()

		self.ins = ins
		self.outs = outs

		if 'DESCRIPTION' in program:

			i = program['DESCRIPTION'] + 1
			next_flag = 'PICTURE' if 'PICTURE' in program else 'INPUT'

			while i != program[next_flag] - 1:
				line = self.file_array[i]
				self.description += line
				i += 1

		self.label = self.filename[:-5].upper()
		self.arity = (len(self.ins), len(self.outs))
		

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

	def set_enviroment(self):

		env = {}

		self.set_modules()

		for item in self.modules:

			name, kind = item[0], item[1]

			if name not in env:
				if kind == 'AND':
					env[name] = logicgate.AndGate()
				elif kind == 'OR':
					env[name] = logicgate.OrGate()
				elif kind == 'NAND':
					env[name] = logicgate.NandGate()
				elif kind == 'NOR':
					env[name] = logicgate.NorGate()
				elif kind == 'XOR':
					env[name] = logicgate.XorGate()
				elif kind == 'XNOR':
					env[name] = logicgate.XnorGate()
				elif kind == 'NOT':
					env[name] = logicgate.NotGate()

				if kind[0].isdigit():
					number = int(kind[0])
					gate = kind[1:]
					if gate == 'AND':
						env[name] = logicgate.NAndGate(number)
					elif gate == 'OR':
						env[name] = logicgate.NOrGate(number)
					elif gate == 'NAND':
						env[name] = logicgate.NNandGate(number)
					elif gate == 'NOR':
						env[gate] = logicgate.NNorGate(number)

			else:
				print 'WARNING: Repeated gate definition: ' + name

		return env

	def perform_logic(self):

		enviroment = self.set_enviroment()



class ModuleConnector(object):

	def __init__(self, fmodule, tmodule):

		self.fmodule = fmodule
		self.tmodule = tmodule

f = Module(sys.argv[1])