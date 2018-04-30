import os
import data_downloader
import data_provider

def download_data():
	csv_file = input("Type the CSV file name")

	if(csv_file[-4:] != ".csv"):
		csv_file += ".csv"

	print("Select the type of the CSV file (providing train data or test data):")

	file_type = input("A: train data\nB: test data\n")
		
	data_path = "data"

	if file_type in ('A', 'a'):
		data_path += "\\training"
	elif file_type in ('B', 'b'):
		data_path += "\\testing"
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
	command = input("Please select action:\n")
	
	try:
		cmd_no = int(command)
	except:
		print("Incorrect selection.")

	perform(cmd_no)


main()