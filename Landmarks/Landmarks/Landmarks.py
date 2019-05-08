from data_downloader import download_data
from network import run_training
from classify import run_classification
from help_about import show_help

def perform(action_no):
	if action_no == 1:
		download_data()
	elif action_no == 2:
		run_training()
	elif action_no == 3:
		run_classification()
	elif action_no == 4:
		show_help()
	elif action_no == 5:
		print("Exiting program.")
	else:
		print("There's no such option.")

if __name__ == '__main__':
	cmd_no = 0

	while cmd_no != 5:
		print("\nAvailable actions:\n")
		print("1 - download data. This option downloads the data from the Internet.\n"
			"\tThe action requires providing CSV file with labeled links.\n"
			"\tTo read more about format of the file, select option 4 - about&help)")
		print("2 - train. This option trains the network basing on the loaded data.\n"
			"\tBefore running this option, you should load the data using option 1 - download the data.\n"
			"\tFor details, use option 4 - about&help")
		print("3 - test. This option loads trained model and performs testing on the loaded testing data.\n"
			"\tBefore running this option, you should train the network using option 2 - train.\n"
			"\tFor details, use option 4 - about&help.")
		print("4 - about&help")
		print("5 - exit\n")

		command = input("Please select action (type the number of desired option): ")
		
		try:
			cmd_no = int(command)
		except:
			print("Incorrect selection.")
			continue

		perform(cmd_no)
