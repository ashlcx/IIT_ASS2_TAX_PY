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
import constants as CONSTS
import calculate
import tkinter as tk
from tkinter import ttk
import sys


class GUI:
    def __init__(self):
        #print("Starting GUI")
        self.root = tk.Tk()
        # self.root.geometry("800x600")
        self.root.title("Pay Calculator")
        self.__createMenuBar()
        self.__initLayout()

    def __createMenuBar(self):
        self.__menuBar = tk.Menu(self.root)
        fileMenu = tk.Menu(self.__menuBar, tearoff=0)
        fileMenu.add_command(label="Exit", command=self.__kill)
        self.__menuBar.add_cascade(label="File", menu=fileMenu)
        aboutMenu = tk.Menu(self.__menuBar, tearoff=0)
        aboutMenu.add_command(label="License", command=self.__popupLicense)
        aboutMenu.add_separator()
        aboutMenu.add_command(label="About SSL Manager",
                              command=self.__popupAbout)
        self.__menuBar.add_cascade(label="About", menu=aboutMenu)
        self.root.config(menu=self.__menuBar)

    def __kill(self):
        self.root.destroy()

    def __popupAbout(self):
        self.popup("About", "PayCalculator V{}\nAuthor: Ash Hines".format(
            CONSTS.C_VERSION))

    def __popupLicense(self):
        self.popup("License", (
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
        ))

    def __initLayout(self):
        self.__tabControl = ttk.Notebook(self.root)
        self.__createPayDetailsTab()
        self.__createResultsTab()
        if(CONSTS.C_DEBUG):
            self.debugTab = ttk.Frame(self.__tabControl)
            ttk.Button(self.debugTab, text="BREAK",
                       command=self.__breakpoint).pack()
            self.__tabControl.add(self.debugTab, text="DEBUG")
        self.__tabControl.pack(expand=1, fill="both")

    def __createPayDetailsTab(self):
        self.__valuesTab = ttk.Frame(self.__tabControl)
        self.__bSuper = tk.BooleanVar(self.__valuesTab)
        self.bNTFT = tk.BooleanVar(self.__valuesTab)
        self.bHECS = tk.BooleanVar(self.__valuesTab)
        self.income = tk.StringVar(self.__valuesTab)
        self.hours = tk.StringVar(self.__valuesTab)
        self.hours.set("40")
        self.increment = tk.StringVar(self.__valuesTab)
        self.increment.set(CONSTS.C_INCREMENT_ANNUALLY)
        self.increment.trace('w', self.__optionChange)
        self.FY = tk.StringVar(self.__valuesTab)
        ttk.Label(self.__valuesTab, text="Enter Pay Details Below").grid(
            column=0, row=0, columnspan=3)
        ttk.Label(self.__valuesTab, text="Income $").grid(
            sticky="E", column=0, row=1)
        ttk.Label(self.__valuesTab, text="Pay Increment").grid(
            sticky="E", column=0, row=2)
        self.labelHour = ttk.Label(self.__valuesTab, text="Hours")
        ttk.Label(self.__valuesTab, text="Finincal Year").grid(
            sticky="E", column=0, row=4)
        ttk.Entry(self.__valuesTab, textvariable=self.income).grid(
            column=1, row=1)
        self.entryHours = ttk.Entry(self.__valuesTab, textvariable=self.hours)
        self.entryHours.config(state='disabled')
        ttk.OptionMenu(self.__valuesTab, self.increment, *
                       CONSTS.C_INCREMENT_CHOICES).grid(column=1, row=2, sticky="N"+"S"+"E"+"W")
        ttk.OptionMenu(self.__valuesTab, self.FY, CONSTS.C_FY[0], *CONSTS.C_FY).grid(
            column=1, row=4, sticky="N"+"S"+"E"+"W")
        ttk.Checkbutton(self.__valuesTab, text="No Tax Free Threshold",
                        variable=self.bNTFT).grid(sticky="W", column=2, row=1)
        ttk.Checkbutton(self.__valuesTab, text="HECS/HELP Debt",
                        variable=self.bHECS).grid(sticky="W", column=2, row=2)
        ttk.Checkbutton(self.__valuesTab, text="Includes SuperAnnuation",
                        variable=self.__bSuper).grid(sticky="W", column=2, row=3)
        ttk.Button(self.__valuesTab, text="Calculate", command=self.__calculate).grid(
            column=0, row=5, columnspan=3, sticky="N"+"S"+"E"+"W")

        self.__tabControl.add(self.__valuesTab, text="Pay Details")

    def __createResultsTab(self):
        # print("CreatingResults")
        self.__resultsTab = ttk.Frame(self.__tabControl)
        #ttk.Label(self.__resultsTab, text="Increment").grid(column=0, row=0)
        ttk.Label(self.__resultsTab, text="Taxable Income").grid(
            sticky="W", column=1, row=0, padx=10)
        ttk.Label(self.__resultsTab, text="Superannuation").grid(
            sticky="W", column=2, row=0, padx=10)
        ttk.Label(self.__resultsTab, text="Income Tax").grid(
            sticky="W", column=3, row=0, padx=10)
        ttk.Label(self.__resultsTab, text="Medicare Levy").grid(
            sticky="W", column=4, row=0, padx=10)
        ttk.Label(self.__resultsTab, text="Hecs Payable").grid(
            sticky="W", column=5, row=0, padx=10)
        ttk.Label(self.__resultsTab, text="Total Tax").grid(
            sticky="W", column=6, row=0, padx=10)
        ttk.Label(self.__resultsTab, text="Net Income").grid(
            sticky="W", column=7, row=0, padx=10)
        #rows = self.calc.calculateIncrementVaribles(self.dictCalcResult, self.hours.get())

    def __setTable(self):
        rows = self.calc.calculateIncrementVaribles(
            self.dictCalcResult, int(self.hours.get()))
        i = 1
        for row in rows:
            # (row)
            ttk.Label(self.__resultsTab, text="{}".format(row["Increment"])).grid(
                sticky="W", column=0, row=i, padx=10)
            ttk.Label(self.__resultsTab, text="${:.2f}".format(
                row["taxableIncome"])).grid(sticky="W", column=1, row=i)
            ttk.Label(self.__resultsTab, text="${:.2f}".format(
                row["super"])).grid(sticky="W", column=2, row=i)
            ttk.Label(self.__resultsTab, text="${:.2f}".format(
                row["tax"])).grid(sticky="W", column=3, row=i)
            ttk.Label(self.__resultsTab, text="${:.2f}".format(
                row["medicareLevy"])).grid(sticky="W", column=4, row=i)
            ttk.Label(self.__resultsTab, text="${:.2f}".format(
                row["hecsOwed"])).grid(sticky="W", column=5, row=i)
            ttk.Label(self.__resultsTab, text="${:.2f}".format(
                row["totalTax"])).grid(sticky="W", column=6, row=i)
            ttk.Label(self.__resultsTab, text="${:.2f}".format(
                row["netIncome"])).grid(sticky="W", column=7, row=i)
            i += 1

    def __validate(self, input, type) -> bool:
        try:
            type(input)
            return True
        except:
            return True

    def __showResultsTab(self):
        self.__setTable()
        self.__tabControl.add(self.__resultsTab, text="Results")
        # self.__tabControl.c

    def __optionChange(self, *args):
        #print("OPTION CHANGED")
        if(self.increment.get() == CONSTS.C_INCREMENT_HOURLY):
            self.labelHour.grid(
            sticky="E", column=0, row=3)
            self.entryHours.grid(column=1, row=3)
            self.entryHours.config(state='enabled')
        else:
            self.entryHours.config(state='disabled')
            self.labelHour.grid_forget()
            self.entryHours.grid_forget()
    def __calculate(self):
        options = {
            "bHECS": self.bHECS.get(),
            "bSuper": self.__bSuper.get(),
            "bNTFT": self.bNTFT.get(),
            "iFY": self.FY.get()
        }
        try:
            income = float(self.income.get())
            if(income < 0):
                self.popup("Error", "Income must be positive")
                raise Exception("Income must be positive")
            self.calc = calculate.taxCalculations(income, self.increment.get(
            ), options, hours=int(self.hours.get()) if not self.hours.get() == "" else 40)
            self.dictCalcResult, hours = self.calc.calculate()
            self.hours.set(str(hours))
            self.__showResultsTab()
            self.__tabControl.select(len(self.__tabControl.tabs()) - 1)
        except Exception as e:
            print(str(e))
            self.popup("Error", "Invalid Input", "200x75")

    def __breakpoint(self):
        # PUT A BREAK POINT HERE FOR A BUTTON TO CAUSE A BREAK
        pass

    def popup(self, title, msg, size="auto"):
        popup = tk.Tk()
        if(size == "auto"):
            pass
        else:
            popup.geometry(size)
        popup.wm_title(title)
        label = tk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(popup, text="Okay", command=popup.destroy)
        B1.pack()
        popup.mainloop()


def start():
    # GUI Starts Here.
    gui = GUI()
    gui.root.mainloop()
    sys.exit(0)
