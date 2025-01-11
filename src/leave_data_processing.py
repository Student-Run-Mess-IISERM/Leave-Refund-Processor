import pandas as pd
from .directory import get_config_data

def fetch_leave_data(filepath, output_path):
    mappings = {
        'Name': 'name',
        'Bank Account Number': 'account_number',
        'Branch IFSC Code': 'ifsc',
        'Name of the Account Holder': 'account_holder',
    }
    month = get_config_data()['month']
    data = pd.read_csv(filepath, sep='\t')
    data['identifier'] = data['Email Address'].str.extract(r'(.*)@iisermohali.ac.in')
    data['Start Date'] = pd.to_datetime(data['Start Date'], format='%m/%d/%Y')
    data['End Date'] = pd.to_datetime(data['End Date'], format='%m/%d/%Y')
    data['dates'] = data.apply(lambda row: get_dates(row['Start Date'], row['End Date'], month), axis=1)
    data = data[data['dates'].apply(len) > 1]
    data = data.drop_duplicates(subset=['identifier', 'Start Date', 'End Date'])
    data = data.rename(columns=mappings)
    data['account_number'] = data['account_number'].astype(str).str.lstrip('@')
    data['ifsc'] = data['ifsc'].astype(str).str.lstrip('@')
    data = data.drop(columns=[
        'Timestamp', 
        'Registration Number', 
        'Remarks', 
        'No. of Days',
        'Email Address', 
        'Start Date', 
        'End Date'
    ])
    data = aggregate_data(data)
    data.to_json(output_path, orient='records', indent=4)

def aggregate_data(data):
    aggregator = {
        'name': 'first',
        'account_holder': 'first',
        'account_number': 'first',
        'ifsc': 'first',
        'dates': lambda dates: list(set.union(*dates))
    }
    aggregated_data = data.groupby('identifier').agg(aggregator)
    aggregated_data['days'] = aggregated_data['dates'].apply(len)
    # aggregated_data = aggregated_data[aggregated_data['days'] < 9]
    aggregated_data['dates'] = aggregated_data['dates'].apply(sorted)
    aggregated_data.reset_index(inplace=True)
    return aggregated_data

def get_dates(start_date, end_date, chosen_month):
    date_range = pd.date_range(start_date, end_date).to_series()
    chosen_dates = date_range[date_range.dt.month == chosen_month]
    chosen_dates_set = {date.strftime('%Y-%m-%d') for date in chosen_dates}
    return chosen_dates_set
