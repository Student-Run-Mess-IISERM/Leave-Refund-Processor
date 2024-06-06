import pandas as pd
from src.directory import get_config_data


def calculate_refunds(refund_file: str, output_amount_file: str) -> pd.DataFrame:
    """
    Calculate refunds for students based on their identifier, number of days, and number of meals.
    Also consider additional financial aid if applicable.

    Args:
    refund_file (str): Path to the JSON file containing refund data.
    output_amount_file (str): Path to the JSON file where output data with calculated refunds will be saved.

    Returns:
    pd.DataFrame: DataFrame containing the original data with an additional column for refund amounts.
    """
    # Load data
    all_data = pd.read_json(refund_file)
    config_data = get_config_data()
    all_data['refund_amount'] = all_data.apply(
        lambda row: calculate_amount(row, config_data), axis=1
    )
    all_data.to_json(output_amount_file, orient='records', indent=4)
    return all_data


def calculate_amount(row, config_data):
    refund_amount = get_refund_amount_per_day(row['subscription_type'], row['no_of_meals'], config_data)
    if row['financial_help'] == "Yes":
        return round(row['days'] * refund_amount * (1 - config_data["financial_aid"]))
    else:
        return round(row['days'] * refund_amount)


def get_refund_amount_per_day(subscription_type: str, no_of_meals: int, config_data: dict) -> float:
    if subscription_type == "month":
        return config_data["monthly"][str(no_of_meals)]
    elif subscription_type == "semester":
        return config_data["semester"][str(no_of_meals)]
    else:
        return 0.0
