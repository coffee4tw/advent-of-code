history = ""

def opcode(memory, address):
	while True:
		code = memory[address] % 100
		mode_int = int(memory[address] / 100)
		mode = []
		for i in range(4):
			mode.append(mode_int % 10)
			mode_int = int(mode_int / 10)
		params = memory[address+1:address+4]
		global history
		history += "OPCODE: " + str(memory[address]) + " CODE: " + str(code) + " MODE: " + str(mode) + " PARAMS: " + str(params) + "\n"
		history += str(memory) + "\n"

		if code == 1:
			memory[params[2]] = (memory[params[0]] if mode[0] == 0 else params[0]) + (memory[params[1]] if mode[1] == 0 else params[1])
			history += "WROTE: " + str(memory[params[2]]) + " TO ADDRESS " + str(params[2]) + "\n"
			address += 4
		elif code == 2:
			memory[params[2]] = (memory[params[0]] if mode[0] == 0 else params[0]) * (memory[params[1]] if mode[1] == 0 else params[1])
			history += "WROTE: " + str(memory[params[2]]) + " TO ADDRESS " + str(params[2]) + "\n"
			address += 4
		elif code == 3:
			memory[params[0]] = int(input("Input: "))
			address += 2
		elif code == 4:
			out = memory[params[0]] if mode[0] == 0 else params[0]
			print(out)
			history = ""
			address += 2
		elif code == 5:
			if (memory[params[0]] if mode[0] == 0 else params[0]) != 0:
				address = memory[params[1]] if mode[1] == 0 else params[1]
			else:
				address += 3
		elif code == 6:
			if (memory[params[0]] if mode[0] == 0 else params[0]) == 0:
				address = memory[params[1]] if mode[1] == 0 else params[1]
			else:
				address += 3
		elif code == 7:
			memory[params[2]] = 1 if (memory[params[0]] if mode[0] == 0 else params[0]) < (memory[params[1]] if mode[1] == 0 else params[1]) else 0
			address += 4
		elif code == 8:
			memory[params[2]] = 1 if (memory[params[0]] if mode[0] == 0 else params[0]) == (memory[params[1]] if mode[1] == 0 else params[1]) else 0
			address += 4
		elif code == 99:
			return

file = open("input.txt")
content = file.read()
data = content.split(",")
data = list(map(int, data))
memory = data.copy()

opcode(memory, 0)