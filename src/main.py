import os

from src.app import App

def get_user_input():
    print("Notice:\n- Please be sure that all the input files are placed in the <test> directory of this program.\n- The input file must be of the form <file_name>.txt")
    while True:
        user_input = input("Enter the file name:\n")
        if not os.path.exists("test/" + user_input):
            print("Invalid directory. Please try again.")
        elif not user_input.endswith(".txt"):
            print("Invalid file type. Please try again.")
        else:
            file_name = "test/" + user_input
            return file_name
def main():
    # Get user input for a file directory
    file_name = get_user_input()
    
    app = App(file_name)
    app.on_execute()

if __name__ == "__main__":
    main()