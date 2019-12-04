file = open("input.txt")
wires = []
for line in file:
	coordinates = {}
	x = 0
	y = 0
	steps = 0
	for instruction in line.split(","):
		num = int(instruction[1:])
		if instruction[0] == 'R':
			for i in range(num):
				x += 1
				steps += 1
				coordinates[(x, y)] = steps
		elif instruction[0] == 'L':
			for i in range(num):
				x -= 1
				steps += 1
				coordinates[(x, y)] = steps
		elif instruction[0] == 'U':
			for i in range(num):
				y += 1
				steps += 1
				coordinates[(x, y)] = steps
		elif instruction[0] == 'D':
			for i in range(num):
				y -= 1
				steps += 1
				coordinates[(x, y)] = steps
	wires.append(coordinates)

min_dist = -1
min_steps = -1
intersections = wires[0].keys() & wires[1].keys()
for intersection in intersections:
			steps = wires[0][intersection] + wires[1][intersection]
			dist = abs(intersection[0]) + abs(intersection[1])
			if min_dist == -1:
				min_dist = dist
			elif dist < min_dist:
				min_dist = dist
			if min_steps == -1:
				min_steps = steps
			elif steps < min_steps:
				min_steps = steps

print("Part 1: " + str(min_dist))
print("Part 2: " + str(min_steps))
