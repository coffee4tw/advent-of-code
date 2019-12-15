import functools

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
				line += str(area[p]) + ' '
			else:
				line += '### '
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

start = (0 , 0)
odygen = (0 , 0)

i, j = 0, 0
area = dict()
for line in open("area.txt"):
	j = 0
	for c in line:
		area[(j, i)] = c
		if c == 'S':
			start = (j, i)
		if c == 'O':
			oxygen = (j, i)
		j += 1
	i += 1

print_area(area)

min_depths = dict()
children = [(oxygen, 0)]
while len(children) != 0:
	next_children = []
	for child in children:
		if child[0] not in min_depths or min_depths[child[0]] > child[1]:
			min_depths[child[0]] = child[1]
			next_children.extend(get_valid_children(area, child[0], child[1] + 1))
	children = next_children

print(min_depths[oxygen])
print_area(min_depths)

print(functools.reduce(lambda max, x: x if x > max else max, map(lambda x: min_depths[x], min_depths.keys())))