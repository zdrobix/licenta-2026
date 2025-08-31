import csv
import pandas as pd

def append_unique_rows(csv1_path, csv2_path):
    with open(csv2_path, newline='', encoding='utf-8') as f2:
        reader2 = csv.reader(f2)
        csv2_rows = set(tuple(row) for row in reader2)

    with open(csv1_path, newline='', encoding='utf-8') as f1, \
         open(csv2_path, 'a', newline='', encoding='utf-8') as f2:
        reader1 = csv.reader(f1)
        writer2 = csv.writer(f2)
        for row in reader1:
            if tuple(row) not in csv2_rows:
                writer2.writerow(row)
                csv2_rows.add(tuple(row))

if __name__ == "__main__":
    append_unique_rows("melodii_versuri_genius.csv", "melodii_versuri_genius_unic.csv")