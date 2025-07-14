import json

# Read the multi-line JSON file
with open('temp_data/temp_databases/temp.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Write each object as a single line to the output file
with open('temp_data/temp_databases/temp_oneline.json', 'w', encoding='utf-8') as f:
    for item in data:
        json.dump(item, f, ensure_ascii=False)
        f.write('\n')