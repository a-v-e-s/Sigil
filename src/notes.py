from PIL import Image, ImageFont, ImageDraw, ImageOps
import os, random, chaos, math

def list_pixels(phrase):
	font_options = []
	for x in os.listdir('fonts'):
		font_options.append(os.path.join(os.getcwd(), 'fonts', x))

	font = ImageFont.truetype(font=random.choice(font_options), size=48, encoding='unic')
	text_width, text_height = font.getsize(phrase)
	canvas = Image.new('L', (text_width, text_height), "white")
	draw = ImageDraw.Draw(canvas)
	draw.text((0, 0), phrase, 'black', font)
	pixels = canvas.getdata()
	return list(pixels)

def text_img(phrase):
	font_options = []
	for x in os.listdir('fonts'):
		font_options.append(os.path.join(os.getcwd(), 'fonts', x))

	font = ImageFont.truetype(font=random.choice(font_options), size=48, encoding='unic')
	text_width, text_height = font.getsize(phrase)
	canvas = Image.new('L', (text_width, text_height), "white")
	draw = ImageDraw.Draw(canvas)
	draw.text((0, 0), phrase, 'black', font)
	canvas.show()

def regrid(width=24, height=30, pixies=0):
	# x, xc, y, grid, pixies = regrid()
	if pixies == 0:
		pixies = width * height / 3
	grid = [[0 for x in range(width)] for x in range(height)]
	x = random.randint(0, width-1)
	xc = x
	y = random.randint(0, height-1)
	grid[y][x] = 1
	# x is now a list for some reason so beware...
	return x, xc, y, grid, pixies


def grid(width=24, height=30, pixies=0):
	points = width * height
	if pixies == 0:
		pixies = points / 3
	grid = [[0 for x in range(width)] for x in range(height)]
	x = random.randint(0, width-1)
	xc = x
	y = random.randint(0, height-1)
	#
	grid[y][x] = 1
	blacks = [(y,x)]
	new_blacks = [True, -1]
	pixies -= 1
	#
	# x may now be a list for some reason so beware...
	#
	use_these = []
	while pixies > 0:
		if new_blacks[0] == True:
			for a in range(-1, (new_blacks[1] - 1), -1):
				use_these.append(blacks[a])
			new_blacks = [False, 0]
			used = False
		for b in use_these:
			y = b[0]
			xc = b[1]
			if xc > 0:
				h = xc - 1
				if grid[y][h] != 1 and random.random() <= pixies/points:
					grid[y][h] = 1
					blacks.append((y,h))
					used = True
					new_blacks[0] = True
					new_blacks[1] -= 1
					pixies -= 1
			if y > 0:
				j = y - 1
				if grid[j][xc] != 1 and random.random() <= pixies/points:
					grid[j][xc] = 1
					blacks.append((j,xc))
					used = True
					new_blacks[0] = True
					new_blacks[1] -= 1
					pixies -= 1
			if y < height-2:
				k = y + 1
				if grid[k][xc] != 1 and random.random() <= pixies/points:
					grid[k][xc] = 1
					blacks.append((k,xc))
					used = True
					new_blacks[0] = True
					new_blacks[1] -= 1
					pixies -= 1
			if xc < width-2:
				l = xc + 1
				if grid[y][l] != 1 and random.random() <= pixies/points:
					grid[y][l] = 1
					blacks.append((y,l))
					used = True
					new_blacks[0] = True
					new_blacks[1] -= 1
					pixies -= 1