# Imports
import os
import sys

import constants
import calculate


class CLI:
    def __init__(self):

        self.fIncome = 0
        self.strIncrement = "Annually"
        self.iIncrement = 6
        self.dictOptions = {
            "bHECS": False,
            "bNTFT": False,
            "bSuper": False,
            "iFY": 2021
        }
        self.bAllItemsSet = False
        self.iHours = 40

        self.cliMenu()

    def cliMenu(self):
        while(True):
            self.clearScreen()
            self.checkValid()
            print("Pay Calculator V{}".format(constants.C_VERSION))
            print("1) Set Income (${})".format(self.fIncome))
            print("2) Set Pay Increment ({})".format(self.strIncrement) if not self.strIncrement ==
                  "Hourly" else "2) Set Pay Increment ({} ({} Hours))".format(self.strIncrement, self.iHours))
            print("3) Set Tax Options (HECS/HELP: {}, No Tax Free Threshold: {}, Include Superannuation: {})".format(
                self.dictOptions.get("bHECS"), self.dictOptions.get("bNTFT"), self.dictOptions.get("bSuper")))
            if self.bAllItemsSet:
                print("4) Calculate")
                iIncrement = 5
            else:
                iIncrement = 4
            print("{}) Exit".format(str(iIncrement)))

            strSelection = "0"
            while(not self.verifyMenuInput(strSelection)):
                strSelection = input("Enter Selection: ")

    def verifyMenuInput(self, strSelection) -> bool:
        try:
            iStrSelection = int(strSelection)
        except:
            return False
        if(iStrSelection == 0):
            return False
        elif(iStrSelection == 1):
            # print("SetIncomeMenu")
            self.setIncomeMenu()
            return True
        elif(iStrSelection == 2):
            self.setPayIncrementMenu()
            return True
        elif(iStrSelection == 3):
            self.setTaxOptions()
            return True
        elif(iStrSelection == 4 and self.bAllItemsSet):
            self.cliCalc()
            return True
        elif((iStrSelection == 4 and not self.bAllItemsSet) or iStrSelection == 5):
            sys.exit(0)
        else:
            return False

    def setIncomeMenu(self):
        self.clearScreen()
        bIntValid = False
        while(not bIntValid):
            strTempIncome = input("Enter Income for Time Period (${} {}):".format(
                self.fIncome, self.strIncrement))
            try:
                fTemp = float(strTempIncome)
                if(fTemp <= 0):
                    raise Exception("Value must be positive")
                else:
                    self.fIncome = fTemp
                    bIntValid = True
            except:
                print("Input Not Valid")

    def setPayIncrementMenu(self):
        self.clearScreen()
        strInput = "0"
        print("Select Pay Increment")
        print("1) Hourly ({})".format(self.iHours))
        print("2) Daily")
        print("3) Weekly")
        print("4) Fortnightly")
        print("5) Monthly")
        print("6) Annually")
        while(not self.verifyPayInput(strInput)):
            strInput = input(
                "Enter Increment ({}): ".format(self.strIncrement))

    def verifyPayInput(self, strInput):
        try:
            iInput = int(strInput)
            if(iInput == 0):
                return False
            elif(iInput < 0 or iInput > 6):
                raise Exception("Value is Incorrect")
            else:
                # WHY NO SWITCH CASE PYTHON!!!
                self.iIncrement = iInput
                if(iInput == 1):
                    self.strIncrement = "Hourly"
                    self.iIncrement = 1
                    self.verifyHours()
                elif(iInput == 2):
                    self.strIncrement = "Daily"
                elif(iInput == 3):
                    self.strIncrement = "Weekly"
                elif(iInput == 4):
                    self.strIncrement = "Fortnightly"
                elif(iInput == 5):
                    self.strIncrement = "Monthly"
                elif(iInput == 6):
                    self.strIncrement = "Annually"
                return True
        except:
            print("Invalid Entry")
            return False

    def verifyHours(self):
        while(True):
            strInput = input("Enter Hours worked ({}): ".format(self.iHours))
            try:
                iInput = int(strInput)
                if(iInput <= 0):
                    raise Exception("Invalid Hours")
                else:
                    self.iHours = iInput
                    break
            except:
                print("Invalid Hours Entered!!")

    def setTaxOptions(self):

        bContinue = True
        while(bContinue):
            self.clearScreen()
            print("Enter an input to toggle a tax option")
            print("1) HECS/HELP ({})".format(self.dictOptions.get("bHECS")))
            print("2) No Tax Free Threshold ({})".format(
                self.dictOptions.get("bNTFT")))
            print("3) Salary Include Superannuation ({})".format(
                self.dictOptions.get("bSuper")))
            print("4) Set Finincal Year (2020/2021)")
            print("5) Back to Menu")
            strInput = input("Enter Selection: ")
            try:
                iInput = int(strInput)
                if(iInput < 0 or iInput > 5):
                    raise Exception("Invalid Number")
                else:
                    if iInput == 5:
                        bContinue = False
                        break
                    elif iInput == 1:
                        self.dictOptions.update(
                            {"bHECS": not self.dictOptions.get("bHECS")})
                    elif iInput == 2:
                        self.dictOptions.update(
                            {"bNTFT": not self.dictOptions.get("bNTFT")})
                    elif iInput == 3:
                        self.dictOptions.update(
                            {"bSuper": not self.dictOptions.get("bSuper")})
                    elif iInput == 4:
                        self.dictOptions.update({
                            "iFY": 2021
                        })
                        #TODO Set Year
            except:
                print("Invalid Input!!")

    def cliCalc(self):
        calc = calculate.taxCalculations(self.fIncome, self.strIncrement, self.dictOptions, cli=True)

    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def checkValid(self):
        if self.fIncome > 0:
            self.bAllItemsSet = True


"""
1) Set Income (Amount)
2) Set Pay Increment (Annually)
3) Set Tax Options (HECS/HELP: False, Tax Free Threshold: False, Include Superannuation: False)
4) Calculate
"""
