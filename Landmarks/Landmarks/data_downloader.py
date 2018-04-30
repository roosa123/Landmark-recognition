#!/usr/bin/python

# Note to Kagglers: This script will not run directly in Kaggle kernels. You
# need to download it and run it on your local machine.

# Downloads images from the Google Landmarks dataset using multiple threads.
# Images that already exist will not be downloaded again, so the script can
# resume a partially completed download. All images will be saved in the JPG
# format with 90% compression quality.

import sys, os, multiprocessing, urllib.request, csv
from PIL import Image
from io import StringIO

def ParseData(data_file):
	csvfile = open(data_file, 'r')
	csvreader = csv.reader(csvfile)
	key_url_class_list = [line[:3] for line in csvreader]
	return key_url_class_list[1:]  # Chop off header


def DownloadImage(key_url_class, out_dir):
	#out_dir = sys.argv[2]
	(key, url, img_class) = key_url_class
	filename = os.path.join(out_dir, '%s_%s.jpg' % (img_class, key))

	if img_class not in ("6651", "6696"):
		return

	if os.path.exists(filename):
		print('Image %s already exists. Skipping download.' % filename)
		return

	try:
		response = urllib.request.urlretrieve(url, filename)
		#image_data = response.read()
	except:
		print('Warning: Could not download image %s from %s' % (key, url))
		return

def Run(csv_file, output_dir):
	#if len(sys.argv) != 3:
		#print('Syntax: %s <data_file.csv> <output_dir/>' % sys.argv[0])
		#sys.exit(0)
		#(data_file, out_dir) = sys.argv[1:]

	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	key_url_class_list = ParseData(data_file)
	pool = multiprocessing.Pool(processes=50)
	pool.map(DownloadImage, key_url_class_list)
