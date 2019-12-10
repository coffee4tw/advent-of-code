class boost:
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
				x = self.params(1)[0]
				self.write(x, self.input[0])
				self.input.pop(0)
				self.pointer += 2
			elif code == 4:
				x = self.params(1)[0]
				self.pointer += 2
				print(self.read(x))
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
# data = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
# data = [1102,34915192,34915192,7,4,7,99,0]
# data = [104,1125899906842624,99]
print(boost(data.copy()).run(2))

