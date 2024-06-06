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

    # Add a column to indicate the subscription type
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
    df = pd.read_csv(input_file, sep='\t')
    columns_to_keep = ['Email Address', 'Meals you want to take', 'Is your financial help approved?']
    df = df[columns_to_keep]
    df['identifier'] = df['Email Address'].apply(lambda x: x.split('@')[0])
    df['no_of_meals'] = df['Meals you want to take'].apply(lambda x: len(x.split(',')))
    df.rename(columns={'Is your financial help approved?': 'financial_help'}, inplace=True)

    df = df[['identifier', 'financial_help', 'no_of_meals']]

    return df
