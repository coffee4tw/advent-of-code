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

def check(x, y):
	drone = intcode(data.copy())
	drone.run(x)
	return drone.run(y) == 1

data = list(map(int, open("input.txt").read().strip().split(",")))
drone = intcode(data.copy())

top = (0, 0)
bottom = (0, 0)
count = 0
for y in range(50):
	line = ""
	i, o = False, False
	for x in range(50):
		if check(x, y) == 1:
			count += 1
			line += "#"
			if not i:
				i = True
				bottom = (x, y)
		else:
			line += "."
			if i and not o:
				o = True
				top = (x-1, y)
	print(line)
print(count)

size = 99
x, y = 10, 0
while True:
	if check(x+size, y):
		if check(x, y+size):
			print((x, y))
			print(x*10000+y)
			break
		else:
			x += 1
	else:
		y += 1