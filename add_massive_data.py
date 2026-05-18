import json
import urllib.request
import random
import os

url = "https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/master/dictionary_compact.json"
print("Downloading Webster's Dictionary JSON from GitHub...")
try:
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    print(f"Successfully downloaded {len(data)} words.")

    words = list(data.keys())
    # Sort to keep it somewhat deterministic, or just shuffle
    random.seed(42)
    random.shuffle(words)

    # Add 10,000 words! (Chala ekkuva!)
    selected_words = words[:10000]
    
    count = 0
    with open('dataset.txt', 'a', encoding='utf-8') as f:
        for word in selected_words:
            if not word.isalpha(): continue # Skip words with spaces/hyphens
            if len(word) < 3: continue # Skip very short words
            
            desc = data[word].replace('\n', ' ').replace('|', '').replace('"', '&quot;')
            
            # Format nicely with HTML
            html = f"<strong>{word.capitalize()}</strong><br><br>"
            html += f"<span style='color: var(--primary);'>Definition:</span> {desc}<br><br>"
            html += f"<span class='badge'>WEBSTER DICTIONARY EXPANSION</span>"
            
            f.write(f"{word.lower()}|{html}\n")
            count += 1

    print(f"Successfully appended {count} real dictionary definitions to dataset.txt!")
    
    # Also copy to dist folder to keep Netlify deploy in sync
    import shutil
    if os.path.exists('dist'):
        shutil.copy('dataset.txt', 'dist/dataset.txt')
        print("Copied updated dataset.txt to dist/ folder.")

except Exception as e:
    print(f"Error: {e}")
