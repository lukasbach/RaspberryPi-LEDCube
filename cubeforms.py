def formLine(x1, y1, z1, x2, y2, z2):
	linelength = round(math.sqrt(abs(x1 - x2) * abs(x1 - x2) + abs(y1 - y2) * abs(y1 - y2) + abs(z1 - z2) * abs(z1 - z2)))
	xDifferencePerStep = abs(x1 - x2) / linelength
	yDifferencePerStep = abs(y1 - y2) / linelength
	zDifferencePerStep = abs(z1 - z2) / linelength

	for i in range(0, linelength):
		setLedState(x1 + xDifferencePerStep * (i - 1), y1 + yDifferencePerStep * (i - 1), z1 + zDifferencePerStep * (i - 1)), True)
	return

def formRect(x1, y1, z1, x2, y2, z2):
	corner1 = [x1, y1, z1]
	corner2 = [x2, y2, z1]
	corner3 = [x1, y1, z2]
	corner4 = [x2, y2, z2]

	formLine(corner1[0], corner1[1], corner1[2], corner2[0], corner2[1], corner2[2])
	formLine(corner2[0], corner2[1], corner2[2], corner3[0], corner3[1], corner3[2])
	formLine(corner3[0], corner3[1], corner3[2], corner4[0], corner4[1], corner4[2])
	formLine(corner4[0], corner4[1], corner4[2], corner1[0], corner1[1], corner1[2])
	return

def formCube(x1, y1, z1, x2, y2, z2):
	corner1 = [x1, y1, z1]
	corner2 = [x2, y1, z1]
	corner3 = [x1, y2, z1]
	corner4 = [x2, y2, z1]
	corner5 = [x1, y1, z2]
	corner6 = [x2, y1, z2]
	corner7 = [x1, y2, z2]
	corner8 = [x2, y2, z2]

	formRect(corner1[0], corner1[1], corner1[2], corner6[0], corner6[1], corner6[2])
	formRect(corner5[0], corner5[1], corner5[2], corner8[0], corner8[1], corner8[2])
	formRect(corner3[0], corner3[1], corner3[2], corner8[0], corner8[1], corner8[2])
	formRect(corner1[0], corner1[1], corner1[2], corner4[0], corner4[1], corner4[2])
	formRect(corner1[0], corner1[1], corner1[2], corner7[0], corner7[1], corner7[2])
	formRect(corner2[0], corner2[1], corner2[2], corner8[0], corner8[1], corner8[2])
	return