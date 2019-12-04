import re

count = 0

start = 165432
end = 707912
num = start
while num <= end:
	str_num = str(num)
	if str_num[0] == str_num[1] or str_num[1] == str_num[2] or str_num[2] == str_num[3] or str_num[3] == str_num[4] or str_num[4] == str_num[5]:
		if int(str_num[0]) <= int(str_num[1]) <= int(str_num[2]) <= int(str_num[3]) <= int(str_num[4]) <= int(str_num[5]):
			count += 1
	num += 1
print("Part 1: " + str(count))

count = 0

start = 165432
end = 707912
num = start
while num <= end:
	str_num = str(num)
	if int(str_num[0]) <= int(str_num[1]) <= int(str_num[2]) <= int(str_num[3]) <= int(str_num[4]) <= int(str_num[5]):
		for x in range(10):
			if re.search("([^"+str(x)+"]|^)"+str(x)+"{2}([^"+str(x)+"]|$)", str_num):
				count += 1
				break
	num += 1
print("Part 2: " + str(count))
