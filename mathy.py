import math

speed = 10


def get_bullet_xy(speed,xstart,ystart, xtarget, ytarget):

	if xstart < xtarget:
		xdir = 1
	elif xstart > xtarget:
		xdir = -1
	else:
		xdir = 0

	if ystart < ytarget:
		ydir = 1
	elif ystart > ytarget:
		ydir = -1
	else:
		ydir = 0

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

	distance = [xstart - xtarget, ystart - ytarget]
	norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
	direction = [distance[0] / norm, distance[1] / norm]
	vector = [direction[0] * math.sqrt(speed), direction[1] * math.sqrt(speed)]
	rise = vector[1] * speed
	run = vector[0] * speed
	print( str(run) + " " + str(rise))


get_bullet_xy(1, 200, 130, 0, 0)
