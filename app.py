import sys

import GUI
import CLI
import constants as C

if __name__ == "__main__":
    # Get System Args to check if GUI or CLI
    if (len(sys.argv) > 1):
        # print(sys.argv[1])
        # print(sys.argv[1].lower())
        if(sys.argv[1].lower() == "cli"):
            # Begin CLI
            Cli = CLI.CLI()
        else:
            print("Pay Calculator {}".format(C.C_VERSION))
            print(
                "Invalid Argument - Syntax should be 'python3 app.py cli' or 'python3 app.py'")
            sys.exit(1)
    else:
        # GUI Starts Here.
        GUI.guiMain()
        sys.exit(0)
