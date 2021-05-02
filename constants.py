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
###Constants

C_VERSION = "1.0.0"
C_FY = ("2019-2020", "2020-2021")
C_TAXFILE = "taxrates.json"
C_INCREMENT_HOURLY = "Hourly"
C_INCREMENT_DAILY = "Daily"
C_INCREMENT_WEEKLY = "Weekly"
C_INCREMENT_FORTNIGHTLY = "Fortnightly"
C_INCREMENT_MONTHLY = "Monthly"
C_INCREMENT_ANNUALLY = "Annually"
C_WEEKSPYEAR = 52
C_MEDICARE_LEVY_RATE = 0.02
C_DEBUG = False
C_INCREMENT_CHOICES = (
    "",
    C_INCREMENT_HOURLY,
    C_INCREMENT_DAILY,
    C_INCREMENT_WEEKLY,
    C_INCREMENT_FORTNIGHTLY,
    C_INCREMENT_MONTHLY,
    C_INCREMENT_ANNUALLY,
)

###
