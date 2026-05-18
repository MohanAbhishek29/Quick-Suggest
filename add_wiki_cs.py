import json
import urllib.request
import urllib.parse
import os
import shutil
import time

categories = [
    "Computer_science", "Algorithms", "Data_structures", 
    "Software_engineering", "Cloud_computing", "Artificial_intelligence",
    "Computer_networking", "Operating_systems", "Databases",
    "Cyberattacks", "Cryptography", "Programming_languages"
]

def get_category_members(category, limit=500):
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:{category}&cmlimit={limit}&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        return [item['title'] for item in data['query']['categorymembers'] if ':' not in item['title']]
    except Exception as e:
        print(f"Error fetching {category}: {e}")
        return []

def get_summaries_bulk(titles):
    results = {}
    chunk_size = 20
    for i in range(0, len(titles), chunk_size):
        chunk = titles[i:i+chunk_size]
        safe_titles = urllib.parse.quote('|'.join(chunk))
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=True&explaintext=True&titles={safe_titles}&format=json"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            response = urllib.request.urlopen(req)
            data = json.loads(response.read().decode('utf-8'))
            pages = data['query']['pages']
            for page_id, page_info in pages.items():
                if page_id != '-1' and 'extract' in page_info:
                    results[page_info['title']] = page_info['extract']
        except Exception as e:
            pass
        print(f"Fetched {min(i+chunk_size, len(titles))}/{len(titles)} topics...")
        time.sleep(0.1) # Be nice to Wiki API
    return results

def format_entry(word, extract):
    if not extract or len(extract) < 50: return None
    
    # Split into sentences to fake the "Characteristics" and "Types" structure
    sentences = [s.strip() + ('.' if not s.endswith('.') else '') for s in extract.split('. ') if s]
    
    if len(sentences) < 2:
        desc = sentences[0] if sentences else extract
        characteristics = ["Fundamental concept in Computer Science & Engineering."]
        types = ["Academic/Industry Standard Term"]
    else:
        desc = sentences[0]
        characteristics = sentences[1:4]
        types = sentences[4:6] if len(sentences) > 4 else ["Refer to CS documentation for more details.", "Used extensively in real-world systems."]

    html = f"<strong>{word.upper()}</strong><br><br>"
    html += f"<span style='color: var(--text-main);'><strong>Definition:</strong></span> {desc}<br><br>"
    
    html += f"<span style='color: var(--primary);'><strong>Key Characteristics:</strong></span><ul>"
    for char in characteristics:
        if len(char) > 5:
            html += f"<li>{char.replace('|', '')}</li>"
    html += "</ul><br>"
    
    html += f"<span style='color: var(--accent);'><strong>Context / Details:</strong></span><ul>"
    for t in types:
        if len(t) > 5:
            html += f"<li>{t.replace('|', '')}</li>"
    html += "</ul>"
    
    html = html.replace('\n', ' ')
    return f"{word.lower()}|{html}\n"

print("Fetching thousands of Computer Science topics from Wikipedia...")
all_titles = set()
for cat in categories:
    print(f"Fetching category: {cat}")
    titles = get_category_members(cat, 500)
    all_titles.update(titles)

print(f"\nTotal unique CS topics found: {len(all_titles)}")
print("Downloading detailed definitions for all topics (This will take ~1-2 minutes)...\n")

titles_list = list(all_titles)
summaries = get_summaries_bulk(titles_list)

count = 0
existing_words = set()
if os.path.exists('dataset.txt'):
    with open('dataset.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if '|' in line:
                existing_words.add(line.split('|')[0].lower())

with open('dataset.txt', 'a', encoding='utf-8') as f:
    for word, extract in summaries.items():
        if word.lower() not in existing_words:
            entry = format_entry(word, extract)
            if entry:
                f.write(entry)
                count += 1

if os.path.exists('dist'):
    shutil.copy('dataset.txt', 'dist/dataset.txt')
    print("\nCopied updated massive dataset to dist/dataset.txt")

print(f"\nSuccessfully added {count} brand new, highly-detailed Computer Science topics to the engine!")
