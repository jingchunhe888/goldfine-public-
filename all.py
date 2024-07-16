
from config import *
import pandas as pd
import regex as re
from fuzzywuzzy import process

activitydf = pd.read_excel(Activity_File, sheet_name=ActivitySheet, usecols=[PriceColumn, "Date", "Description"])
QB = input("Paste what is already in QB ")
vendor_list = pd.read_excel(Vendor_File, sheet_name=VendorSheet, usecols=[VendorColumn])


def sort_line(text):
    pattern = r'(\d{1,2}/\d{1,2}(?:/\d{2})?)'
    lines = text.split('\n')
    formatted_lines = []
    count = 0

    for line in lines:
        match = re.match(pattern, line)
        if match:
            formatted_lines.append("\n" + line)
            count += 1
        else:
            if formatted_lines:
                formatted_lines[-1] += " " + line
                count -= 1
    print("format lies")
    print(formatted_lines)
    formatted_text = '\n'.join(formatted_lines)
    return formatted_text.strip()
def is_subsequence(vendor_name, description):
    # Clean up vendor name and description for comparison
    vendor_words = re.findall(r'\b\w+\b', vendor_name.lower())
    desc_words = re.findall(r'\b\w+\b', description.lower())

    # Ignore common punctuation
    vendor_words = [word.strip('.,') for word in vendor_words]
    desc_words = [word.strip('.,') for word in desc_words]

    # Check if vendor words appear in sequence within description words
    i, j = 0, 0
    while i < len(vendor_words) and j < len(desc_words):
        if vendor_words[i] == desc_words[j]:
            i += 1
        j += 1

    # If all remaining vendor words are found in sequence, return True
    return i == len(vendor_words)
def find_price(text):
    dates = []
    prices = []
    descriptions = []
    matched_vendors = []
    has_match_vendor = []
    has_match_activity = []

    pattern_date = r'(\d{1,2}/\d{1,2}(?:/\d{2})?)'
    pattern_price = r'\$?\d+\.\d{2}\b'
    lines = text.split('\n')

    year_provided = True
    year = ""

    for line in lines:
        match_price = re.search(pattern_price, line)
        match_date = re.match(pattern_date, line)

        if match_date:
            date = match_date.group()
            # Check if the date includes a year
            if len(date.split('/')) == 2:
                if not year_provided:
                    # Ask the user for the year if not already provided
                    pass
                #date += f'/{year}'
            dates.append(date)

            # Extract the description starting after the date
            start = match_date.end()
            if match_price:
                end = match_price.start()
                description = line[start:end].strip()
            else:
                description = line[start:].strip()

            description = re.sub(r'\d', '', description)
            description = re.sub(r'\b(?:Card|Purchase)\b', '', description, flags=re.IGNORECASE)
            description = re.sub(r'[\/\\,]', '', description)
            description = re.sub(r'\.com\b', '', description, flags=re.IGNORECASE)
            description = re.sub(r'[.-]', '', description)
            descriptions.append(description)

            if True:
                best_match, score = process.extractOne(description, vendor_list)
                if score >= FuzzyMatch:
                    # Check if the best match is a subsequence of description
                    if is_subsequence(best_match, description):
                        matched_vendors.append(best_match)
                        has_match_vendor.append(True)
                    else:
                        matched_vendors.append('')
                        has_match_vendor.append(False)
                else:
                    matched_vendors.append('')
                    has_match_vendor.append(False)
            else:
                matched_vendors.append('')
                has_match_vendor.append(False)

        if match_price:
            price = match_price.group()
            price = float(price.replace("$", ""))
            prices.append(price)

    # Ensure all lists are of the same length by padding with empty strings or zeros
    max_length = max(len(dates), len(descriptions), len(prices))
    dates.extend([''] * (max_length - len(dates)))
    descriptions.extend([''] * (max_length - len(descriptions)))
    prices.extend([0.0] * (max_length - len(prices)))

    cached_df = pd.DataFrame(
        {'Date': dates, 'Description': descriptions, 'Vendor': matched_vendors, 'Price': prices,
         'Matched Vendor':has_match_vendor})

    return cached_df
#main code

sorted_output = sort_line(QB)
result_df = find_price(sorted_output)
filtered_df = result_df[result_df['Matched Vendor'].isin([True])]

print("this is the sorted output")
print(sorted_output)

print("this is the result df")
print(result_df)

print("this is the filtered df")
print(filtered_df)


unmatched_activity = activitydf[~activitydf["Amount"].isin(result_df["Price"])]

print("find unmatched")
print(unmatched_activity)






