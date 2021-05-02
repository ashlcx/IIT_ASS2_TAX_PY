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

Formatted in accordance with PEP-8 Using Black
"""
import json
import sys
import constants as CONSTS

# calculations Class Declaration
class taxCalculations:
    ## Called when class initalised
    def __init__(self, fIncome, strPayIncrement, dcitTaxOptions, iHours=40):
        # Get Tax Rates
        self.__fIncome = fIncome
        self.__payIncrement = strPayIncrement
        self.__taxOptions = dcitTaxOptions
        ## Fixes issues where hours and !hours is increment
        if strPayIncrement == CONSTS.C_INCREMENT_HOURLY:
            self.__iHours = iHours
        else:
            self.__iHours = 40
        ## Open taxrates as json object and converts to object
        try:
            with open(CONSTS.C_TAXFILE) as fileTaxRates:
                jsonData = json.load(fileTaxRates)
                # print("type: ", type(self. jsonData))
                strFY = dcitTaxOptions.get("iFY")
                self.taxRates = jsonData["t{}".format(strFY)]
        ## Exit on fatal exception
        except Exception as e:
            print(str(e))
            print(
                "FATAL EXCEPTION: Cannot grab {}; Now Exiting".format(CONSTS.C_TAXFILE)
            )
            sys.exit(1)  # sys.exit(1) Indicate non normal exit code

    ## Public method to calculate and return results
    def calculate(self) -> dict:
        self.__calcTaxableIncomeToAnnually()
        self.__calculateTax()

        self.__fMedicareLevy = self.__fTaxableIncome * CONSTS.C_MEDICARE_LEVY_RATE
        self.__fTotaltax = self.tax + self.__fMedicareLevy + self.__fHecsOwed
        self.__fNetIncome = self.__fTaxableIncome - self.__fTotaltax
        self.__totalPackage = self.__fTaxableIncome + self.__fSuper
        dictResponse = {
            "taxableIncome": self.__fTaxableIncome,
            "super": self.__fSuper,
            "tax": self.tax,
            "medicareLevy": self.__fMedicareLevy,
            "hecsOwed": self.__fHecsOwed,
            "totalTax": self.__fTotaltax,
            "netIncome": self.__fNetIncome,
        }
        return dictResponse, self.__iHours

    ## Calculates taxable income and ensures its in annual format
    def __calcTaxableIncomeToAnnually(self):
        # PYTHON WHY NO SWITCH!!!!>.>!>!>!>!>!>!>!>>!>!>!>!
        if self.__payIncrement == CONSTS.C_INCREMENT_HOURLY:
            self.__fTaxableIncome = self.__fIncome * self.__iHours * CONSTS.C_WEEKSPYEAR
        elif self.__payIncrement == CONSTS.C_INCREMENT_DAILY:
            self.__fTaxableIncome = self.__fIncome * 5 * CONSTS.C_WEEKSPYEAR
        elif self.__payIncrement == CONSTS.C_INCREMENT_WEEKLY:
            self.__fTaxableIncome = self.__fIncome * CONSTS.C_WEEKSPYEAR
        elif self.__payIncrement == CONSTS.C_INCREMENT_FORTNIGHTLY:
            self.__fTaxableIncome = self.__fIncome * CONSTS.C_WEEKSPYEAR / 2
        elif self.__payIncrement == CONSTS.C_INCREMENT_MONTHLY:
            self.__fTaxableIncome = self.__fIncome * 12
        else:
            self.__fTaxableIncome = self.__fIncome
       
        ## PROCESS SUPERANNUATION
        fSuperPercentage = 9.5 / 100

        ## If includes super extract super or just calculate it based off 9.5%
        if self.__taxOptions.get("bSuper"):
            self.__fSuper = (
                self.__fTaxableIncome / (1 + fSuperPercentage) * fSuperPercentage
            )
            self.__fTaxableIncome -= self.__fSuper
        else:
            self.__fSuper = self.__fTaxableIncome * fSuperPercentage

    ## Calculate Income Tax & HECS
    def __calculateTax(self):
        self.tax = 0  # Init tax value
        self.__fHecsOwed = 0

        ## Determine if using No Tax Free Threeshold rates or normal
        if self.__taxOptions.get("bNTFT"):
            taxTable = self.taxRates["NTFT"]
        else:
            taxTable = self.taxRates["normal"]
        hecsRates = self.taxRates["HECS"]
        ## Calculate HECS if required
        ## HECS is not tax deductable so dont modify taxable income
        if self.__taxOptions.get("bHECS"):
            for i in hecsRates:
                if self.__fTaxableIncome > hecsRates[i][0]:
                    self.__fHecsOwed = self.__fTaxableIncome * hecsRates[i][1]
                    break
        remainingTaxableIncome = self.__fTaxableIncome
        ## Loop to calculate tax
        for i in taxTable:
            # print(taxTable[i])
            if remainingTaxableIncome > taxTable[i][0]:
                tax = (remainingTaxableIncome - taxTable[i][0]) * taxTable[i][1]
                self.tax += tax
                remainingTaxableIncome = taxTable[i][0]

    ## Calculates all the divided values for an increment
    def calculateIncrementVaribles(self, INCAnnually, hours) -> tuple:
        # hourly
        INCHourly = {}
        INCHourly.update({"Increment": "Hourly ({})".format(hours)})
        INCHourly.update(
            {
                "taxableIncome": (
                    INCAnnually.get("taxableIncome") / CONSTS.C_WEEKSPYEAR / hours
                )
            }
        )
        INCHourly.update(
            {"super": (INCAnnually.get("super") / CONSTS.C_WEEKSPYEAR / hours)}
        )
        INCHourly.update({"tax": (INCAnnually.get("tax") / CONSTS.C_WEEKSPYEAR / hours)})
        INCHourly.update(
            {
                "medicareLevy": (
                    INCAnnually.get("medicareLevy") / CONSTS.C_WEEKSPYEAR / hours
                )
            }
        )
        INCHourly.update(
            {"hecsOwed": (INCAnnually.get("hecsOwed") / CONSTS.C_WEEKSPYEAR / hours)}
        )
        INCHourly.update(
            {"totalTax": (INCAnnually.get("totalTax") / CONSTS.C_WEEKSPYEAR / hours)}
        )
        INCHourly.update(
            {"netIncome": (INCAnnually.get("netIncome") / CONSTS.C_WEEKSPYEAR / hours)}
        )
        # Daily
        INCDaily = {}
        INCDaily.update({"Increment": "Daily"})
        INCDaily.update(
            {"taxableIncome": (INCAnnually.get("taxableIncome") / CONSTS.C_WEEKSPYEAR / 5)}
        )

        INCDaily.update({"super": (INCAnnually.get("super") / CONSTS.C_WEEKSPYEAR / 5)})
        INCDaily.update({"tax": (INCAnnually.get("tax") / CONSTS.C_WEEKSPYEAR / 5)})
        INCDaily.update(
            {"medicareLevy": (INCAnnually.get("medicareLevy") / CONSTS.C_WEEKSPYEAR / 5)}
        )

        INCDaily.update(
            {"hecsOwed": (INCAnnually.get("hecsOwed") / CONSTS.C_WEEKSPYEAR / 5)}
        )
        INCDaily.update(
            {"totalTax": (INCAnnually.get("totalTax") / CONSTS.C_WEEKSPYEAR / 5)}
        )
        INCDaily.update(
            {"netIncome": (INCAnnually.get("netIncome") / CONSTS.C_WEEKSPYEAR / 5)}
        )
        # Weekly
        INCWeekly = {}
        INCWeekly.update({"Increment": "Weekly"})
        INCWeekly.update(
            {"taxableIncome": (INCAnnually.get("taxableIncome") / CONSTS.C_WEEKSPYEAR)}
        )

        INCWeekly.update({"super": (INCAnnually.get("super") / CONSTS.C_WEEKSPYEAR)})
        INCWeekly.update({"tax": (INCAnnually.get("tax") / CONSTS.C_WEEKSPYEAR)})
        INCWeekly.update(
            {"medicareLevy": (INCAnnually.get("medicareLevy") / CONSTS.C_WEEKSPYEAR)}
        )

        INCWeekly.update({"hecsOwed": (INCAnnually.get("hecsOwed") / CONSTS.C_WEEKSPYEAR)})
        INCWeekly.update({"totalTax": (INCAnnually.get("totalTax") / CONSTS.C_WEEKSPYEAR)})
        INCWeekly.update(
            {"netIncome": (INCAnnually.get("netIncome") / CONSTS.C_WEEKSPYEAR)}
        )
        # Fortnightly
        INCFornightly = {}
        INCFornightly.update({"Increment": "Fortnightly"})
        INCFornightly.update(
            {
                "taxableIncome": (
                    INCAnnually.get("taxableIncome") / (CONSTS.C_WEEKSPYEAR / 2)
                )
            }
        )

        INCFornightly.update(
            {"super": (INCAnnually.get("super") / (CONSTS.C_WEEKSPYEAR / 2))}
        )
        INCFornightly.update({"tax": (INCAnnually.get("tax") / (CONSTS.C_WEEKSPYEAR / 2))})
        INCFornightly.update(
            {"medicareLevy": (INCAnnually.get("medicareLevy") / (CONSTS.C_WEEKSPYEAR / 2))}
        )

        INCFornightly.update(
            {"hecsOwed": (INCAnnually.get("hecsOwed") / (CONSTS.C_WEEKSPYEAR / 2))}
        )
        INCFornightly.update(
            {"totalTax": (INCAnnually.get("totalTax") / (CONSTS.C_WEEKSPYEAR / 2))}
        )
        INCFornightly.update(
            {"netIncome": (INCAnnually.get("netIncome") / (CONSTS.C_WEEKSPYEAR / 2))}
        )
        # Monthly
        INCMonthly = {}
        INCMonthly.update({"Increment": "Monthly"})
        INCMonthly.update({"taxableIncome": (INCAnnually.get("taxableIncome") / 12)})

        INCMonthly.update({"super": (INCAnnually.get("super") / 12)})
        INCMonthly.update({"tax": (INCAnnually.get("tax") / 12)})
        INCMonthly.update({"medicareLevy": (INCAnnually.get("medicareLevy") / 12)})

        INCMonthly.update({"hecsOwed": (INCAnnually.get("hecsOwed") / 12)})
        INCMonthly.update({"totalTax": (INCAnnually.get("totalTax") / 12)})
        INCMonthly.update({"netIncome": (INCAnnually.get("netIncome") / 12)})

        INCAnnually.update({"Increment": "Annually"})
        tupleRows = (INCHourly, INCDaily, INCWeekly, INCFornightly, INCMonthly, INCAnnually)
        return tupleRows
