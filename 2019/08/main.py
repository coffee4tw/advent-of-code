def checksum(data, width, height):
	count = 1e32
	checksum = 0
	for i in range(int(len(data) / (width * height))):
		layer = data[i * width * height:(i + 1) * width * height]
		# print(''.join(map(str, layer)))
		x = len(list(filter(lambda x: x == 0, layer)))
		if x < count:
			count = x
			checksum = len(list(filter(lambda x: x == 1, layer))) * len(list(filter(lambda x: x == 2, layer)))
	return checksum

def decode(data, width, height):
	final = []
	for i in range(int(len(data) / (width * height))):
		layer = data[i * width * height:(i + 1) * width * height]
		# print(''.join(map(str, layer)))
		if len(final) == 0:
			final = layer.copy()
		else:
			for j in range(len(final)):
				if final[j] == 2:
					final[j] = layer[j]
	return final

data = list(map(int, open("test.txt").read().strip()))
print(checksum(data, 2, 2))
print(decode(data, 2, 2))

w, h = 25, 6
data = list(map(int, open("input.txt").read().strip()))
print(checksum(data, w, h))
image = decode(data, w, h)
for i in range(h):
	print(''.join(map(lambda x: u" #" if x == 1 else '  ', image[i*w:(i+1)*w])))