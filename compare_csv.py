from csv_diff import load_csv, compare

def compare_csv_files(file1, file2, key_column):
    # Load the CSV files
    file1_data = load_csv(open(file1), key_column)
    file2_data = load_csv(open(file2), key_column)

    # Compare the CSV files
    diff = compare(file1_data, file2_data)

    # Print added rows
    print("\nAdded rows:")
    for row in diff["added"]:
        print(row)

    # Print removed rows
    print("\nRemoved rows:")
    for row in diff["removed"]:
        print(row)

    # Print changed rows
    print("\nChanged rows:")
    for change in diff["changed"]:
        key = change["key"]
        print(f"Row with key '{key}' has changes:")
        for column, column_diff in change["changes"].items():
            if isinstance(column_diff, list):
                # Handle multiple changes in a column
                print(f"  Column '{column}': Multiple changes -> {column_diff}")
            elif isinstance(column_diff, dict):
                # Handle single change in a column
                print(f"  Column '{column}': {column_diff['old_value']} -> {column_diff['new_value']}")

if __name__ == "__main__":
    # Specify the files and key column
    file1 = "data_01.csv"
    file2 = "data_02.csv"
    key_column = "gfrgebaeudeid"

    compare_csv_files(file1, file2, key_column)
