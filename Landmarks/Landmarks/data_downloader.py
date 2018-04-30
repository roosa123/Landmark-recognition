import sys, os, multiprocessing, urllib.request, csv, threading
from PIL import Image
from io import StringIO

def parse_data(data_file):
	csvfile = open(data_file, 'r')
	csvreader = csv.reader(csvfile)
	key_url_class_list = [line[:3] for line in csvreader]
	return key_url_class_list[1:]  # Chop off header


def download_image(key_url_class, out_dir):
	download_args_size = len(key_url_class)

	if download_args_size == 2:
		(key, url) = key_url_class
		filename = os.path.join(out_dir, '%s.jpg' % key)
	elif download_args_size == 3:
		(key, url, img_class) = key_url_class

		if img_class not in ("6651", "6696"):
			return

		directory = os.path.join(out_dir, '%s' % img_class)
		filename = os.path.join(directory, '%s_%s.jpg' % (img_class, key))

		if not os.path.exists(directory):
			os.makedirs(directory)
	else:
		print("Incorrect download arguments")
		return

	if os.path.exists(filename):
		print('Image %s already exists. Skipping download.' % filename)
		return

	try:
		urllib.request.urlretrieve(url, filename)
	except:
		print('Warning: Could not download image %s from %s' % (key, url))
		return

def run(csv_file, output_dir):
	print("Running download")

	key_url_class_list = parse_data(csv_file)

	threads = []

	for i in range(len(key_url_class_list)):
		t2 = threading.Thread(target=download_image, args=(key_url_class_list[i], output_dir))
		threads.append(t2)
		t2.start()
	
	for i in range(len(key_url_class_list)):
		threads[i].join()

