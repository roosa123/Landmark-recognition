from data_downloader import download_data
from network import run_training, build_network
from classify import classify

def perform(action_no, model = None):
	if action_no == 1:
		download_data()
	elif action_no == 2:
		model = build_network()
		run_training(model)
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