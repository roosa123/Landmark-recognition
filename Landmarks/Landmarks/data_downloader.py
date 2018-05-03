import sys, os, multiprocessing, urllib.request, csv, threading
from io import StringIO
from shutil import move

def parse_data(data_file):
	try:
		csvfile = open(data_file, 'r')
	except:
		print("Unable to read file. Did you type the name correctly?")
		return []

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

		if img_class not in ("6651", "6696"):		# just temporarily
			return

		directory = os.path.join(out_dir, img_class)
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
	print("\nRunning download...")

	key_url_class_list = parse_data(csv_file)

	threads = []
	validation_dir = None

	if len(output_dir) == 2:
		(training_dir, validation_dir) = output_dir
		dest_dir = training_dir
	else:
		dest_dir = output_dir
	
	for i in range(len(key_url_class_list)):
		t = threading.Thread(target=download_image, args=(key_url_class_list[i], dest_dir))
		threads.append(t)
		t.start()
	
	for i in range(len(key_url_class_list)):
		threads[i].join()

	if validation_dir is not None:
		all_dirs = os.listdir(training_dir)

		for directory in all_dirs:
			next_train_dir = os.path.join(training_dir, directory)
			next_val_dir = os.path.join(validation_dir, directory)
			files = os.listdir(next_train_dir)
			change_dir = int(0.2 * len(files))

			for (i, next_file) in enumerate(files):
				src = os.path.join(next_train_dir, next_file)
				dst = os.path.join(next_val_dir, next_file)
				move(src, dst)

				if i == change_dir:
					break

	print("Download finished successfully. Data split into trainig and validation sets.")
