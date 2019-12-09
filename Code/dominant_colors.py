import cv2
import numpy as np
from skimage import io
import glob
import re

# Adapted from https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
n_colors = 3
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
flags = cv2.KMEANS_RANDOM_CENTERS

f = open("colors.csv", "w")
header = "Timestamp"
for i in range(n_colors):
	header += " color_" + str(i + 1) + "_R"
	header += " color_" + str(i + 1) + "_G"
	header += " color_" + str(i + 1) + "_B"
	header += " color_" + str(i + 1) + "_proportion"
f.write(header + "\n")

img_paths = glob.glob("images/*.jpg")

j = 0

for path in img_paths:
	if re.search(r".*((UTC)|(_1)).jpg", path) is None:
		continue
	img = io.imread(path, plugin='matplotlib')

	pixels = np.float32(img.reshape(-1, 3))

	_, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
	_, counts = np.unique(labels, return_counts=True)
	indices = np.argsort(counts)[::-1] 

	clr_ordered = palette[indices]
	counts_ordered = counts[indices]
	
	out = [re.findall(r"\/(.*)_UTC", path)[0]]
	for i in range(n_colors):
		out.append(str(clr_ordered[i, 0]))
		out.append(str(clr_ordered[i, 1]))
		out.append(str(clr_ordered[i, 2]))
		out.append(str(counts_ordered[i]/sum(counts_ordered)))
	f.write(" ".join(out) + "\n")

	j += 1
	if j % 50 == 49:
		print(j+1)

f.close()
