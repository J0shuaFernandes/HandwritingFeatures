from PIL import Image
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt
import sqlite3
import cv2
import os

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