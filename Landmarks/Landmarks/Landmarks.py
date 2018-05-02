from os import path, makedirs
from data_downloader import run
from network import run_training, build_network
from classify import classify
from keras.models import Sequential

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

def perform(action_no, model = None):
	if action_no == 1:
		download_data()
	elif action_no == 2:
		model = build_network()
		#run_training(model)
	elif action_no == 3:
		classify(model)
	else:
		return

	return model

def main():
	cmd_no = 0
	model = None

	while cmd_no != 5:
		print("\nAvailable actions:\n")
		print("1 - download data. This option downloads the data from the Internet. "
			"The action requires providing CSV file with labeled links. "
			"To read more about format of the file, select option 4 - about&help)")
		print("2 - train. This option trains the network basing on the loaded data. "
			"Before running this option, you should load the data using option 1 - download the data. "
			"For details, use option 4 - about&help")
		print("3 - test. This option loads trained model and performs testing on the loaded testing data. "
			"Before running this option, you should train the network using option 2 - train. "
			"For details, use option 4 - about&help.")
		print("4 - about&help")
		print("5 - exit\n")

		command = input("Please select action (type in the number of desired option): ")
		
		try:
			cmd_no = int(command)
		except:
			print("Incorrect selection.")
			continue

		if model is None:
			model = perform(cmd_no)
		else:
			perform(cmd_no, model=model)
	
	print("Exiting program.")


main()