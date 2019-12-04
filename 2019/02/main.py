def intcode(data):
	position = 0
	while data[position] != 99:
		if data[position] == 1:
			data[data[position+3]] = data[data[position+1]] + data[data[position+2]]
		elif data[position] == 2:
			data[data[position+3]] = data[data[position+1]] * data[data[position+2]]
		else:
			raise ValueError
		position += 4
	return data

file = open("input.txt")
content = file.read()
data = content.split(",")
data = list(map(int, data))
memory = data.copy()

memory[1] = 12
memory[2] = 2

print(intcode([1,0,0,0,99]) == [2,0,0,0,99])
print(intcode([2,3,0,3,99]) == [2,3,0,6,99])
print(intcode([2,4,4,5,99,0]) == [2,4,4,5,99,9801])
print(intcode([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99])
print("Part 1: " + str(intcode(memory)[0]))

for noun in range(100):
	for verb in range(100):
		memory = data.copy()
		memory[1] = noun
		memory[2] = verb
		if intcode(memory)[0] == 19690720:
			print("Part 2: " + str(100 * noun + verb))
			break