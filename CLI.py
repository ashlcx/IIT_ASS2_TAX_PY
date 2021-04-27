# Imports
import constants
import sys
import os

class CLI:
    def __init__(self):
        
        self.iIncome = 0
        self.strIncrement = "Annually"
        self.bHECS = False
        self.bNTFT = False
        self.bSuper = False
        self.bAllItemsSet = False

        self.cliMenu()

    def cliMenu(self):
        print("Pay Calculator V{}".format(constants.C_VERSION))
        print("1) Set Income (${})".format(self.iIncome))
        print("2) Set Pay Increment ({})".format(self.strIncrement))
        print("3) Set Tax Options (HECS/HELP: {}, No Tax Free Threshold: {}, Include Superannuation: {})".format(
            self.bHECS, self.bNTFT, self.bSuper))
        if self.bAllItemsSet:
            print("4) Calculate")
            iIncrement = 5
        else:
            iIncrement = 4
        print("{}) Exit".format(str(iIncrement)))
        
        strSelection = "0"
        while(not self.verifyIntSelection(strSelection)):
            strSelection = input("Enter Selection: ")

    def verifyIntSelection(self, strSelection) -> bool:
        try:
            iStrSelection = int(strSelection)
        except:
            return False
        if(iStrSelection == 0):
            return False
        elif(iStrSelection == 1):
            #TODO SetIncome Menu
            print("SetIncomeMenu")
            return True
        elif(iStrSelection == 2):
            print("setPayIncrement")
            return True
        elif(iStrSelection == 3):
            print("SetTaxOptions")
            return True
        elif(iStrSelection == 4 and self.bAllItemsSet):
            print("Calculate")
            return True
        elif((iStrSelection == 4 and not self.bAllItemsSet) or iStrSelection == 5):
            sys.exit(0)
        else:
            return False
    
    def setIncomeMenu(self):
        cls
        print("Income")

    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')


"""
1) Set Income (Amount)
2) Set Pay Increment (Annually)
3) Set Tax Options (HECS/HELP: False, Tax Free Threshold: False, Include Superannuation: False)
4) Calculate
"""


    
