import functools
import random

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
robot = intcode(data)
area = dict()
direction = 1 # north (1), south (2), west (3), and east (4)
position = (0, 0)
oxygen = (0, 0)

def new_position(position, direction):
	if direction == 1:
		return (position[0], position[1] + 1)
	elif direction == 2:
		return (position[0], position[1] - 1)
	elif direction == 3:
		return (position[0] - 1, position[1])
	elif direction == 4:
		return (position[0] + 1, position[1])

def print_area(area):
	max_x, min_x = functools.reduce(lambda acc, x: (x[0] if x[0] > acc[0] else acc[0], x[0] if x[0] < acc[1] else acc[1]), area.keys())
	max_y, min_y = functools.reduce(lambda acc, x: (x[1] if x[1] > acc[0] else acc[0], x[1] if x[1] < acc[1] else acc[1]), area.keys())
	w = max_x - min_x
	h = max_y - min_y
	for i in range(h+1):
		line = ''
		for j in range(w+1):
			p = (j + min_x, max_y - i)
			if p in area:
				line += area[p]
			else:
				line += ' '
		print(line)

def get_valid_children(area, position, depth):
	children = []
	p = (position[0], position[1]+1)
	if p in area and area[p] in ['D', 'S', 'O', '.']:
		children.append((p, depth))
	p = (position[0], position[1]-1)
	if p in area and area[p] in ['D', 'S', 'O', '.']:
		children.append((p, depth))
	p = (position[0]+1, position[1])
	if p in area and area[p] in ['D', 'S', 'O', '.']:
		children.append((p, depth))
	p = (position[0]-1, position[1])
	if p in area and area[p] in ['D', 'S', 'O', '.']:
		children.append((p, depth))
	return children

def fully_explored(area):
	for p in area:
		if area[p] == '#':
			continue
		if (p[0], p[1]+1) not in area:
			return False
		if (p[0], p[1]-1) not in area:
			return False
		if (p[0]+1, p[1]) not in area:
			return False
		if (p[0]-1, p[1]) not in area:
			return False
	return True

area[position] = 'D'
while not fully_explored(area):
	area[position] = 'D'
	area[(0, 0)] = 'S'
	if oxygen != (0, 0):
		area[oxygen] = 'O'
	# 0: The repair droid hit a wall. Its position has not changed.
	# 1: The repair droid has moved one step in the requested direction.
	# 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
	status = robot.run(direction)
	if status == 0:
		area[new_position(position, direction)] = '#'
	elif status == 1:
		area[position] = '.'
		position = new_position(position, direction)
	elif status == 2:
		position = new_position(position, direction)
		area[position] = 'O'
		oxygen = position
	direction = random.randint(1, 4)
print_area(area)

min_depths = dict()
children = [((0, 0), 0)]
while len(children) != 0:
	next_children = []
	for child in children:
		if child[0] not in min_depths or min_depths[child[0]] > child[1]:
			min_depths[child[0]] = child[1]
			next_children.extend(get_valid_children(area, child[0], child[1] + 1))
	children = next_children
print(min_depths[oxygen])

min_depths = dict()
children = [(oxygen, 0)]
while len(children) != 0:
	next_children = []
	for child in children:
		if child[0] not in min_depths or min_depths[child[0]] > child[1]:
			min_depths[child[0]] = child[1]
			next_children.extend(get_valid_children(area, child[0], child[1] + 1))
	children = next_children
print(functools.reduce(lambda max, x: x if x > max else max, map(lambda x: min_depths[x], min_depths.keys())))