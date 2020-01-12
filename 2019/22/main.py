import functools

def deal(deck):
	return deck[::-1]

def cut(deck, n):
	return deck[n:] + deck[:n]

def deal_inc(deck, n):
	new_deck = deck.copy()
	i = 0
	while len(deck) > 0:
		new_deck[i] = deck[0]
		deck.pop(0)
		i = (i + n) % len(new_deck)
	return new_deck

def i_deal(idx, length):
	return length - idx - 1

def i_cut(idx, num, length):
	return (length + idx + num) % length

def i_inc(idx, num, length):
	num = num % length
	for x in range(1, length):
		if ((num * x) % length == idx):
			return x 
	return 1

# deck = list(range(10))
# print(deal(deck))
# print(i_deal(5, 10))
# print(cut(deck, 3))
# print(i_cut(5, 3, 10))
# print(cut(deck, -4))
# print(i_cut(5, -4, 10))
# print(deal_inc(deck, 3))
# print(i_inc(5, 3, 10))

instructions = []
for line in open("input.txt"):
	if "deal into new stack" in line:
		instructions.append(("deal", 0))
	elif "deal with increment" in line:
		instructions.append(("inc", int(line.split(" ")[-1])))
	elif "cut" in line:
		instructions.append(("cut", int(line.split(" ")[-1])))

deck = list(range(10007))
for (ins, num) in instructions:
	if ins == "deal":
		deck = deal(deck)
	elif ins == "inc":
		deck = deal_inc(deck, num)
	elif ins == "cut":
		deck = cut(deck, num)
print(deck.index(2019))

instructions = instructions[::-1]
position = 2020
length = 119315717514047
iterations = 101741582076661

@functools.lru_cache(500)
def inv(n):
	return pow(n, length-2, length)

add = 0
mul = 1
for (ins, num) in instructions:
	if ins == "deal":
		mul = -1 * mul
		add = -1 * add + length - 1
	elif ins == "inc":
		mul = mul * inv(num) % length
		add = add * inv(num) % length
	elif ins == "cut":
		add = add + num + length
position = (position * pow(mul, iterations, length) + add * (pow(mul, iterations, length) - 1) * pow(mul-1, length - 2, length)) % length
print(position)