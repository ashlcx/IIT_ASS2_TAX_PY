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
import constants as CONSTS
import calculate
import tkinter as tk
from tkinter import ttk
import sys

# Class Declaration
class GUI:
    def __init__(self):
        ## Creates the main window and call the layout initalisers
        self.mainWindow = tk.Tk()
        self.mainWindow.title("Pay Calculator")
        self.mainWindow.config(bg="#FFFFFF") # Set background as white to match Mac
        self.__createMenuBar()
        self.__initLayout()

    ## creates the menu bar
    def __createMenuBar(self):
        ## creates the menu bar object
        self.__menuBar = tk.Menu(self.mainWindow)
        ## Creates the "File" Menu
        fileMenu = tk.Menu(self.__menuBar, tearoff=0)
        fileMenu.add_command(label="Exit", command=self.__kill)
        self.__menuBar.add_cascade(label="File", menu=fileMenu)
        ## creates the "About" Menu
        aboutMenu = tk.Menu(self.__menuBar, tearoff=0)
        aboutMenu.add_command(label="License", command=self.__popupLicense)
        aboutMenu.add_separator()
        aboutMenu.add_command(label="About SSL Manager", command=self.__popupAbout)
        self.__menuBar.add_cascade(label="About", menu=aboutMenu)
        # Sets the menubar
        self.mainWindow.config(menu=self.__menuBar)

    ## Kills the main window
    def __kill(self):
        self.mainWindow.destroy()

    ## calls create popup showing the about details
    def __popupAbout(self):
        self.__createPopup(
            "About", "PayCalculator V{}\nAuthor: Ash Hines".format(CONSTS.C_VERSION)
        )

    ## calls create popup showing the license details
    def __popupLicense(self):
        self.__createPopup(
            "License",
            (
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
            ),
        )

    ## Initializes the layout
    def __initLayout(self):
        self.__tabControl = ttk.Notebook(self.mainWindow)
        self.__createPayDetailsTab()
        self.__createResultsTab()
        if CONSTS.C_DEBUG:
            self.__debugTab = ttk.Frame(self.__tabControl)
            ttk.Button(self.__debugTab, text="BREAK", command=self.__breakpoint).pack()
            self.__tabControl.add(self.__debugTab, text="DEBUG")
        self.__tabControl.pack(expand=1, fill="both")

    ## Creates the paydetails Tab
    def __createPayDetailsTab(self):
        ## Declare Variables
        self.__valuesTab = ttk.Frame(self.__tabControl)
        self.__bSuper = tk.BooleanVar(self.__valuesTab)
        self.__bNTFT = tk.BooleanVar(self.__valuesTab)
        self.__bHECS = tk.BooleanVar(self.__valuesTab)
        self.__fIncome = tk.StringVar(self.__valuesTab)
        self.__iHours = tk.StringVar(self.__valuesTab)
        self.__iHours.set("40")
        self.__strIncrement = tk.StringVar(self.__valuesTab)
        self.__strIncrement.set(CONSTS.C_INCREMENT_ANNUALLY)
        self.__strIncrement.trace("w", self.__optionChange)
        self.__strFY = tk.StringVar(self.__valuesTab)

        ##Create Labels
        ttk.Label(self.__valuesTab, text="Enter Pay Details Below").grid(
            column=0, row=0, columnspan=3
        )
        ttk.Label(self.__valuesTab, text="Income $").grid(sticky="E", column=0, row=1)
        ttk.Label(self.__valuesTab, text="Pay Increment").grid(
            sticky="E", column=0, row=2
        )
        self.__labelHour = ttk.Label(self.__valuesTab, text="Hours")
        ttk.Label(self.__valuesTab, text="Finincal Year").grid(
            sticky="E", column=0, row=4
        )

        ## Creates Entries
        ttk.Entry(self.__valuesTab, textvariable=self.__fIncome).grid(column=1, row=1)
        self.__entryHours = ttk.Entry(self.__valuesTab, textvariable=self.__iHours)
        self.__entryHours.config(state="disabled")

        ## Creates optionMenus
        ttk.OptionMenu(
            self.__valuesTab, self.__strIncrement, *CONSTS.C_INCREMENT_CHOICES
        ).grid(column=1, row=2, sticky="N" + "S" + "E" + "W")
        ttk.OptionMenu(
            self.__valuesTab, self.__strFY, CONSTS.C_FY[0], *CONSTS.C_FY
        ).grid(column=1, row=4, sticky="N" + "S" + "E" + "W")

        ## Creates checkButtons
        ttk.Checkbutton(
            self.__valuesTab, text="No Tax Free Threshold", variable=self.__bNTFT
        ).grid(sticky="W", column=2, row=1)
        ttk.Checkbutton(
            self.__valuesTab, text="HECS/HELP Debt", variable=self.__bHECS
        ).grid(sticky="W", column=2, row=2)
        ttk.Checkbutton(
            self.__valuesTab, text="Includes SuperAnnuation", variable=self.__bSuper
        ).grid(sticky="W", column=2, row=3)
        ## Create Calculate button
        ttk.Button(
            self.__valuesTab, text="Calculate", command=self.__calculateResults
        ).grid(column=0, row=5, columnspan=3, sticky="N" + "S" + "E" + "W")

        ## Adds the tab to the notebook
        self.__tabControl.add(self.__valuesTab, text="Pay Details")

    ## Creates the resultsTab
    def __createResultsTab(self):
        # print("CreatingResults")
        self.__resultsTab = ttk.Frame(self.__tabControl)
        # ttk.Label(self.__resultsTab, text="Increment").grid(column=0, row=0)
        ## Creates the labels for the top row
        ttk.Label(self.__resultsTab, text="Taxable Income").grid(
            sticky="W", column=1, row=0, padx=10
        )
        ttk.Label(self.__resultsTab, text="Superannuation").grid(
            sticky="W", column=2, row=0, padx=10
        )
        ttk.Label(self.__resultsTab, text="Income Tax").grid(
            sticky="W", column=3, row=0, padx=10
        )
        ttk.Label(self.__resultsTab, text="Medicare Levy").grid(
            sticky="W", column=4, row=0, padx=10
        )
        ttk.Label(self.__resultsTab, text="Hecs Payable").grid(
            sticky="W", column=5, row=0, padx=10
        )
        ttk.Label(self.__resultsTab, text="Total Tax").grid(
            sticky="W", column=6, row=0, padx=10
        )
        ttk.Label(self.__resultsTab, text="Net Income").grid(
            sticky="W", column=7, row=0, padx=10
        )
        # rows = self.calc.calculateIncrementVaribles(self.dictCalcResult, self.hours.get())

    ## Creates a table and fills all the details into the rows
    def __createAndFillResultsTable(self):
        tupleRows = self.__calculations.calculateIncrementVaribles(
            self.__dictCalcResult, int(self.__iHours.get())
        )
        i = 1
        for row in tupleRows:
            # (row) Adds all the labels for an indivual row
            ttk.Label(self.__resultsTab, text="{}".format(row["Increment"])).grid(
                sticky="W", column=0, row=i, padx=10
            )
            ttk.Label(
                self.__resultsTab, text="${:.2f}".format(row["taxableIncome"])
            ).grid(sticky="W", column=1, row=i)
            ttk.Label(self.__resultsTab, text="${:.2f}".format(row["super"])).grid(
                sticky="W", column=2, row=i
            )
            ttk.Label(self.__resultsTab, text="${:.2f}".format(row["tax"])).grid(
                sticky="W", column=3, row=i
            )
            ttk.Label(
                self.__resultsTab, text="${:.2f}".format(row["medicareLevy"])
            ).grid(sticky="W", column=4, row=i)
            ttk.Label(self.__resultsTab, text="${:.2f}".format(row["hecsOwed"])).grid(
                sticky="W", column=5, row=i
            )
            ttk.Label(self.__resultsTab, text="${:.2f}".format(row["totalTax"])).grid(
                sticky="W", column=6, row=i
            )
            ttk.Label(self.__resultsTab, text="${:.2f}".format(row["netIncome"])).grid(
                sticky="W", column=7, row=i
            )
            ## Required to increment row
            i += 1

    ## On calculate this shows the results tab
    def __showResultsTab(self):
        self.__createAndFillResultsTable()
        self.__tabControl.add(self.__resultsTab, text="Results")
        # self.__tabControl.c

    ## When the Increment optionMenu is changed this checks if strIncrement == Hours
    def __optionChange(self, *args):
        # print("OPTION CHANGED")
        if self.__strIncrement.get() == CONSTS.C_INCREMENT_HOURLY:
            self.__labelHour.grid(sticky="E", column=0, row=3)
            self.__entryHours.grid(column=1, row=3)
            self.__entryHours.config(state="enabled")
        else:
            self.__entryHours.config(state="disabled")
            self.__labelHour.grid_forget()
            self.__entryHours.grid_forget()

    ## Calls calcualate results and adds to self. Raises exception on bad entries
    def __calculateResults(self):
        dictTaxOptions = {
            "bHECS": self.__bHECS.get(),
            "bSuper": self.__bSuper.get(),
            "bNTFT": self.__bNTFT.get(),
            "iFY": self.__strFY.get(),
        }
        ## Verify Information
        try:
            fIncome = float(self.__fIncome.get())
            if fIncome < 0:
                self.__createPopup("Error", "Income must be positive")
                raise Exception("Income must be positive")
            self.__calculations = calculate.taxCalculations(
                fIncome,
                self.__strIncrement.get(),
                dictTaxOptions,
                iHours=int(self.__iHours.get()) if not self.__iHours.get() == "" else 40,
            )
            self.__dictCalcResult, hours = self.__calculations.calculate()
            self.__iHours.set(str(hours))
            self.__showResultsTab()
            self.__tabControl.select(len(self.__tabControl.tabs()) - 1)
        except Exception as e:
            ## Displays error info into terminal
            print(str(e))
            self.__createPopup("Error", "Invalid Input", "200x75")

    ## For debugging
    def __breakpoint(self):
        # PUT A BREAK POINT HERE FOR A BUTTON TO CAUSE A BREAK
        pass

    ## Creates a poppup message
    def __createPopup(self, title, msg, size="auto"):
        popupWindow = tk.Tk()
        if size == "auto":
            pass
        else:
            popupWindow.geometry(size)
        popupWindow.wm_title(title)
        labelMSG = tk.Label(popupWindow, text=msg)
        labelMSG.pack(side="top", fill="x", pady=10)
        buttonOKAY = tk.Button(popupWindow, text="Okay", command=popupWindow.destroy)
        buttonOKAY.pack()
        popupWindow.mainloop()


def start():
    # GUI Starts Here.
    gui = GUI()
    gui.mainWindow.mainloop()
    sys.exit(0)
