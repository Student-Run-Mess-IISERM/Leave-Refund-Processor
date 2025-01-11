from src.directory import get_input_files, get_output_files
from src.student_data_processsing import fetch_student_data
from src.leave_data_processing import fetch_leave_data
from src.amount_processing import calculate_refunds
from src.bank_processing import create_bank_file
from src.utils import merge_data


def main():
    input_files = get_input_files()
    output_files = get_output_files()
    fetch_leave_data(input_files["leaves"], output_files["leaves"])
    fetch_student_data(
        input_files["monthly_subscription"],
        input_files["semester_subscription"],
        input_files["financial_aid"],
        output_files["student"]
    )
    merge_data(output_files["leaves"], output_files["student"], output_files["refund"])
    amount_included_data = calculate_refunds(output_files["refund"], output_files["amount"])
    create_bank_file(amount_included_data, output_files["bank"])
    print("Done processing.")


if __name__ == '__main__':
    main()