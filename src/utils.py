from datetime import datetime
import pandas as pd
import logging
from enum import Enum


def get_previous_month_and_year() -> list[int]:
    """
    Get the previous monthly and year.
    Returns:
        A list containing the previous monthly and year.
    """
    month = datetime.now().month - 1
    year = datetime.now().year
    if month == 0:
        month = 12
        year -= 1
    return [month, year]


def merge_data(leave_file: str, student_file: str, refund_file: str) -> pd.DataFrame:
    student_data = pd.read_json(student_file)
    leave_data = pd.read_json(leave_file)
    merged_df = pd.merge(student_data, leave_data, how='outer', on='identifier')
    merged_df = merged_df.fillna(0)
    merged_df = merged_df[merged_df['days'] != 0]
    merged_df.to_json(refund_file, orient='records', indent=4)
    return merged_df


def setup_logger() -> logging.Logger:
    """
    Setup the logger.
    Returns:
        The logger object.
    """
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()],
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8',
        filemode='w',
        filename=f'{__name__}.log',
        force=True,
        style='%'
    )
    return logger


def log(level: str = 'info', message: str = ''):
    """
    Log a message at the specified level.
    Args:
        level: The log level.
        message: The message to log.
    """
    if level == 'info':
        logging.info(message)
    elif level == 'debug':
        logging.debug(message)
    elif level == 'warning':
        logging.warning(message)
    elif level == 'error':
        logging.error(message)
    elif level == 'critical':
        logging.critical(message)
    else:
        logging.info(message)
