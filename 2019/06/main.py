def walk(x, depth):
	if x not in orbits:
		return depth
	else:
		sum = depth
		for y in orbits[x]:
			sum += walk(y, depth+1)
		return sum

def path(p, x):
	p.add(x)
	if x == "COM":
		return p
	else:
		return path(p, parent[x])

parent = {}
orbits = {}
file = open("input.txt")
for line in file:
	line = line.strip()
	a, b = line.split(")")
	if a in orbits:
		orbits[a].append(b)
	else:
		orbits[a] = [b]
	parent[b] = a

print("Part 1: " + str(walk("COM", 0)))

transfers = path(set(), "YOU").symmetric_difference(path(set(), "SAN"))
print("Part 2: " + str(len(transfers) - 2))