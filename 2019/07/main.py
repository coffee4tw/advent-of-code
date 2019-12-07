class amplifier:
	def __init__(self, memory, phase):
		self.address = 0
		self.memory = memory
		self.input = [phase]

	def code(self):
		return self.memory[self.address] % 100

	def params(self, n):
		mode_int = int(self.memory[self.address] / 100)
		params = []
		for i in range(n):
			mode = mode_int % 10
			mode_int = int(mode_int / 10)
			params.append(self.memory[self.memory[self.address+1+i]] if mode == 0 else self.memory[self.address+1+i])
		# print(self.code())
		# print(params)
		# print(self.memory[self.address:self.address+n+1])
		return params

	def run(self, x):
		self.input.append(x)
		while True:
			code = self.code()

			if code == 1:
				x, y = self.params(2)
				self.memory[self.memory[self.address+3]] = x + y
				self.address += 4
			elif code == 2:
				x, y = self.params(2)
				self.memory[self.memory[self.address+3]] = x * y
				self.address += 4
			elif code == 3:
				self.memory[self.memory[self.address+1]] = self.input[0]
				self.input.pop(0)
				self.address += 2
			elif code == 4:
				x = self.params(1)[0]
				self.address += 2
				return x
			elif code == 5:
				x, y = self.params(2)
				if x != 0:
					self.address = y
				else:
					self.address += 3
			elif code == 6:
				x, y = self.params(2)
				if x == 0:
					self.address = y
				else:
					self.address += 3
			elif code == 7:
				x, y = self.params(2)
				self.memory[self.memory[self.address+3]] = 1 if x < y else 0
				self.address += 4
			elif code == 8:
				x, y = self.params(2)
				self.memory[self.memory[self.address+3]] = 1 if x == y else 0
				self.address += 4
			elif code == 99:
				return

file = open("input.txt")
content = file.read()
data = content.split(",")
data = list(map(int, data))

# regular mode
max = 0
for i in range(5):
	for j in range(5):
		if j == i:
			continue
		for k in range(5):
			if k == i or k == j:
				continue
			for l in range(5):
				if l == i or l == j or l == k:
					continue
				for m in range(5):
					if m == i or m == j or m == k or m == l:
						continue
					a = amplifier(data.copy(), i)
					b = amplifier(data.copy(), j)
					c = amplifier(data.copy(), k)
					d = amplifier(data.copy(), l)
					e = amplifier(data.copy(), m)
					signal = 0
					while True:
						loop = e.run(d.run(c.run(b.run(a.run(signal)))))
						if loop != None:
							signal = loop
						else:
							break
					# exit()
					if signal > max:
						max = signal
print(max)

#  feedback loop mode
max = 0
for i in range(5,10):
	for j in range(5,10):
		if j == i:
			continue
		for k in range(5,10):
			if k == i or k == j:
				continue
			for l in range(5,10):
				if l == i or l == j or l == k:
					continue
				for m in range(5,10):
					if m == i or m == j or m == k or m == l:
						continue
					a = amplifier(data.copy(), i)
					b = amplifier(data.copy(), j)
					c = amplifier(data.copy(), k)
					d = amplifier(data.copy(), l)
					e = amplifier(data.copy(), m)
					signal = 0
					while True:
						loop = e.run(d.run(c.run(b.run(a.run(signal)))))
						if loop != None:
							signal = loop
						else:
							break

					if signal > max:
						max = signal
print(max)