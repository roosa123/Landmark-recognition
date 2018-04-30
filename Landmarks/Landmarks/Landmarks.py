import os
import data_downloader
import data_provider

def download_data():
	csv_file = input("Type the CSV file name: ")

	if(csv_file[-4:] != ".csv"):
		csv_file += ".csv"

	print("Select the type of the CSV file (providing train data or test data):")

	file_type = input("A: train data\nB: test data\n")
		
	data_path = "data"

	if file_type in ('A', 'a'):
		os.path.join(data_path, "training")
	elif file_type in ('B', 'b'):
		os.path.join(data_path, "testing")
	else:
		print("Incorrect selection.")
		return

	if not os.path.exists(data_path):
		os.makedirs(data_path)
		
	data_downloader.Run(csv_file, data_path)

def perform(action_no):
	if action_no == 1:
		download_data()
	elif action_no == 2:
		return

def main():
	print("Available actions:\n")
	print("1 - download data. This option downloads the data from the Internet. "
		"It requires providing CSV file with labeled links."
		"To read more about format of the file, select option 5 - help)")
	print("2 - load the data. This option loads the data for training and testing from the hard drive.")
	print("3 - train. This option trains the network basing on the loaded data. "
		"Before running this option, you should load the data using option 2 - load the data")
	print("4 - test. This option loads trained model and performs testing on the loaded testing data. "
		"Before running this option, you should train the network using option 3 - train.")
	print("5 - about&help")
	print("6 - exit\n")

	command = input("Please select action: ")
	
	try:
		cmd_no = int(command)
	except:
		print("Incorrect selection.")
		return		# later change to continue

	perform(cmd_no)


main()