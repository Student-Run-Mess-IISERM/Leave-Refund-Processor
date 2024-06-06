# Leave Refund Processor

This script processes leave refund from the Student Run Mess's subscription, request by students of Indian Institute of Science Education and Research, Mohali.

## How to use

### Prerequisites
1. Python 3.6 or higher with `pandas` and `xlsxwriter` installed.
2. Anywhere in the following instructions, `*` is a placeholder that means you can use any arbitrary name.

### Instructions
1. Clone the repository/ Download as a zip file.
2. Download the Semester subscription data from the Student Run Mess's Google Drive as a `tsv` file, save it in the `input/student_data/semester/*.tsv` directory.
3. Download the Monthly refund data from the Student Run Mess's Google Drive as a `tsv` file, save it in the `input/student_data/monthly/*.tsv` directory.
4. Download the leave detail data from the Student Run Mess's Google Drive as a `tsv` file, save it in the `input/leaves/*.tsv` directory.
5. If anyone is to be given financial aid outside of what is specified in subscription, add their registration number in the `input/financial_aid/*.tsv` file seperated by `,`.
6. In the `config/config.json` file, set:
    - 'month': Number of the month for which the refund is to be processed. Ex:  March is 3.
    - 'financial_aid': Discount to be given to students with financial aid. Ex: 0.3 for 30% discount.
    - Also set the price for each meal for both monthly as well as semester subscriptions.
7. Run the `main.py` script with the following command:
    ```bash
    python main.py
    ```
   
# What does the script do?
In order:
1. Renames all the data inputted to previous month number and year. We process March Refunds in April.
2. Reads the leave data, eliminates duplicate entries if any, and calculates the total days of leave taken by each student.
3. Reads the subscription data for the semester and the month, and merges them into a single dataframe.
4. Based on the leave data and subscription data, calculates the total refund for each student for the specified month.
5. Writes the refund data to an Excel file in the `output/` directory.

The file that SRMC submits to admin is the `output/bank_data/*.xlsx` file.
For the SRMC records, the `output/amount_data/*.json` file is used.

# Contributing
If you want to contribute to this project, please follow the following steps:
1. Fork the repository.
2. Create a new branch with the name of the feature/ bug fix you are working on.
3. Make your changes.

Contributions can also be made by identifying and reporting bugs, suggesting improvements, or proposing new features in the issues section of the repository.