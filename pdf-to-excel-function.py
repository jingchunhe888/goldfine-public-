import re
def clean_lines(input_line):
    date_or_check = ''
    pattern_date = re.compile(r'^\d{2}/\d{2}')
    pattern_check_number = re.compile(r'^\d{4}\b')  # Pattern to match four-digit number at the start of the line
    pattern_balance = re.compile(r'.*balance.*', flags=re.IGNORECASE)

    for index, char in enumerate(input_line):
        if pattern_balance.match(input_line):
            return None
        if char.isdigit() or char == '/':
            date_or_check += char
            match_date = pattern_date.match(date_or_check)
            match_check = pattern_check_number.match(date_or_check)
            if index == len(input_line)-5:
                #print('None')
                return None

            if match_date:
                date_or_check = match_date.group()
                end = index + 1
                remainingString = date_or_check + input_line[end:]
                #print('here')
                return remainingString
                    #print("remain" + remainingString)
                    #break
            if match_check:
                date_or_check = match_check.group()
                end = index + 1
                    # print(end)
                remainingString = date_or_check + input_line[end:]
                return remainingString
                    # print("remain" + remainingString)
                    #break
    return None
