from bs4 import BeautifulSoup
from PIL import Image

import numpy as np
import sqlite3
import cv2
import os

def extract_word():
	return None

if __name__ == '__main__':
	#gl_dist, gl_thresh_val, n_black_pixels = measures_of_pen_pressure(img)
	#int_contours, ext_contours = no_of_contours(img)
	#n_pos, n_neg, n_ver, n_hor = slope_components(img)

	imgs = sorted([x for x in os.listdir('formsA-D')]) 
	#e_h = sorted([x for x in os.listdir('formsE-H')]) 
	#i_z = sorted([x for x in os.listdir('formsI-Z')]) 
	xmls = sorted([x for x in os.listdir('xml')])
	#print(xmls[:10])

	#img = Image.open('formsA-D/'+a_d[1], 0)
	xml = xmls[0]
	#img_np = cv2.imread('formsA-D/'+a_d[1], 0)
	img = Image.open('formsA-D/'+imgs[0])

	file = open('xml/'+xml, 'r')
	contents = file.read()
	file.close()

	soup = BeautifulSoup(contents, 'xml')
	word = soup.find('word', {'text':'Gaitskell'})
	chldn = word.findChildren()

		
	if len(chldn) == 1: # if word is annotated as one block
		attrs = chldn[0].attrs
		x, y = int(attrs['x']), int(attrs['y'])
		width, height = int(attrs['width']), int(attrs['height'])


	elif len(chldn) > 1: # separate blocks
		attrs = chldn[0].attrs
		x, y = int(attrs['x']), int(attrs['y'])
		height = int(attrs['height'])
		width = 0 #int(attrs['width']), int(attrs['height'])
		for alph in word.findChildren():
			attrs = alph.attrs
			width = width + int(attrs['width'])

	crop = img.crop((x, y, x+width, y+height))
	#crop.show()
	crop = np.array(crop)


	"""
	attrs = word.cmp.attrs
	x, y = int(attrs['x']), int(attrs['y'])
	width, height = int(attrs['width']), int(attrs['height'])
	"""
	#img = Image.open()
	#print(width, height, x, y)
	#the = img.crop((x, y, x+width, y+height))
	#the_np = np.array(the)
	
	#ret, thresh = cv2.threshold(the_np, 127, 255, 0)
	#contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#cv2.drawContours(the_np, contours, -1, (0,255,0), 3)

	#cv2.imshow('the_np', the_np)
	#cv2.waitKey(0)
	#crop = img_np[width:height, width+x:height+y] 
	#print(x, y, width, height)

	#cv2.imwrite('cropped.png', crop)
	cv2.imshow('crop', crop)
	cv2.waitKey(0)