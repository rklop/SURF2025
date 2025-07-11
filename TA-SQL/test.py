import csv

with open('TA-SQL/data/final_results.json', 'r') as f:
    reader = csv.DictReader(f)

    final_results = list(reader)

