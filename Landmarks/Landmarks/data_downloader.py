from csv import reader as csv_reader
from urllib.request import urlretrieve
from threading import Thread
from os import path, makedirs, listdir
from shutil import move

def parse_data(data_file):
	try:
		csvfile = open(data_file, 'r')
	except:
		print("Unable to read file. Did you type the name correctly?")
		return []

	csvreader = csv_reader(csvfile)
	key_url_class_list = [line[:3] for line in csvreader]
	return key_url_class_list[1:]  # Chop off header


def download_image(key_url_class, out_dir):
	download_args_size = len(key_url_class)

	if download_args_size == 2:
		(key, url) = key_url_class
		filename = path.join(out_dir, '%s.jpg' % key)
	elif download_args_size == 3:
		(key, url, img_class) = key_url_class

		if img_class not in ("6651", "6696"):		# just temporarily
			return

		directory = path.join(out_dir, img_class)
		filename = path.join(directory, '%s_%s.jpg' % (img_class, key))

		if not path.exists(directory):
			makedirs(directory)
	else:
		print("Incorrect download arguments")
		return

	if path.exists(filename):
		print('Image %s already exists. Skipping download.' % filename)
		return

	try:
		urlretrieve(url, filename)
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
	
	# for i in range(len(key_url_class_list)):
	# 	t = Thread(target=download_image, args=(key_url_class_list[i], dest_dir))
	# 	threads.append(t)
	# 	t.start()
	
	# for i in range(len(key_url_class_list)):
	# 	threads[i].join()

	if validation_dir is not None:
		all_dirs = listdir(training_dir)

		for directory in all_dirs:
			next_train_dir = path.join(training_dir, directory)
			dst_val = path.join(validation_dir, directory)

			if not path.exists(dst_val):
				makedirs(dst_val)

			files = listdir(next_train_dir)
			change_dir = int(0.2 * len(files))

			for (i, next_file) in enumerate(files):
				src = path.join(next_train_dir, next_file)
				move(src, dst_val)

				if i == change_dir:
					break

	print("Download finished successfully. Data split into trainig and validation sets.")

def download_data():
	csv_file = input("Type the CSV file name: ")

	if(csv_file[-4:] != ".csv"):
		csv_file += ".csv"

	print("Select the type of the CSV file (providing train data or test data):")

	file_type = input("A: train data\nB: test data\n")
	
	data_path = "data"

	if file_type in ('A', 'a'):
		training_path = path.join(data_path, "training")
		validation_path = path.join(data_path, "validation")
		data_path = (training_path, validation_path)

		if not path.exists(training_path):
			makedirs(training_path)

		if not path.exists(validation_path):
			makedirs(validation_path)
	elif file_type in ('B', 'b'):
		data_path = path.join(data_path, "testing")
		
		if not path.exists(data_path):
			makedirs(data_path)
	else:
		print("Incorrect selection.")
		return
		
	run(csv_file, data_path)
