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
import json
import sys
import constants as CONSTS

class taxCalculations:

    def __init__(self, income, payIncrement,taxOptions, hours=40):
        #Get Tax Rates
        self.income = income
        self.payIncrement = payIncrement
        self.taxOptions = taxOptions
        if(payIncrement == CONSTS.C_INCREMENT_HOURLY):
            self.hours = hours
        else:
            self.hours = 40
        try:
            with open(CONSTS.C_TAXFILE) as fileTaxRates:
                jsonData = json.load(fileTaxRates)
                #print("type: ", type(self. jsonData))
                iFY = taxOptions.get("iFY")
                self.taxRates = jsonData["t{}".format(iFY)]
        except Exception as e:
            print(str(e))
            print("FATAL EXCEPTION: Cannot grab {}; Now Exiting".format(CONSTS.C_TAXFILE))
            sys.exit(1) # sys.exit(1) Indicate non normal exit code


    def calculate(self) -> dict:
        
        self.__calcTaxableIncomeToAnnually()
        self.__calculateTax()
        self.medicareLevy = self.taxableIncome * CONSTS.C_MEDICARE_LEVY_RATE
        self.totaltax = self.tax + self.medicareLevy + self.hecsOwed
        self.netIncome = self.taxableIncome - self.totaltax
        self.totalPackage = self.taxableIncome + self.fSuper
        dictResponse = {
            "taxableIncome": self.taxableIncome,
            "super": self.fSuper,
            "tax": self.tax,
            "medicareLevy": self.medicareLevy,
            "hecsOwed": self.hecsOwed,
            "totalTax": self.totaltax,
            "netIncome": self.netIncome,
        }
        return dictResponse, self.hours
    
    def __calcTaxableIncomeToAnnually(self):
        
        # PYTHON WHY NO SWITCH!!!!>.>!>!>!>!>!>!>!>>!>!>!>!
        if(self.payIncrement == CONSTS.C_INCREMENT_HOURLY):
            self.taxableIncome = self.income * self.hours * CONSTS.C_WEEKSPYEAR
        elif(self.payIncrement == CONSTS.C_INCREMENT_DAILY):
            self.taxableIncome = self.income * 5 * CONSTS.C_WEEKSPYEAR
        elif(self.payIncrement == CONSTS.C_INCREMENT_WEEKLY):
            self.taxableIncome = self.income * CONSTS.C_WEEKSPYEAR
        elif(self.payIncrement == CONSTS.C_INCREMENT_FORTNIGHTLY):
            self.taxableIncome = self.income * CONSTS.C_WEEKSPYEAR / 2
        elif(self.payIncrement == CONSTS.C_INCREMENT_MONTHLY):
            self.taxableIncome = self.income * 12 
        else:
            self.taxableIncome = self.income
        #PROCESS SUPERANNUATION

        superPercentage = 9.5 / 100

        if(self.taxOptions.get("bSuper")):
            self.fSuper = (self.taxableIncome / (1 + superPercentage) * superPercentage)
            self.taxableIncome -= self.fSuper
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
                self.tax += tax
                remainingTaxableIncome = taxTable[i][0]
        #print(self.tax)

    def calculateIncrementVaribles(self, results, hours) -> tuple:

        #hourly
        INCHourly = {}
        INCHourly.update({"Increment": "Hourly ({})".format(hours)})
        INCHourly.update({"taxableIncome": (results.get("taxableIncome") / CONSTS.C_WEEKSPYEAR / hours)}) 
        INCHourly.update({"super": (results.get("super") / CONSTS.C_WEEKSPYEAR / hours)})
        INCHourly.update({"tax": (results.get("tax") / CONSTS.C_WEEKSPYEAR / hours)})
        INCHourly.update({"medicareLevy": (results.get("medicareLevy") / CONSTS.C_WEEKSPYEAR / hours)})
        INCHourly.update({"hecsOwed": (results.get("hecsOwed") / CONSTS.C_WEEKSPYEAR / hours)})
        INCHourly.update({"totalTax": (results.get("totalTax") / CONSTS.C_WEEKSPYEAR / hours)})
        INCHourly.update({"netIncome": (results.get("netIncome") / CONSTS.C_WEEKSPYEAR / hours)})
        #Daily
        INCDaily = {}
        INCDaily.update({"Increment": "Daily"})
        INCDaily.update({"taxableIncome": (results.get("taxableIncome") / CONSTS.C_WEEKSPYEAR / 5)})
        
        INCDaily.update({"super": (results.get("super") / CONSTS.C_WEEKSPYEAR / 5)})
        INCDaily.update({"tax": (results.get("tax") / CONSTS.C_WEEKSPYEAR / 5)})
        INCDaily.update({"medicareLevy": (results.get("medicareLevy") / CONSTS.C_WEEKSPYEAR / 5)})
        
        INCDaily.update({"hecsOwed": (results.get("hecsOwed") / CONSTS.C_WEEKSPYEAR / 5)})
        INCDaily.update({"totalTax": (results.get("totalTax") / CONSTS.C_WEEKSPYEAR / 5)})
        INCDaily.update({"netIncome": (results.get("netIncome") / CONSTS.C_WEEKSPYEAR / 5)})
        #Weekly
        INCWeekly = {}
        INCWeekly.update({"Increment": "Weekly"})
        INCWeekly.update({"taxableIncome": (results.get("taxableIncome") / CONSTS.C_WEEKSPYEAR)})
        
        INCWeekly.update({"super": (results.get("super") / CONSTS.C_WEEKSPYEAR)})
        INCWeekly.update({"tax": (results.get("tax") / CONSTS.C_WEEKSPYEAR)})
        INCWeekly.update({"medicareLevy": (results.get("medicareLevy") / CONSTS.C_WEEKSPYEAR)})
        
        INCWeekly.update({"hecsOwed": (results.get("hecsOwed") / CONSTS.C_WEEKSPYEAR)})
        INCWeekly.update({"totalTax": (results.get("totalTax") / CONSTS.C_WEEKSPYEAR)})
        INCWeekly.update({"netIncome": (results.get("netIncome") / CONSTS.C_WEEKSPYEAR)})
        #Fortnightly
        INCFornightly = {}
        INCFornightly.update({"Increment": "Fortnightly"})
        INCFornightly.update({"taxableIncome": (results.get("taxableIncome") / (CONSTS.C_WEEKSPYEAR /2 ))})
        
        INCFornightly.update({"super": (results.get("super") / (CONSTS.C_WEEKSPYEAR /2 ))})
        INCFornightly.update({"tax": (results.get("tax") / (CONSTS.C_WEEKSPYEAR /2 ))})
        INCFornightly.update({"medicareLevy": (results.get("medicareLevy") / (CONSTS.C_WEEKSPYEAR /2 ))})
        
        INCFornightly.update({"hecsOwed": (results.get("hecsOwed") / (CONSTS.C_WEEKSPYEAR /2 ))})
        INCFornightly.update({"totalTax": (results.get("totalTax") / (CONSTS.C_WEEKSPYEAR /2 ))})
        INCFornightly.update({"netIncome": (results.get("netIncome") / (CONSTS.C_WEEKSPYEAR /2 ))})
        #Monthly
        INCMonthly = {}
        INCMonthly.update({"Increment": "Monthly"})
        INCMonthly.update({"taxableIncome": (results.get("taxableIncome") / 12)})
        
        INCMonthly.update({"super": (results.get("super") / 12)})
        INCMonthly.update({"tax": (results.get("tax") / 12)})
        INCMonthly.update({"medicareLevy": (results.get("medicareLevy") / 12)})
        
        INCMonthly.update({"hecsOwed": (results.get("hecsOwed") / 12)})
        INCMonthly.update({"totalTax": (results.get("totalTax") / 12)})
        INCMonthly.update({"netIncome": (results.get("netIncome") / 12)})

        results.update({"Increment": "Annually"})
        rows = (INCHourly, INCDaily ,INCWeekly ,INCFornightly,INCMonthly, results)
        return rows
