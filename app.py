"""
Copyright 2021 Ashley Hines

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
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
            cli = CLI.CLI()
            cli.cliMenu()
        else:
            print("Pay Calculator {}".format(C.C_VERSION))
            print(
                "Invalid Argument - Syntax should be 'python3 app.py cli' or 'python3 app.py'")
            sys.exit(1)
    else:
        GUI.start()
