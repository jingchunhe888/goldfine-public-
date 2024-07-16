import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import re
from config-compare import *


class BankStatementMatcherApp:

    def __init__(self, root):

        self.file_path_qb = None
        self.file_path_statement = None
        self.start_date = None
        self.end_date = None
        self.root = root
        self.root.title("Quick-er-Books")

        # QB file upload section
        self.qb_file_label = tk.Label(root, text="Upload QB File:")
        self.qb_file_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.qb_file_button = tk.Button(root, text="Upload QB", command=self.upload_qb_file)
        self.qb_file_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.qb_file_status = tk.Label(root, text="Current File: None")
        self.qb_file_status.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        # Bank statement file upload section
        self.bank_file_label = tk.Label(root, text="Upload Bank Statement:")
        self.bank_file_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.bank_file_button = tk.Button(root, text="Upload Bank Statement", command=self.upload_bank_file)
        self.bank_file_button.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.bank_file_status = tk.Label(root, text="Current File: None")
        self.bank_file_status.grid(row=1, column=2, padx=5, pady=5, sticky='w')

        # Start date entry
        self.start_date_label = tk.Label(root, text="Start Date (YYYY-MM-DD):")
        self.start_date_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.start_date_entry = tk.Entry(root, width=20)
        self.start_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.start_date_status = tk.Label(root, text="Current Start Date: None")
        self.start_date_status.grid(row=2, column=2, padx=5, pady=5, sticky='w')

        # End date entry
        self.end_date_label = tk.Label(root, text="End Date (YYYY-MM-DD):")
        self.end_date_label.grid(row=3, column=0, padx=5, pady=5, sticky='e')

        self.end_date_entry = tk.Entry(root, width=20)
        self.end_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.end_date_status = tk.Label(root, text="Current End Date: None")
        self.end_date_status.grid(row=3, column=2, padx=5, pady=5, sticky='w')

        # Update dates button
        self.update_dates_button = tk.Button(root, text="Update Dates", command=self.update_dates)
        self.update_dates_button.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        # Summary output
        self.summary_button = tk.Button(root, text="Summary", command=self.main)
        self.summary_button.grid(row=5, column=0, padx=5, pady=5, sticky='w')

        self.summary_text = scrolledtext.ScrolledText(root, width=100, height=20)
        self.summary_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

    def upload_qb_file(self):
        file_path_qb = filedialog.askopenfilename(title="Select QB File", filetypes=[("All files", "*.*")])
        if file_path_qb:
            self.file_path_qb = file_path_qb
            self.qb_file_status.config(text=f"Current File: {file_path_qb}")
        else:
            messagebox.showwarning("Warning", "No file selected")

    def upload_bank_file(self):
        file_path_statement = filedialog.askopenfilename(title="Select Bank Statement File", filetypes=[("All files", "*.*")])
        if file_path_statement:
            self.file_path_statement = file_path_statement
            self.bank_file_status.config(text=f"Current File: {file_path_statement}")
        else:
            messagebox.showwarning("Warning", "No file selected")

    def update_dates(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        if start_date:
            self.start_date = start_date
            self.start_date_status.config(text=f"Current Start Date: {start_date}")
        else:
            messagebox.showwarning("Warning", "No start date entered")

        if end_date:
            self.end_date = end_date
            self.end_date_status.config(text=f"Current End Date: {end_date}")
        else:
            messagebox.showwarning("Warning", "No end date entered")

    def get_qb_file_path(self):
        print(self.file_path_qb)
        return self.file_path_qb

    def get_bank_file_path(self):
        print(self.file_path_statement)
        return self.file_path_statement

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def main(self):
        # Example of using the file paths and dates
        qb_file_path = self.get_qb_file_path()
        bank_statement_path = self.get_bank_file_path()
        startDate = self.get_start_date()
        endDate = self.get_end_date()

        # Import activity data
        activitydf = pd.read_csv(bank_statement_path , usecols=ActivityColumns , skiprows=ActivitySkipRow)

        # Import QB data
        QBdf = pd.read_excel(qb_file_path, skiprows=QBskipRow, usecols=QBColumns)

        # Check if a value is numeric
        def is_numeric(value):
            try:
                float(value)
                return True
            except ValueError:
                return False

        # Convert date format to MM/DD/YYYY
        def convert_date_format(date_str):
            date_str = date_str.strip()
            date_patterns = [r'(\d{1,2})/(\d{1,2})/(\d{4})']
            for pattern in date_patterns:
                match = re.match(pattern, date_str)
                if match:
                    month, day, year = match.groups()
                    return f'{month.zfill(2)}/{day.zfill(2)}/{year}'
            return None

        # Clean and process QB data
        #QBdf['Amount'] = pd.to_numeric(QBdf['Amount'])
        QBdf.loc[:,'Amount'] = QBdf['Amount'].apply(pd.to_numeric)

        QBdf.rename(columns={'Date': 'Trans. Date'}, inplace=True)
        QBdf['Trans. Date'] = QBdf['Trans. Date'].astype(str).apply(convert_date_format)
        QBdf['Trans. Date'] = pd.to_datetime(QBdf['Trans. Date'], format='%m/%d/%Y')
        filteredQB = QBdf.dropna(subset=['Trans. Date'])
        filteredQB = filteredQB[filteredQB['Clr'] != 'R']

        # Clean and process activity data
        activitydf['Trans. Date'] = activitydf['Trans. Date'].astype(str).apply(convert_date_format)
        activitydf['Posting Date'] = activitydf['Posting Date'].astype(str).apply(convert_date_format)
        activitydf['Posting Date'] = activitydf['Posting Date'].fillna(pd.to_datetime(activitydf['Trans. Date']))
        activitydf['Posting Date'] = pd.to_datetime(activitydf['Posting Date'], format='%m/%d/%Y')
        activitydf['Trans. Date'] = pd.to_datetime(activitydf['Trans. Date'], format='%m/%d/%Y')
        filteredActivity = activitydf[
            (activitydf['Posting Date'] >= startDate) & (activitydf['Posting Date'] <= endDate)]
        filteredActivity.loc[:,'Amount'] = filteredActivity.apply(
           lambda row: row['Amount'] if is_numeric(row['Amount']) else row['MCC'], axis=1)
        #filteredActivity['Amount'] = filteredActivity.apply(
        #   lambda row: row['Amount'] if is_numeric(row['Amount']) else row['MCC'], axis=1)
        # Use .loc to assign values:
        filteredActivity.loc[:, 'Amount'] = filteredActivity['Amount'].apply(pd.to_numeric)

        #filteredActivity['Amount'] = pd.to_numeric(filteredActivity['Amount'])
        filteredActivity = filteredActivity[
            ~filteredActivity['CardHolder Name'].isin(['ANA MAS', 'JUAN DIEGUEZ', 'DIGNA CABRAL', 'ERICK MEDINA'])]

        # Identify duplicates
        duplicatesQB = filteredQB.duplicated(subset=['Trans. Date', 'Amount'], keep=False)
        filteredQB['Duplicates'] = duplicatesQB.groupby(
            [filteredQB['Trans. Date'], filteredQB['Amount']]).cumcount().astype(float).where(duplicatesQB, 0.0)

        duplicatesActivity = filteredActivity.duplicated(subset=['Trans. Date', 'Amount'], keep=False)
        filteredActivity['Duplicates'] = duplicatesActivity.groupby(
            [filteredActivity['Trans. Date'], filteredActivity['Amount']]).cumcount().astype(float).where(
            duplicatesActivity, 0.0)

        # Merge filtered data
        merged = pd.merge(filteredActivity, filteredQB, on=['Trans. Date', 'Amount', 'Duplicates'],
                          suffixes=(" Activity", " QB"), how='outer', indicator=True)
        merge_summary = merged['_merge'].value_counts()

        # Check the total row count
        missing = merged[(merged['_merge'] == 'left_only') | (merged['_merge'] == 'right_only')]
        columns = ['_merge', 'Amount', 'Trans. Date', 'CardHolder Name']
        missing = missing[columns]

        # Replace the values in the _merge column
        categories_map = {'left_only': 'Add', 'right_only': 'Remove'}
        missing['_merge'] = missing['_merge'].cat.rename_categories(categories_map)

        # Rename the columns
        missing = missing.rename(columns={'_merge': 'QB Status', 'Trans. Date': 'Date', 'Amount': 'Amount',
                                          'CardHolder Name': 'Card Holder Name'})

        self.summary_text.delete('1.0', tk.END)

        # Print new summary text
        self.summary_text.insert(tk.END, missing.to_string(justify ='center', index=False), "center")


if __name__ == "__main__":
    root = tk.Tk()
    app = BankStatementMatcherApp(root)
    root.mainloop()
