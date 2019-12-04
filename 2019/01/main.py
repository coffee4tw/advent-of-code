def fuel(mass):
	return max(mass / 3 - 2, 0)

def rec_fuel(mass):
	if mass == 0:
		return 0
	else:
		return fuel(mass) + rec_fuel(fuel(mass))

file = open("input.txt")
part1 = 0
part2 = 0
for line in file:
	part1 += fuel(int(line))
	part2 += rec_fuel(int(line))

print("Part 1: " + str(part1))
print("Part 2: " + str(part2))