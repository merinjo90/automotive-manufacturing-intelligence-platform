import csv


def write_records_to_csv(records,filepath):
    fieldnames = records[0].keys()
    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)