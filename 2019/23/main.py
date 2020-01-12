from functools import reduce

class intcode:
	def __init__(self, memory):
		self.relative_base = 0
		self.pointer = 0
		self.memory = memory
		self.input = []

	def code(self):
		return self.read(self.pointer) % 100

	def params(self, n):
		mode_int = int(self.read(self.pointer) / 100)
		params = []
		for i in range(n):
			mode = mode_int % 10
			mode_int = int(mode_int / 10)
			param = self.pointer+1+i
			if mode == 0:
				param = self.read(self.pointer+1+i)
			elif mode == 2:
				param = self.read(self.pointer+1+i) + self.relative_base
			params.append(param)
		# print(self.code())
		# print(params)
		# print(self.read(self.pointer:self.pointer+n+1])
		return params

	def read(self, address):
		if address < 0:
			raise ValueError
		while address >= len(self.memory):
			self.memory.append(0)
		return self.memory[address]

	def write(self, address, value):
		if address < 0:
			raise ValueError
		while address >= len(self.memory):
			self.memory.append(0)
		self.memory[address] = value

	def run(self, x):
		if x != None:
			self.input.append(x)
		while True:
			code = self.code()
			if code == 1:
				x, y, z = self.params(3)
				self.write(z, self.read(x) + self.read(y))
				self.pointer += 4
			elif code == 2:
				x, y, z = self.params(3)
				self.write(z, self.read(x) * self.read(y))
				self.pointer += 4
			elif code == 3:
				if(len(self.input) == 0):
					return
				x = self.params(1)[0]
				self.write(x, self.input[0])
				# self.write(x, ord(input()))
				self.input.pop(0)
				self.pointer += 2
			elif code == 4:
				x = self.params(1)[0]
				self.pointer += 2
				return self.read(x)
			elif code == 5:
				x, y = self.params(2)
				if self.read(x) != 0:
					self.pointer = self.read(y)
				else:
					self.pointer += 3
			elif code == 6:
				x, y = self.params(2)
				if self.read(x) == 0:
					self.pointer = self.read(y)
				else:
					self.pointer += 3
			elif code == 7:
				x, y, z = self.params(3)
				self.write(z, 1 if self.read(x) < self.read(y) else 0)
				self.pointer += 4
			elif code == 8:
				x, y, z = self.params(3)
				self.write(z, 1 if self.read(x) == self.read(y) else 0)
				self.pointer += 4
			elif code == 9:
				x = self.params(1)[0]
				self.relative_base += self.read(x)
				self.pointer += 2
			elif code == 99:
				return
			else:
				raise ValueError(self.memory)

data = list(map(int, open("input.txt").read().strip().split(",")))

nics = []
queues = []
for i in range(50):
	nic = intcode(data.copy())
	nics.append(nic)
	queues.append([])
	nic.run(i)

last_sent = None
nat = None

while True:
# for _ in range(2):
	inputs = []
	for i in range(50):
		if len(queues[i]) == 0:
			inputs.append(-1)
		else:
			inputs.append(queues[i][0])
			queues[i].pop(0)
	is_idle = reduce(lambda acc, x: acc and x == -1, inputs)
	if is_idle:
		if nat != None:
			if nat == last_sent:
				print(nat[1])
				exit()
			inputs[0] = nat
			last_sent = nat
	for i in range(50):
		nic = nics[i]
		if inputs[i] == -1:
			# print('Executing ' + str(i) + ' with -1')
			dest = nic.run(-1)
			if dest != None:
				(x, y) = (nic.run(None), nic.run(None))
				# print('Result: ' + str((x, y)) + ' -> ' + str(dest))
				if dest == 255:
					nat = (x, y)
				else:
					queues[dest].append((x, y))
		else:
			(x, y) = inputs[i]
			# print('Executing ' + str(i) + ' with ' + str((x, y)))
			nic.run(x)
			dest = nic.run(y)
			if dest != None:
				(x, y) = (nic.run(None), nic.run(None))
				# print('Result: ' + str((x, y)) + ' -> ' + str(dest))
				if dest == 255:
					nat = (x, y)
				else:
					queues[dest].append((x, y))