from PIL import Image
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt
import sqlite3
import cv2
import os

def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)   
    for i in arr:
        temp = (((i - min(arr))*diff)/diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr

def measures_of_pen_pressure(img):
	# grey_level_distribution, threshold value, no_black_pixel
	# get grayscale histogram of image
	t_min, t_max = 0, 1
	hist, bin = np.histogram(img.ravel(),256,[0,255])
	# normalize histogram
	norm_arr = normalize(bin, 0, 1)
	# sum
	gray_level_distribution = (np.sum(norm_arr))/len(norm_arr)    
	# threshold value
	thresh_val, thresh_img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	# no of black pixels
	no_black_pixels = np.sum(thresh_img == 0)
	return gray_level_distribution, thresh_val, no_black_pixels

# measures of writing movement
def no_of_contours(img):
	# no of interior and exterior contours
	ret, thresh = cv2.threshold(img, 127, 255, 0)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	hierarchy = hierarchy[0]

	interior_contours, exterior_contours = 0, 0 
	for x in list(range(len(contours))):
		current_hierarchy = hierarchy[x]
		current_contour = contours[x]

		if current_hierarchy[3] == 0 or current_hierarchy[3] == -1:
			exterior_contours += 1
		else:
			interior_contours += 1

	return interior_contours, exterior_contours

if __name__ == '__main__':
	conn = sqlite3.connect('forms.db')
	c = conn.cursor()

	the_1 = cv2.imread('the-1.png', 0)

	a_d = sorted([x for x in os.listdir('formsA-D')]) 
	e_h = sorted([x for x in os.listdir('formsE-H')]) 
	i_z = sorted([x for x in os.listdir('formsI-Z')]) 
	xmls = sorted([x for x in os.listdir('xml')])
	#print(xmls[:10])
	
	"""
	# extract the word 'the'
	file = open('xml/'+xmls[0], 'r')
	contents = file.read()
	file.close()	

	soup = BeautifulSoup(contents, 'xml')
	words = soup.find_all('word', {'text'})
	word = words[0]
	"""
	

	for xml in xmls[:1]:
		file = open('xml/'+xml, 'r')
		contents = file.read()
		file.close()

		soup = BeautifulSoup(contents, 'xml')
		words = soup.find_all('word', {'text':'the'})
		word = words[0]
		print(word)

	c.close()
	conn.close()