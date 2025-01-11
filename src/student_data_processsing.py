import pandas as pd


def fetch_student_data(monthly_subscription_file: str, semester_subscription_file: str, financial_aid_file: str,
                       output_file: str):
    """
    Fetch all the student data from the input files, combine them properly and write the output to a file.
    """
    monthly_df = process_student_data_df(monthly_subscription_file)
    semester_df = process_student_data_df(semester_subscription_file)
    try:
        additional_financial_aid_data = set(
            ','.join(pd.read_csv(financial_aid_file).astype(str).values.flatten()).split(',')
        )
    except FileNotFoundError:
        print("No additional financial aid data found.")
        additional_financial_aid_data = set()

    monthly_df['subscription_type'] = 'month'
    semester_df['subscription_type'] = 'semester'

    combined_df = pd.concat([monthly_df, semester_df], ignore_index=True)

    # Update the 'financial_help' column based on the additional financial aid data
    combined_df.loc[
        combined_df['identifier'].isin(additional_financial_aid_data),
        'financial_help'
    ] = True

    combined_df.to_json(output_file, orient='records', indent=4)


def process_student_data_df(input_file: str):
    """
    Modify the dataframe to later merge them together.
    """

import pandas as pd

def process_student_data_df(input_file: str):
    # Return an empty dataframe if file is empty
    if input_file == 'empty':
        return pd.DataFrame()

    df = pd.read_csv(input_file, sep='\t')    

    email_col = [col for col in df.columns if 'email' in col.lower()]
    meals_col = [col for col in df.columns if 'meal' in col.lower()]
    financial_col = [col for col in df.columns if 'financial' in col.lower()]

    if not (len(email_col) == 1 and len(meals_col) == 1 and len(financial_col) == 1):
        raise ValueError("Could not uniquely identify columns for email, meals, and financial help.")

    df['identifier'] = df[email_col[0]].apply(lambda x: x.split('@')[0])
    df['no_of_meals'] = df[meals_col[0]].apply(lambda x: len(x.split(',')))
    df['financial_help'] = df[financial_col[0]]

    return df[['identifier', 'financial_help', 'no_of_meals']]