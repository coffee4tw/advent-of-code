import math
reactions = dict()

class reaction:
	def __init__(self, elem, num, inputs):
		self.elem = elem
		self.produces = num
		self.produced = 0
		self.consumed = 0
		self.inputs = inputs

	def run(self, n):
		self.produced += self.produces * n
		if self.inputs != None:
			for x in self.inputs:
				reactions[x[0]].get(x[1] * n)

	def get(self, num):
		self.consumed += num
		self.run(math.ceil((self.consumed - self.produced) / self.produces))

reactions["ORE"] = reaction("ORE", 1, None)

file = open("input.txt")
for line in file:
	i, o = line.split("=>")
	ins = i.split(",")
	onum, oelem = o.strip().split(" ")
	inputs = []
	for x in ins:
		inum, ielem = x.strip().split(" ")
		inputs.append((ielem, int(inum)))
	reactions[oelem] = reaction(oelem, int(onum), inputs)

reactions["FUEL"].get(1)
max_ore_per_fuel = reactions["ORE"].consumed
print(max_ore_per_fuel)

count = 1
max_ore = 1000000000000
while reactions["ORE"].consumed < max_ore:
	num = math.ceil((max_ore - reactions["ORE"].consumed) / max_ore_per_fuel)
	reactions["FUEL"].get(num)
	count += num
print(count-1)