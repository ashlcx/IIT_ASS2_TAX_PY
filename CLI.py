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
# Imports
import os
import sys

import GUI

import constants as CONSTS
import calculate

class CLI:
    def __init__(self):

        self.fIncome = 0
        self.strIncrement = CONSTS.C_INCREMENT_ANNUALLY
        self.iIncrement = 6
        self.dictOptions = {
            "bHECS": False,
            "bNTFT": False,
            "bSuper": False,
            "iFY": "2020-2021"
        }
        self.bAllItemsSet = False
        self.iHours = 40

    def cliMenu(self):
        while(True):
            self.__clearScreen()
            self.__checkValid()
            print("Pay Calculator V{}".format(CONSTS.C_VERSION))
            print("1) Set Income (${})".format(self.fIncome))
            print("2) Set Pay Increment ({})".format(self.strIncrement) if not self.strIncrement ==
                  "Hourly" else "2) Set Pay Increment ({} ({} Hours))".format(self.strIncrement, self.iHours))
            print("3) Set Tax Options (HECS/HELP: {}, No Tax Free Threshold: {}, Include Superannuation: {}, FY{})".format(
                self.dictOptions.get("bHECS"), self.dictOptions.get("bNTFT"), self.dictOptions.get("bSuper"), self.dictOptions.get("iFY")))
            if self.bAllItemsSet:
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
                # This is only for debugging, this is unstable
                GUI.start()
            iStrSelection = int(strSelection)
            
        except:
            return False
        if(iStrSelection == 0):
            return False
        elif(iStrSelection == 1):
            # print("SetIncomeMenu")
            self.__setIncomeMenu()
            return True
        elif(iStrSelection == 2):
            self.__setPayIncrementMenu()
            return True
        elif(iStrSelection == 3):
            self.__setTaxOptions()
            return True
        elif(iStrSelection == 4 and self.bAllItemsSet):
            self.__cliCalc()
            return True
        elif((iStrSelection == 4 and not self.bAllItemsSet) or iStrSelection == 5):
            sys.exit(0)
        else:
            return False

    def __setIncomeMenu(self):
        self.__clearScreen()
        bIntValid = False
        while(not bIntValid):
            strTempIncome = input("Enter Income for Time Period (${} {}): ".format(
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

    def __setPayIncrementMenu(self):
        self.__clearScreen()
        strInput = "0"
        print("Select Pay Increment")
        print("1) Hourly ({})".format(self.iHours))
        print("2) Daily")
        print("3) Weekly")
        print("4) Fortnightly")
        print("5) Monthly")
        print("6) Annually")
        while(not self.__verifyPayInput(strInput)):
            strInput = input(
                "Enter Increment ({}): ".format(self.strIncrement))

    def __verifyPayInput(self, strInput):
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
                    self.strIncrement = CONSTS.C_INCREMENT_HOURLY
                    self.iIncrement = 1
                    self.__verifyHours()
                elif(iInput == 2):
                    self.strIncrement = CONSTS.C_INCREMENT_DAILY
                elif(iInput == 3):
                    self.strIncrement = CONSTS.C_INCREMENT_WEEKLY
                elif(iInput == 4):
                    self.strIncrement = CONSTS.C_INCREMENT_FORTNIGHTLY
                elif(iInput == 5):
                    self.strIncrement = CONSTS.C_INCREMENT_MONTHLY
                elif(iInput == 6):
                    self.strIncrement = CONSTS.C_INCREMENT_ANNUALLY
                return True
        except:
            print("Invalid Entry")
            return False

    def __verifyHours(self):
        while(True):
            strInput = input("Enter Hours worked ({}): ".format(self.iHours))
            try:
                if(strInput == ""): #Enter Follows with using current values
                    break
                iInput = int(strInput)
                if(iInput < 0):
                    raise Exception("Invalid Hours")
                else:
                    self.iHours = iInput
                    break
            except:
                print("Invalid Hours Entered!!")

    def __setTaxOptions(self):

        bContinue = True
        while(bContinue):
            self.__clearScreen()
            print("Enter an input to toggle a tax option")
            print("1) HECS/HELP ({})".format(self.dictOptions.get("bHECS")))
            print("2) No Tax Free Threshold ({})".format(
                self.dictOptions.get("bNTFT")))
            print("3) Salary Include Superannuation ({})".format(
                self.dictOptions.get("bSuper")))
            print("4) Set Finincal Year ({})".format(self.dictOptions.get("iFY")))
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
                        iFY = self.__getFYYear()
                        self.dictOptions.update({
                            "iFY": iFY
                        })
                        #print(self.dictOptions.get("iFY"))
            except:
                print("Invalid Input!!")

    def __getFYYear(self) -> int:
        while(True):
            #Get FY year from CONSTS
            i = 1
            print("Select Year")
            for year in CONSTS.C_FY:
                print("{}) FY{}".format(i, year))
                i+=1
            strInput = input("Enter Selection: ")
            try:
                iInput = int(strInput)
                if (iInput <= 0):
                    raise Exception("Value < 0")
                elif (iInput > len(CONSTS.C_FY)):
                    raise Exception("Input higher than tuple")
                else:
                    return CONSTS.C_FY[iInput - 1] # Convert starting from 1 to 0.
            #
            except:
                print("Invalid Input!!")
    def __cliCalc(self):
        calcClass = calculate.taxCalculations(self.fIncome, self.strIncrement, self.dictOptions, self.iHours)
        self.dictCalcResult, self.iHours = calcClass.calculate()
        self.rows = calcClass.calculateIncrementVaribles(self.dictCalcResult, self.iHours)
        self.__displayResponse()

    
    def __displayResponse(self):
        self.__clearScreen()
        print("Results: ")
        """ print(self.INCHourly)
        print(self.INCDaily)
        print(self.INCWeekly)
        print(self.INCFornightly)
        print(self.INCMonthly)
        print(self.dictCalcResult) """
        #TABLE
        tempRow = self.rows[0]
        format_titlerow = "{:>15}" * len(tempRow)
        format_row = "{:>15}" + ("{:>15.2f}" * (len(tempRow) -1))
        print(format_titlerow.format(*tempRow))
        for increment in self.rows:
            finc = increment["Increment"]
            ftaxableIncome = increment["taxableIncome"]
            fnetIncome = increment["netIncome"]
            fsuper = increment["super"]
            fmedicareLevy = increment["medicareLevy"]
            ftax = increment["tax"]
            fhecsOwed = increment["hecsOwed"]
            ftotalTax = increment["totalTax"]
            values = (finc, ftaxableIncome, fsuper, ftax, fmedicareLevy,  fhecsOwed, ftotalTax,fnetIncome)
            print(format_row.format(*values))
        input("Press Enter to return")

        
    def __clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def __checkValid(self):
        if self.fIncome > 0:
            self.bAllItemsSet = True


"""
1) Set Income (Amount)
2) Set Pay Increment (Annually)
3) Set Tax Options (HECS/HELP: False, Tax Free Threshold: False, Include Superannuation: False)
4) Calculate
"""
