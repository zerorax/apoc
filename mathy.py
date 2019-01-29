import math
speed = 10


def get_bullet_xy(speed,xdir,ydir):
	if xdir == 0:
		if ydir < 0:
			return((0,-speed))
		else:
			return((0,speed))
	elif ydir == 0:
		if xdir < 0:
			return((-speed,0))
		else:
			return((speed,0))

	for x in range(speed):
		for y in range(speed):
			if round(math.isclose(math.sqrt(x*x + y*y), speed, rel_tol=0.5)):
				if ydir < 0:
					if xdir < 0:
						return((-x, -y))
					else:
						return((x, -y))
				elif xdir < 0:
					return((-x, y))
				else:
					return((x, y))


print(get_bullet_xy(8, 1,1))