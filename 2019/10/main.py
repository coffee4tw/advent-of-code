from math import atan2

asteroids = []
file = open("input.txt")
i, j = 0, 0
for line in file:
	for c in line.strip():
		if c == '#':
			asteroids.append((j, i))
		j += 1
	i += 1
	j = 0
# print(asteroids)

best = (0, 0)
max = 0
best_vectors = dict()
for (x, y) in asteroids:
	vectors = dict()
	for (a, b) in asteroids:
		if (x, y) == (a, b):
			continue
		(c, d) = (a - x, b - y)
		if c != 0:
			(c, d) = (c/abs(c), d/abs(c))
		else:
			(c, d) = (0, d/abs(d))
		if (c, d) not in vectors:
			vectors[(c, d)] = [(a - x, b - y)]
		else:
			vectors[(c, d)].append((a - x, b - y))
			vectors[(c, d)].sort(key=lambda x: abs(x[1]))

	# print((x, y))
	# print(len(vectors))
	if len(vectors) > max:
		best = (x, y)
		max = len(vectors)
		best_vectors = vectors

print(best)
print(max)

sorted = list(best_vectors.keys())
sorted.sort(key=lambda p:atan2(p[0], p[1]), reverse=True)
count = 0
index = 0
while count < 200:
	if index >= len(sorted):
		index = 0
	xs = best_vectors[sorted[index]]
	x, y = xs[0]
	print(str(count+1) + ": " + str((x+best[0], y+best[1])))
	xs.pop(0)
	if len(xs) == 0:
		del best_vectors[sorted[index]]
	count += 1
	index += 1