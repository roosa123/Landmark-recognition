import os
import data_downloader
import data_provider
import network

def download_data():
	csv_file = input("Type the CSV file name: ")

	if(csv_file[-4:] != ".csv"):
		csv_file += ".csv"

	print("Select the type of the CSV file (providing train data or test data):")

	file_type = input("A: train data\nB: test data\n")
		
	data_path = "data"

	if file_type in ('A', 'a'):
		data_path = os.path.join(data_path, "training")
	elif file_type in ('B', 'b'):
		data_path = os.path.join(data_path, "testing")
	else:
		print("Incorrect selection.")
		return

	if not os.path.exists(data_path):
		os.makedirs(data_path)
		
	data_downloader.run(csv_file, data_path)

# def load_data():
# 	print("Select type of the loaded data:")
# 	load_type = input("A - train data\nB - test data\nC - both\n")

# 	data_path = "data"

# 	if load_type in ('A', 'a'):
# 		data_path = os.path.join(data_path, "training")
# 	elif load_type in ('B', 'b'):
# 		data_path = os.path.join(data_path, "testing")
# 	else:
# 		training_path = os.path.join(data_path, "training")
# 		testing_path= os.path.join(data_path, "testing")
# 		data_path = (training_path, testing_path)

# 	data_provider.run(data_path)

def perform(action_no):
	if action_no == 1:
		download_data()
	elif action_no == 2:
		network.train()

def main():
	while True:
		print("\nAvailable actions:\n")
		print("1 - download data. This option downloads the data from the Internet. "
			"The action requires providing CSV file with labeled links."
			"To read more about format of the file, select option 4 - about&help)")
		print("2 - train. This option trains the network basing on the loaded data. "
			"Before running this option, you should load the data using option 1 - download the data"
			"For details, use option 4 - about&help")
		print("3 - test. This option loads trained model and performs testing on the loaded testing data. "
			"Before running this option, you should train the network using option 2 - train."
			"For details, use option 4 - about&help.")
		print("4 - about&help")
		print("5 - exit\n")

		command = input("Please select action (type in the number of desired option): ")
		
		try:
			cmd_no = int(command)
		except:
			print("Incorrect selection.")
			continue

		if cmd_no == 5:
			print("Exiting program.")
			break
		else:
			perform(cmd_no)

main()