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
# System Imports
import os
import sys

# Local Imports
import GUI
import constants as CONSTS
import calculate

# Class declaration for the CLI
## __ = private


class CLI:
    # Function called on creation of the class
    def __init__(self):
        # Create inital global vars
        self.__fIncome = 0
        self.__strIncrement = CONSTS.C_INCREMENT_ANNUALLY

        self.__dictOptions = {
            "bHECS": False,
            "bNTFT": False,
            "bSuper": False,
            "iFY": "2020-2021"
        }
        self.__bAllItemsSet = False
        self.__iHours = 40

    def cliMenu(self):
        while(True):
            self.__clearScreen()
            self.__checkValid()
            print("Pay Calculator V{}".format(CONSTS.C_VERSION))
            print("1) Set Income (${})".format(self.__fIncome))
            print("2) Set Pay Increment ({})".format(self.__strIncrement) if not self.__strIncrement ==
                  "Hourly" else "2) Set Pay Increment ({} ({} Hours))".format(self.__strIncrement, self.__iHours))
            print("3) Set Tax Options (HECS/HELP: {}, No Tax Free Threshold: {}, Include Superannuation: {}, FY{})".format(
                self.__dictOptions.get("bHECS"), self.__dictOptions.get("bNTFT"), self.__dictOptions.get("bSuper"), self.__dictOptions.get("iFY")))
            if self.__bAllItemsSet:
                print("4) Calculate")
                iIncrement = 5
            else:
                iIncrement = 4
            print("{}) Exit".format(str(iIncrement)))
            strSelection = "0"
            while(not self.__verifyMenuInput(strSelection)):
                strSelection = input("Enter Selection: ")

    def __verifyMenuInput(self, strSelection) -> bool:
        try:
            if(strSelection == "GUI"):
                # This is only for debugging, this is unstable when opened multiple times (MAC)
                GUI.start()
            iStrSelection = int(strSelection)

        except:
            # NON INT Entered
            return False

        # Checks menuInput and calls menus
        if(iStrSelection == 0):
            return False
        elif(iStrSelection == 1):
            self.__setIncomeMenu()
            return True
        elif(iStrSelection == 2):
            self.__setPayIncrementMenu()
            return True
        elif(iStrSelection == 3):
            self.__setTaxOptionsMenu()
            return True
        elif(iStrSelection == 4 and self.__bAllItemsSet):
            self.__cliCalc()
            return True
        elif((iStrSelection == 4 and not self.__bAllItemsSet) or iStrSelection == 5):
            sys.exit(0)
        else:
            return False

    def __setIncomeMenu(self):
        self.__clearScreen()
        bIntValid = False
        while(not bIntValid):
            strTempIncome = input("Enter Income for Time Period (${} {}): ".format(
                self.__fIncome, self.__strIncrement))
            try:
                fTemp = float(strTempIncome)
                if(fTemp <= 0):
                    raise Exception("Value must be positive")
                else:
                    self.__fIncome = fTemp
                    bIntValid = True
            except:
                print("Input Not Valid")

    # Shows the Pay Increment menu
    def __setPayIncrementMenu(self):
        self.__clearScreen()
        strInput = "0"
        print("Select Pay Increment")
        print("1) Hourly ({})".format(self.__iHours))
        print("2) Daily")
        print("3) Weekly")
        print("4) Fortnightly")
        print("5) Monthly")
        print("6) Annually")
        # Verifies Input
        while(not self.__verifyPayInput(strInput)):
            strInput = input(
                "Enter Increment ({}): ".format(self.__strIncrement))

    # Verify the pay increment Input
    def __verifyPayInput(self, strInput):
        try:
            iInput = int(strInput)
            if(iInput <= 0 or iInput > 6):
                raise Exception("Value is Incorrect")
            else:
                # WHY NO SWITCH CASE PYTHON!!!
                if(iInput == 1):
                    self.__strIncrement = CONSTS.C_INCREMENT_HOURLY
                    self.__verifyHours()
                elif(iInput == 2):
                    self.__strIncrement = CONSTS.C_INCREMENT_DAILY
                elif(iInput == 3):
                    self.__strIncrement = CONSTS.C_INCREMENT_WEEKLY
                elif(iInput == 4):
                    self.__strIncrement = CONSTS.C_INCREMENT_FORTNIGHTLY
                elif(iInput == 5):
                    self.__strIncrement = CONSTS.C_INCREMENT_MONTHLY
                elif(iInput == 6):
                    self.__strIncrement = CONSTS.C_INCREMENT_ANNUALLY
                # Return true after valid input exiting loop
                return True
        except:
            print("Invalid Entry")
            return False

    # Verify inputted hours

    def __verifyHours(self):
        while(True):
            strInput = input("Enter Hours worked ({}): ".format(self.__iHours))
            try:
                if(strInput == ""):  # Enter Follows with using current values
                    break
                iInput = int(strInput)
                if(iInput < 0):
                    raise Exception("Invalid Hours")
                else:
                    self.__iHours = iInput
                    break
            except:
                print("Invalid Hours Entered!!")

    # Menu for setting tax options
    def __setTaxOptionsMenu(self):
        while(True):
            self.__clearScreen()
            print("Enter an input to toggle a tax option")
            print("1) HECS/HELP ({})".format(self.__dictOptions.get("bHECS")))
            print("2) No Tax Free Threshold ({})".format(
                self.__dictOptions.get("bNTFT")))
            print("3) Salary Include Superannuation ({})".format(
                self.__dictOptions.get("bSuper")))
            print("4) Set Finincal Year ({})".format(
                self.__dictOptions.get("iFY")))
            print("5) Back to Menu")
            strInput = input("Enter Selection: ")
            # Verify Input
            try:
                iInput = int(strInput)
                if(iInput < 0 or iInput > 5):
                    raise Exception("Invalid Number")
                else:
                    if iInput == 5:
                        break
                    elif iInput == 1:
                        self.__dictOptions.update(
                            {"bHECS": not self.__dictOptions.get("bHECS")})
                    elif iInput == 2:
                        self.__dictOptions.update(
                            {"bNTFT": not self.__dictOptions.get("bNTFT")})
                    elif iInput == 3:
                        self.__dictOptions.update(
                            {"bSuper": not self.__dictOptions.get("bSuper")})
                    elif iInput == 4:
                        iFY = self.__getFYYearMenu()
                        self.__dictOptions.update({
                            "iFY": iFY
                        })
            except:
                print("Invalid Input!!")

    def __getFYYearMenu(self) -> int:
        while(True):
            # Get FY year from CONSTS
            i = 1
            print("Select Year")
            # Loop showing each entry in tuple
            for year in CONSTS.C_FY:
                print("{}) FY{}".format(i, year))
                i += 1
            strInput = input("Enter Selection: ")
            # Verify Selection
            try:
                iInput = int(strInput)
                if (iInput <= 0):
                    raise Exception("Value < 0")
                elif (iInput > len(CONSTS.C_FY)):
                    raise Exception("Input higher than tuple")
                else:
                    # Convert starting from 1 to 0.
                    return CONSTS.C_FY[iInput - 1]
            #
            except:
                print("Invalid Input!!")

    # Class that calls all the calculations
    def __cliCalc(self):
        calcClass = calculate.taxCalculations(
            self.__fIncome, self.__strIncrement, self.__dictOptions, self.__iHours)
        self.dictCalcResult, self.__iHours = calcClass.calculate()
        self.rows = calcClass.calculateIncrementVaribles(
            self.dictCalcResult, self.__iHours)
        self.__displayResponse()

    # Displays the results as a table
    def __displayResponse(self):
        self.__clearScreen()
        print("Results: ")
        # Creates TABLE
        tempRow = self.rows[0]
        format_titlerow = "{:>15}" * len(tempRow)
        format_row = "{:>15}" + ("{:>15.2f}" * (len(tempRow) - 1))
        print(format_titlerow.format(*tempRow))
        # for each increment display the details
        for increment in self.rows:
            strIncrement = increment["Increment"]
            fTaxableIncome = increment["taxableIncome"]
            fNetIncome = increment["netIncome"]
            fSuper = increment["super"]
            fMedicareLevy = increment["medicareLevy"]
            fIncomeTax = increment["tax"]
            fHecsOwed = increment["hecsOwed"]
            fTotalTax = increment["totalTax"]
            tupleValues = (strIncrement, fTaxableIncome, fSuper, fIncomeTax,
                           fMedicareLevy,  fHecsOwed, fTotalTax, fNetIncome)
            print(format_row.format(*tupleValues))
        input("Press Enter to return")

    # Clears the screen
    def __clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Checks if valid to calculate
    def __checkValid(self):
        if self.__fIncome > 0:
            self.__bAllItemsSet = True
