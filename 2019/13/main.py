class arcade:
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
data[0] = 2
game = arcade(data)
score = 0
tiles = []
for i in range(50):
	tiles.append([])
	for j in range(50):
		tiles[i].append('  ')

ball = 0
paddle = 0
joystick = None
while True:
	while True:
		x = game.run(joystick)
		joystick = None
		if x == None:
			break
		y = game.run(None)
		z = game.run(None)
		if x == -1 and y == 0:
			score = z
		elif z == 0:
			tiles[y][x] = '  '
		elif z == 1:
			tiles[y][x] = '||'
		elif z == 2:
			tiles[y][x] = ' #'
		elif z == 3:
			tiles[y][x] = ' _'
			paddle = x
		elif z == 4:
			tiles[y][x] = ' o'
			ball = x
	print('Score: ' + str(z))
	count = 0
	for i in range(len(tiles)):
		line = ''
		for j in range(len(tiles[i])):
			line += tiles[i][j]
			if tiles[i][j] == ' #':
				count += 1
		print(line)
	print(count)
	joystick = 1 if ball > paddle else (0 if ball == paddle else -1)
	if count == 0:
		break
