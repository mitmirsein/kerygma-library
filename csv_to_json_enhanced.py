import csv
import json

# Define clean category logic
def assign_category(book):
    title = book.get('title', '').lower()
    author = book.get('author', '').lower()
    source = book.get('source', '').lower()
    
    # 1. Biblical Studies (Paul, Jesus, OT/NT, Parables, Exegesis)
    if any(x in title or x in author for x in ['paul', '바울', 'jesus', '예수', 'bultmann', '불트만', 'bible', '성서', 'gospel', '복음', 'john', '요한', 'exodus', '출애굽', 'new testament', '신약', 'old testament', '구약', 'scriptura', 'parable', '비유', 'exegesis', '주석', 'zimmer', '침머']):
        return "Biblical Studies"
        
    # 2. Historical Theology (Reformation, Ancient, History, Semler, Harnack)
    if any(x in title or x in source or x in author for x in ['reformation', '종교개혁', 'luther', '루터', 'calvin', '칼뱅', 'ancient', '고대', 'history', '역사', 'harnack', '하르낙', 'tertullian', '테르툴리아누스', 'creed', '신조', 'semler', '젬러', 'patristic', '교부']):
        return "Historical Theology"

    # 3. Systematic Theology (Dogmatics, God, Karl Barth, Welker, Pannenberg)
    if any(x in title or x in author for x in ['barth', '바르트', 'welker', '벨커', 'pannenberg', '판넨베르크', 'moltmann', '몰트만', 'dogmatics', '교리', 'systematic', '조직신학', 'trinity', '삼위일체', 'christology', '기독론', 'justification', '칭의', 'reconciliation', '화목', 'salvation', '구원']):
        return "Systematic Theology"

    # 4. Science & Humanities (Emotion, Brain, Climate, Philosophy, Roth)
    if any(x in title or x in author for x in ['emotion', '감정', 'brain', '뇌', 'climate', '기후', 'science', '과학', 'philosophy', '철학', 'kant', '칸트', 'humanities', '인문', 'capitalism', '자본주의', 'roth', 'sternstunde', 'zurich', '취리히']):
        return "Science & Humanities"

    # 5. Practical & Spirituality (Sermon, Life, Meaning, Anselm Grün)
    if any(x in title or x in author for x in ['sermon', '설교', 'spirituality', '영성', 'prayer', '기도', 'life', '삶', 'meaning', '의미', 'anselm', '안셀름', 'meditation', '묵상']):
        return "Practical & Spirituality"
        
    # 6. Lectures & Talk (Worthaus, Interview)
    if 'worthaus' in source or 'interview' in title or '대담' in title or '강연' in title:
        return "Lectures & Talk"
        
    # 7. Others (Default)
    return "Others"

csv_path = 'kerygma_books.csv'
js_output_path = 'library_data.js'

books = []

with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row.get('제목'):
            continue
            
        book = {
            "title": row.get('제목', '').strip(),
            "author": row.get('저자', '').strip(),
            "link": row.get('링크', '').strip(),
            "source": row.get('source', '').strip(),
            "id": row.get('Nr.', '').strip()
        }
        
        # Assign single primary category for filtering
        book['category'] = assign_category(book)
        
        books.append(book)

# Generate JSON
json_data = json.dumps(books, ensure_ascii=False, indent=2)
js_content = f"const libraryData = {json_data};\n"

with open(js_output_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"✅ Enhanced metadata for {len(books)} books.")
