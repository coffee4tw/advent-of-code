pos = [(1, 4, 4), (-4, -1, 19), (-15, -14, 12), (-17, 1, 10)]
# pos = [(-1, 0, 2), (2, -10, -7), (4, -8, 8), (3, 5, -1)]
vel = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

step = 0
while True:
	for i in range(len(pos)):
		for j in range(len(pos)):
			if i == j:
				continue
			x = vel[i][0] + (1 if pos[i][0] < pos[j][0] else (-1 if pos[i][0] > pos[j][0] else 0))
			y = vel[i][1] + (1 if pos[i][1] < pos[j][1] else (-1 if pos[i][1] > pos[j][1] else 0))
			z = vel[i][2] + (1 if pos[i][2] < pos[j][2] else (-1 if pos[i][2] > pos[j][2] else 0))
			vel[i] = (x, y, z)
	for i in range(len(pos)):
		pos[i] = (pos[i][0] + vel[i][0], pos[i][1] + vel[i][1], pos[i][2] + vel[i][2])
	step += 1

	if step == 1000:
		energy = 0
		for i in range(len(pos)):
			pot, kin = 0, 0
			for x in range(3):
				pot += abs(pos[i][x])		
				kin += abs(vel[i][x])
			energy += pot * kin
		print(energy)
		break

class planet:
	def __init__(self, pos):
		self.position = pos
		self.velocity = 0

	def __hash__(self):
		return hash((self.position, self.velocity))

	def __eq__(self, other):
		return (self.position, self.velocity) == (other.position, other.velocity)
		
	def gravity(self, planets):
		for p in planets:
			if self.position < p.position:
				self.velocity += 1
			elif self.position > p.position:
				self.velocity -= 1

	def move(self):
		self.position += self.velocity

def get_cycle(planets):
	n = 0
	states = {tuple(planets): n}
	while True:
		n += 1
		for p in planets:
			p.gravity(planets)
		for p in planets:
			p.move()
		if tuple(planets) in states:
			return n - states[tuple(planets)]
		else:
			states[tuple(planets)] = n

def gcd(a,b): 
    if a == 0: 
        return b 
    return gcd(b % a, a) 
 
def lcm(a):
	x = a[0]
	for i in a[1:]:
	  x = x*i/gcd(x, i)
	return x

x = get_cycle([planet(1), planet(-4), planet(-15), planet(-17)])
y = get_cycle([planet(4), planet(-1), planet(-14), planet(1)])
z = get_cycle([planet(4), planet(19), planet(12), planet(10)])
# x = get_cycle([planet(-1), planet(2), planet(4), planet(3)])
# y = get_cycle([planet(0), planet(-10), planet(-8), planet(5)])
# z = get_cycle([planet(2), planet(-7), planet(8), planet(-1)])

print((x, y, z))
print(lcm([x, y, z]))
