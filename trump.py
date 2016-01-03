import argparse
import os
import sys

import cv
import scipy as sp
import imagehash
from PIL import Image, ImageDraw, ImageFont


font_fname = 'font.ttf'
font_size = 25

font = ImageFont.truetype(font_fname, font_size)

FACE_CASCADE = cv.Load('haarcascade_frontalface_alt.xml')

def box_in_box(a, b):
	"""Returns True if box a and box b overlap"""
	ax, ay, aw, ah = a
	bx, by, bw, bh = b
	return ax < bx+bw and ax+aw > bx and ay < by+bh and ay+ah > by


def faces_filter(rects):
	"""Filter and sort face boxes, removing overlapping boxes (keeping the smallest)"""
	rects = sorted(rects, key=lambda r: r[2] * r[3])
	output = []
	for rect in rects:
		conflicted = False
		for output_rect in output:
			conflicted = conflicted or box_in_box(rect, output_rect)
		if not conflicted:
			output.append(rect)
	return list(reversed(output))


def face_rects(rgba_image_f):
	"""Returns a list of tuples of face rectangles, (x, y, w, h)"""
	grayscale = cv.LoadImage(rgba_image_f, cv.CV_LOAD_IMAGE_GRAYSCALE)
	cv.EqualizeHist(grayscale, grayscale)
	faces = cv.HaarDetectObjects(grayscale, FACE_CASCADE,
								 cv.CreateMemStorage(0), 1.2, 2,
								 cv.CV_HAAR_DO_CANNY_PRUNING, (50,50))
	return faces_filter([rect for (rect, _) in faces])


def overlay_alpha_png(rgba_image, rgba_overlay, face_rect):
	"""Returns a PIL image with the alpha image on top"""
	x, y, w, h = face_rect
	c_x, c_y = x + w/2, y + h/2
	rgba_overlay = rgba_overlay.resize((int(w*1.3), int(h*1.3)), Image.ANTIALIAS)
	size = rgba_overlay.size
	box = (c_x - size[0]/2 + 10,
		   c_y - size[1]/2 - 45,
		   c_x - size[0]/2 + size[0] + 10,
		   c_y - size[1]/2 + size[1] - 45)

	rgba_image.paste(rgba_overlay, box, rgba_overlay)

	return rgba_image


def trumpify(filename):
	inp = filename
	original = Image.open(inp).convert('RGBA')
	rects = face_rects(inp)
	width, height = original.size
	for overlay_fname in ['hair.png']:
		overlay = Image.open(overlay_fname).convert('RGBA')
		for rect in rects:
			original = overlay_alpha_png(original, overlay, rect)

	overlay_alpha_png(original, Image.open('logo.png').convert('RGBA'), (width - 225,height - 50,200,100))
	width, height = original.size


	# draw = ImageDraw.Draw(original)
	# draw.text((0, height - 50), "Made with love at trumpifyme.me", font=font, fill='rgb(0, 0, 255)')
	hashval = imagehash.average_hash(original)
	print hashval
	original.save('outs/' + str(hashval) + '.png')
	return str(hashval) + '.png'

if __name__ == '__main__':
	trumpify('../jamo.jpg')