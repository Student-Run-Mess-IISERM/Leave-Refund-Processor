import pandas as pd


def create_bank_file(data: pd.DataFrame, bank_file: str):
    columns_to_drop = ['days', 'financial_help', 'no_of_meals', 'dates', 'subscription_type']
    data.drop(columns_to_drop, axis=1, inplace=True)
    rename_map = {
        "identifier": "Registration Number",
        "name": "Name",
        "ifsc": "IFSC",
        "account_holder": "Name of Account Holder",
        "account_number": "Account Number",
        "refund_amount": "Refund Amount",
    }
    data.rename(columns=rename_map, inplace=True)
    data['Account Number'] = data['Account Number'].astype(str)
    cnr_data = data[data['IFSC'].str.startswith('CNR')]
    non_cnr_data = data[~data['IFSC'].str.startswith('CNR')]

    with pd.ExcelWriter(bank_file, engine='xlsxwriter') as writer:
        data.to_excel(writer, sheet_name='Combined', index=False)
        cnr_data.to_excel(writer, sheet_name='Canara Bank Accounts', index=False)
        non_cnr_data.to_excel(writer, sheet_name='Non Canara Bank Accounts', index=False)
