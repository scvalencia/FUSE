import sys
import tabulate
from LogicGate import *

SECTIONS = ['PROGRAM', 'INPUT', 'GATES', 'CIRCUIT', 'OUTPUT']
program = {}
values = {}
file_array = []

def process_file(filename):

	file_object = open(filename, 'r')

	global file_array

	done = False

	file_array = file_object.readlines()
	file_array = filter(lambda x : x != '\n', file_array)
	file_object.close()

	size = len(file_array)

	i = 0
	dummy = i
	while not done:
		line = file_array[i].strip().split(':')
		if line[0] in SECTIONS:
			program[line[0]] = i
			dummy = i
		i += 1

		if i == size:
			done = True

def set_inputs():

	inputs = []

	i = program['INPUT']
	i += 1
	while i != program['GATES']:
		line = file_array[i].strip().split(',')
		for itm in line:
			itm = itm.strip()
			inputs.append(itm)

		i += 1

	return inputs

def set_gates():

	gates = []

	i = program['GATES']
	i += 1
	while i != program['CIRCUIT']:
		line = file_array[i].strip().split(':')
		parse = line[0].split(',')
		for itm in parse:
			itm = itm.strip()
			kind = line[1]
			gates.append((itm, kind))

		i += 1

	return gates

def set_outputs():

	outputs = []
	size = len(file_array)

	i = program['OUTPUT']
	i += 1
	while i != size:
		line = file_array[i].strip().split(',')
		for itm in line:
			itm = itm.strip()
			outputs.append(itm)
			
		i += 1

	return outputs

def set_env():
	env = {}

	gates = set_gates()

	for gate in gates:
		name, kind = gate[0], gate[1].strip()

		if name not in env:
			if kind == 'AND':
				env[name] = AndGate()
			elif kind == 'OR':
				env[name] = OrGate()
			elif kind == 'NAND':
				env[name] = NandGate()
			elif kind == 'NOR':
				env[name] = NorGate()
			elif kind == 'XOR':
				env[name] = XorGate()
			elif kind == 'XNOR':
				env[name] = XnorGate()			
			elif kind == 'NOT':
				env[name] = NotGate()
		else:
			print 'Repeated gate definition: ' + name

	return env

def get_binary_string(number, length):

	representation = "{0:b}".format(number)
	new_len = length - len(representation)
	return ("0" * new_len) + representation

def get_max_number(items):
	i = 0
	ans = 0
	while i < items:
		ans += 2 ** i
		i += 1
	return ans

def simulate(env):

	inputs = set_inputs()
	outputs = set_outputs()

	header = inputs + outputs
	table = []

	bits = get_max_number(len(inputs))
	length = len("{0:b}".format(bits))

	for itm in inputs:
		values[itm] = 0

	i = program['CIRCUIT']
	i += 1
	while i != program['OUTPUT']:

		line = file_array[i].strip().split()

		if line[0] == 'SET':
			signal = line[1]
			gate = line[2]

			if signal not in inputs:
				print 'Signal not in enviroment: ' + signal
				sys.exit()

			if gate not in env:
				print 'Gate not in enviroment: ' + gate
				sys.exit()

		elif line[0] == 'CON':
			fgate = line[1]
			tgate = line[2]

			if fgate not in env:
				print 'Gate not in enviroment: ' + fgate
				sys.exit()

			if tgate not in env:
				print 'Gate not in enviroment: ' + fgate
				sys.exit()

		else:
			print 'Unrecognized instruction for simulation: ' + line[0]	
			sys.exit()
		i += 1

	i = 0
	while i <= bits:
		itm = []
		

		rep = get_binary_string(i, length)
		set_values(rep)


		for r in rep:
			itm.append(r)

		j = program['CIRCUIT'] + 1

		while j != program['OUTPUT']:

			flag = True
			line = file_array[j].strip().split()
			
			if line[0] == 'SET':
				signal = line[1]
				gate = line[2]

				env[gate].set_pin(values[signal])


			elif line[0] == 'CON':
				fgate = line[1]
				tgate = line[2]

				Connector(env[fgate], env[tgate])

			for _ in outputs:
				if not env[_].is_complete():
					flag = False

			if flag:
				for o in outputs:
					env[o].perform_logic()
					itm.append(env[o].output)				

			j += 1
		
		for gate in env:
			env[gate].clean()

		table.append(itm)		
		i += 1

	print tabulate.tabulate(table, header, tablefmt="grid")


def set_values(vals):
	inputs = set_inputs()

	i = 0
	for itm in inputs:
		values[itm] = int(vals[i])
		i += 1

def main():

	global file_array

	process_file('FullAdder.lola')
	file_array = filter(lambda x : x != '\n', file_array)
	enviroment = set_env()
	simulate(enviroment)

if __name__ == '__main__':
	main()