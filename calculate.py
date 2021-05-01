import json
import sys
import constants as C

class taxCalculations:

    def __init__(self, income, payIncrement,taxOptions, hours=40, cli=False):
        print("Calculating")
        #Get Tax Rates
        self.income = income
        self.payIncrement = payIncrement
        self.taxOptions = taxOptions
        self.hours = hours
        self.cli = cli
        try:
            with open(C.C_TAXFILE) as fileTaxRates:
                jsonData = json.load(fileTaxRates)
                #print("type: ", type(self. jsonData))
                iFY = taxOptions.get("iFY")
                self.taxRates = jsonData["t{}".format(iFY)]
                print(end="") #DEBUG PAUSE
        except:
            print("FATAL EXCEPTION: Cannot grab {}; Now Exiting".format(C.C_TAXFILE))
            sys.exit(1) # sys.exit(1) Indicate non normal exit code


    def calculate(self) -> object:
        
        self.__calcTaxableIncomeToAnnually()
        self.__calculateTax()
        self.medicareLevy = self.taxableIncome * C.C_MEDICARE_LEVY_RATE
        self.totaltax = self.tax + self.medicareLevy + self.hecsOwed
        self.grossIncome = self.taxableIncome - self.totaltax
        self.totalPackage = self.taxableIncome + self.fSuper
        dictResponse = {
            "taxableIncome": self.taxableIncome,
            "grossIncome": self.grossIncome,
            "super": self.fSuper,
            "medicareLevy": self.medicareLevy,
            "tax": self.tax,
            "hecsOwed": self.hecsOwed,
            "totalTax": self.totaltax,
        }
        return dictResponse
    
    def __calcTaxableIncomeToAnnually(self):
        
        # PYTHON WHY NO SWITCH!!!!>.>!>!>!>!>!>!>!>>!>!>!>!
        if(self.payIncrement == C.C_INCREMENT_HOURLY):
            self.taxableIncome = self.income * self.hours * C.C_WEEKSPYEAR
        elif(self.payIncrement == C.C_INCREMENT_DAILY):
            self.taxableIncome = self.income * 5 * C.C_WEEKSPYEAR
        elif(self.payIncrement == C.C_INCREMENT_WEEKLY):
            self.taxableIncome = self.income * C.C_WEEKSPYEAR
        elif(self.payIncrement == C.C_INCREMENT_FORTNIGHTLY):
            self.taxableIncome = self.income * C.C_WEEKSPYEAR / 2
        elif(self.payIncrement == C.C_INCREMENT_MONTHLY):
            self.taxableIncome = self.income * 12 #TODO #1 Incorporate Leave
        else:
            self.taxableIncome = self.income
        print(self.taxableIncome)
        #PROCESS SUPERANNUATION

        superPercentage = 9.5 / 100

        if(self.taxOptions.get("bSuper")):
            self.fSuper = (self.taxableIncome / (1 + superPercentage) * superPercentage)
            self.taxableIncome -= self.fSuper
            print(self.fSuper)
        else:
            self.fSuper = self.taxableIncome * superPercentage
        

    def __calculateTax(self):
        self.tax = 0 #Init tax value
        self.hecsOwed = 0
        if(self.taxOptions.get("bNTFT")):
            taxTable = self.taxRates["NTFT"]
        else:
            taxTable = self.taxRates["normal"]
        hecsRates = self.taxRates["HECS"]
        if(self.taxOptions.get("bHECS")):
            for i in hecsRates:
                if (self.taxableIncome > hecsRates[i][0]):
                    self.hecsOwed = self.taxableIncome * hecsRates[i][1]
                    break
        remainingTaxableIncome = self.taxableIncome
        for i in taxTable:
            #print(taxTable[i])
            if(remainingTaxableIncome > taxTable[i][0]):
                tax = (remainingTaxableIncome - taxTable[i][0]) * taxTable[i][1]
                print(tax)
                self.tax += tax
                remainingTaxableIncome = taxTable[i][0]
        #print(self.tax)
