from config import *
import pandas as pd
import regex as re
from fuzzywuzzy import process
import io

#activitydf = pd.read_excel(Activity_File, sheet_name=ActivitySheet, usecols=[PriceColumn, "Date", "Description"])
QB = input("Paste your bank statement ")

QB_input_lines = []
while True:
    line = input()
    if line == "":
        break
    QB_input_lines.append(line)

# Join the lines into a single string with newline characters
QB_input = "\n".join(QB_input_lines)

# Convert the input string to a file-like object
QB_file = io.StringIO(QB_input)
QB_file = QB_file.getvalue()

# class Transaction:
#     def __init__(self):
#         self.sign = None #either + or -
#         self.type = None #either check or description
#     
#     def process_data(self,type):
#         type = self.type
        
def process_data(text):
    pattern_date = r'(\d{2}/\d{2})'  # Pattern to match MM/DD format
    pattern_price = r'\$?\b\d{1,3}(?:,\d{3})*\.\d{2}\b'
    pattern_check_number = r'\b\d{4}\b'

    lines = text.split('\n')
    formatted_lines = []
    dates = []
    prices = []
    descriptions = []
    year_provided = False
    year = ''
    checks = []

    for line in lines:
        match_date = re.search(pattern_date, line)  # Search for MM/DD format
        match_price = re.search(pattern_price, line)  # Search for price with optional comma and decimal
        match_check = re.search(pattern_check_number,line)

        if match_check:
            check = match_check.group()
            checks.append(check)

        if match_date:
            date = match_date.group()
            # Check if the date includes a year
            if len(date.split('/')) == 2:
                if not year_provided:
                    # Ask the user for the year if not already provided
                    year = input("Enter the year for the dates pasted ")
                    year_provided = True
                date += f'/{year}'
            dates.append(date)

            # Extract the description starting after the date
            start = match_date.end()
            if match_price:
                end = match_price.start()
                description = line[start:end].strip()
            else:
                description = line[start:].strip()
            description = re.sub(r'\S*\d\S*', '', description)  # Remove digits
            description = re.sub(r'\b(?:CCD|ID|Bkcd|Stlmt|PPD)\b', '', description, flags=re.IGNORECASE)
            description = re.sub(r'https', '', description, flags=re.IGNORECASE).strip()
            description = re.sub(r'http', '', description, flags=re.IGNORECASE).strip()
            description = re.sub(r'www', '', description, flags=re.IGNORECASE).strip()
            description = re.sub(r'\bRecurring Card Purchase\b', '', description, flags=re.IGNORECASE).strip()
            description = re.sub(r'\bCard Purchase\b', '', description, flags=re.IGNORECASE).strip()
            description = re.sub(r'With Pin', '', description, flags=re.IGNORECASE).strip()
            description = re.sub(r'\b(?:Card)\b', '', description, flags=re.IGNORECASE)
            description = re.sub(r'\bTsysTransfirst\s+', '', description).strip()
            description = re.sub(r'\b[A-Z]{2}\b', '', description)
            description = re.sub(r'New York', '', description)
            description = re.sub(r'[\/\\,-]', '', description)
            description = re.sub(r'(\.com)(?=.*\.com)', '', description, flags=re.IGNORECASE)
            description = re.sub(r'\.(?!com)', '', description, flags=re.IGNORECASE)
            word_counts = len(description.split())
            if word_counts < 2:
                description = re.sub(r'.com', '', description, flags=re.IGNORECASE)
                print(word_counts)
            else:
                description = re.sub(r'\S*\.com\S*', '', description, flags=re.IGNORECASE)  # Remove .com and following word
                description = re.sub(r'\S*\.com\S*', '', description, flags=re.IGNORECASE).strip()

            description = re.sub(r'[.-:\*]', ' ', description)


            # Remove everything after a digit without a preceding space
            description = re.sub(r'(\S*\d\S*).*', '', description)
            description = ' '.join(description.split())
            descriptions.append(description)


        if match_price:
            price = match_price.group()
            price = price.replace('$',"")
            price = price.replace(',','')
            price = f"{float(price):.2f}"
            prices.append(price)

    # Create DataFrame from dates and prices
    df = pd.DataFrame({'Date': dates, 'Description' : descriptions, 'Price': prices})
    df.to_string()
    df.to_clipboard(index = False)
    print(df)
    return df

process_data(QB_file)
