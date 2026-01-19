import csv
import io

csv_path = '/Users/msn/Desktop/MS_Dev.nosync/projects/kerygma-library/kerygma_books.csv'

# New entry data
new_entry = {
    '제목': '칭의와 화목: 바울 신학의 두 가지 핵심 축',
    'Nr.': '999', # Temporary ID
    'source': 'https://www.youtube.com/watch?v=cZIiukWxjJE',
    '기타': 'Theology, Paul, Justification',
    '링크': 'https://share.note.sx/fa1r60kd',
    '저자': 'Jens Schröter'
}

# Append to CSV
with open(csv_path, 'a', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['제목', 'Nr.', 'source', '기타', '링크', '저자'])
    writer.writerow(new_entry)

print(f"Added entry: {new_entry['제목']}")
