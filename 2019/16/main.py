from functools import reduce

def pattern(base, n, length):
	expanded = []
	for num in base:
		for i in range(n+1):
			expanded.append(num)
	while len(expanded) < length+1:
		expanded.extend(expanded)
	return expanded[1:length+1]

# Part 1
base = [0, 1, 0, -1]
# phase = [1, 2, 3, 4, 5, 6, 7, 8]
# phase = list(map(int, '03036732577212944063491565474664'))
phase = list(map(int, open("input.txt").read().strip()))

for i in range(100):
	for j in range(len(phase)):
		phase[j] = abs(reduce(lambda acc, x: acc+x, map(lambda x: x[0]*x[1], zip(phase, pattern(base, j, len(phase)))))) % 10
print(''.join(map(str, phase[0:8])))


# Part 2
# phase = list(map(int, open("input.txt").read().strip()))
phase = list(map(int, '03036732577212944063491565474664'))
offset = int(''.join(map(str, phase[:8])))

expanded = []
for _ in range(10000):
	for x in phase:
		expanded.append(x)
phase = expanded

# TODO more efficient algorithm...

# print(''.join(map(str, phase)))
print(''.join(map(str, phase[offset:offset+8])))