def show(option):
    help_file = ""

    if option == 1:
        help_file = "help\\data_download"
    elif option == 2:
        help_file = "help\\training"
    elif option == 3:
        help_file = "help\\classification"
    elif option == 4:
        print("Exiting help.")
        return
    else:
        print("There's no such option.")
        return

    with open(help_file) as f:
        print(f.read())

def show_help():
    with open("help\\about", "r") as f:
        print(f.read())

    sel_no = 0

    while sel_no != 4:
        print("\nContent:\n")
        print("1 - downloading data")
        print("2 - training the network")
        print("3 - testing the network")
        print("4 - exit help\n")
        selection = input("Type the number of the option, which you wish to know about or type 4 to exit: ")

        try:
            sel_no = int(selection)
        except:
            print("Incorrect selection.")
            continue

        show(sel_no)
    