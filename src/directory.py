import json
import os
from .utils import get_previous_month_and_year


def get_output_files() -> dict:
    """
    Get the paths to the output files.
    Returns:
        A dict containing the paths to the output files. Keys: ["leaves", "bank", "refund",
        "student", "amount"]
    """
    parent_dir = os.getcwd()
    current_date = "{}_{}".format(*get_previous_month_and_year())
    output_dir = os.path.join(parent_dir, 'output')
    return {
        "leaves": os.path.join(output_dir, 'leave_data', f'{current_date}.json'),
        "bank": os.path.join(output_dir, 'bank_data', f'{current_date}.xlsx'),
        "refund": os.path.join(output_dir, 'refund_data', f'{current_date}.json'),
        "student": os.path.join(output_dir, 'student_data', f'{current_date}.json'),
        "amount": os.path.join(output_dir, 'amount_data', f'{current_date}.json')
    }


def get_config_data() -> dict:
    """
    Get the data from the config file.
    Returns:
        The data from the config file as a dictionary.
    """
    parent_dir = os.getcwd()
    config_file_path = os.path.join(parent_dir, 'config', 'config.json')
    with open(config_file_path, 'r') as file:
        config_data = json.load(file)
    return config_data


def get_latest_data() -> dict:
    """
    Get the paths to the latest files in the leaves, student_data and financial_aid directories.
    Returns: A dict containing the paths to the latest files. Keys: ["leaves", "monthly_subscription",
    "semester_subscription", "financial_aid"]
    """
    parent_dir = os.getcwd()
    input_dir = os.path.join(parent_dir, 'input')
    leaves_directory = os.path.join(input_dir, 'leaves')
    subscription_data_directory = os.path.join(input_dir, 'student_data')
    monthly_subscription_data_directory = os.path.join(subscription_data_directory, 'monthly')
    semester_subscription_data_directory = os.path.join(subscription_data_directory, 'semester')
    financial_aid_directory = os.path.join(input_dir, 'financial_aid')
    return {
        "leaves": get_latest_file(leaves_directory),
        "monthly_subscription": get_latest_file(monthly_subscription_data_directory),
        "semester_subscription": get_latest_file(semester_subscription_data_directory),
        "financial_aid": get_latest_file(financial_aid_directory)
    }


def get_input_files() -> dict:
    """
    Rename the files to the current date, and return the new file paths.
    Returns:
        A dict containing the paths to the renamed files. Keys: ["leaves", "monthly_subscription",
        "semester_subscription", "financial_aid"]
    """
    current_date = "{}_{}".format(*get_previous_month_and_year())
    latest_data = get_latest_data()
    new_file_paths = {}
    for key, file_path in latest_data.items():
        dir_name = os.path.dirname(file_path)
        _, ext = os.path.splitext(file_path)
        new_file_path = os.path.join(dir_name, f"{current_date}{ext}")

        try:
            os.rename(file_path, new_file_path)
        except FileExistsError:
            print(f"{file_path} already exists. In order to run the program, delete the existing file with name {current_date}{ext}.")
        except FileNotFoundError:
            print(f"{file_path} not found.")
        except PermissionError:
            print(f"{file_path} not readable.")

        new_file_paths[key] = new_file_path
    return new_file_paths


def get_latest_file(dir_path: str) -> str:
    """
    Get the path to the latest file in the directory.
    Args:
        dir_path: The path to the directory.
    Returns:
        The path to the latest file in the directory.
    """
    files = os.listdir(dir_path)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(dir_path, x)))
    return os.path.join(dir_path, files[-1])
