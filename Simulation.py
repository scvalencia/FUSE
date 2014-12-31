from LogicGate import *

def basic_circuit1(a, b, c):

	g1 = AndGate()
	g2 = OrGate()
	g3 = NotGate()

	g1.set_pin(a)
	g1.set_pin(b)
	g2.set_pin(c)

	Connector(g1, g2)
	Connector(g2, g3)

	g3.perform_logic()
	return g3.output

def basic_circuit2(a, b, c, d):

	g1 = NotGate()
	g2 = NotGate()
	g3 = OrGate()
	g4 = AndGate()
	g5 = AndGate()

	g1.set_pin(a)
	g2.set_pin(b)
	g3.set_pin(c)
	g3.set_pin(d)

	Connector(g2, g4)
	Connector(g3, g4)
	Connector(g1, g5)
	Connector(g4, g5)

	g5.perform_logic()
	return g5.output

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

def simulation1():
	import tabulate

	headers = ['A', 'B', 'C', 'OUT']
	table = []

	bits = get_max_number(len(headers) - 1)
	length = len("{0:b}".format(bits))

	i = 0
	while i <= bits:
		rep = get_binary_string(i, length)
		a, b, c = int(rep[0]), int(rep[1]), int(rep[2])
		out = basic_circuit1(a, b, c)
		item = [a, b, c, out]
		table.append(item)
		i += 1

	output_filename = 'out.txt'
	file_object = open(output_filename, 'w')

	print tabulate.tabulate(table, headers, tablefmt="grid")
	file_object.write(tabulate.tabulate(table, headers, tablefmt="grid"))


def simulation2():
	import tabulate

	headers = ['A', 'B', 'C', 'D', 'OUT']
	table = []

	bits = get_max_number(len(headers) - 1)
	length = len("{0:b}".format(bits))

	i = 0
	while i <= bits:
		rep = get_binary_string(i, length)
		a, b, c, d = int(rep[0]), int(rep[1]), int(rep[2]), int(rep[3])
		out = basic_circuit2(a, b, c, d)
		item = [a, b, c, d, out]
		table.append(item)
		i += 1

	output_filename = 'out.txt'
	file_object = open(output_filename, 'w')

	print tabulate.tabulate(table, headers, tablefmt="grid")
	file_object.write(tabulate.tabulate(table, headers, tablefmt="grid"))

simulation1()