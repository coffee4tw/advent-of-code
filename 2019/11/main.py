class paint:
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

data = list(map(int, open("input.txt").read().strip().split(",")))
# data = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
# data = [1102,34915192,34915192,7,4,7,99,0]
# data = [104,1125899906842624,99]
panels = dict()
current = (0,0)
panels[current] = 1
direction = 0
robot = paint(data.copy())
while True:
	color = robot.run(panels[current] if current in panels else 0)
	if color == None:
		break
	else:
		panels[current] = color
	turn = robot.run(None)
	if turn == 0:
		direction = (direction + 3) % 4
	elif turn == 1:
		direction = (direction + 1) % 4
	if direction == 0:
		current = (current[0], current[1]+1)
	elif direction == 1:
		current = (current[0]+1, current[1])
	elif direction == 2:
		current = (current[0], current[1]-1)
	elif direction == 3:
		current = (current[0]-1, current[1])

print(len(panels))

ks = list(panels.keys())
min_x, min_y = 1e32, 1e32
max_x, max_y = -1e32, -1e32
for k in ks:
	if k[0] > max_x:
		max_x = k[0]
	if k[0] < min_x:
		min_x = k[0]
	if k[1] > max_y:
		max_y = k[1]
	if k[1] < min_y:
		min_y = k[1]
w = max_x - min_x
h = max_y - min_y
for i in range(h+1):
	line = ''
	for j in range(w+1):
		p = (j + min_x, max_y - i)
		if p in panels:
			line += ' #' if panels[p] == 1 else ' .'
		else:
			line += ' .'
	print(line)
