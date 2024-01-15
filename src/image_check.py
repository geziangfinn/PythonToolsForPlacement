import argparse
import cv2
import numpy as np
import os
argParser = argparse.ArgumentParser(description='manual to this script')
argParser.add_argument("-path", type=str, default="")
args=argParser.parse_args()
path = args.path
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
for x in range(img.shape[0]):   # 图片的高
	for y in range(img.shape[1]):   # 图片的宽
		px = img[x,y]
		if px > 254:
			print("Yes")