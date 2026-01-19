import csv
import os

csv_path = '/Users/msn/Desktop/MS_Dev.nosync/projects/kerygma-library/kerygma_books.csv'

# Define the data to be added
new_entry = {
    '제목': '칭의와 화목: 바울 신학의 두 가지 핵심 축',
    'Nr.': '999',
    'source': 'https://www.youtube.com/watch?v=cZIiukWxjJE',
    '기타': 'Theology, Paul, Justification',
    '링크': 'https://share.note.sx/fa1r60kd',
    '저자': 'Jens Schröter'
}

# 1. Read existing data and filter out the bad line (the one with too many commas or empty title)
rows = []
fieldnames = []
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        # Check for our botched entry (if title is empty but other fields have our data)
        # The bad line looked like: ,,,,,Title... which means '제목' was empty.
        if not row.get('제목'):
            continue
        rows.append(row)

# 2. Append the new entry
rows.append(new_entry)

# 3. Write back cleanly
with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Repaired CSV and added: {new_entry['제목']}")
