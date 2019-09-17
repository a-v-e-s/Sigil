from PIL import Image, ImageFont, ImageDraw, ImageOps
import os, random, chaos

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
