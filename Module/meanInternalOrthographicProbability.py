import re
from collections import defaultdict
from nltk import ngrams

def calculate_orthographic_predictability(text, chunk_size=125):
    cleaned_text = re.sub(r'[^a-zA-Z]', '', text.lower())
    

    chunks = [cleaned_text[i:i+chunk_size] for i in range(0, len(cleaned_text), chunk_size)]
    chunks = [chunk for chunk in chunks if len(chunk) >= 3]  # Filter small chunks
    
    if not chunks:
        return 0.0, []
    

    global_trigram_counts = defaultdict(int)
    for chunk in chunks:
        for trigram in ngrams(chunk, 3):
            global_trigram_counts[trigram] += 1
    

    global_repeated = 0
    global_total = 0
    chunk_scores = []
    
    for chunk in chunks:
        chunk_trigrams = list(ngrams(chunk, 3))
        unique_trigrams = set(chunk_trigrams)
        

        chunk_repeated = sum(1 for t in unique_trigrams if global_trigram_counts[t] > 1)
        chunk_total = len(chunk_trigrams)
        

        chunk_miop = chunk_repeated / chunk_total if chunk_total > 0 else 0.0
        chunk_scores.append(chunk_miop)
        

        global_repeated += chunk_repeated
        global_total += chunk_total
    
    global_miop = global_repeated / global_total if global_total > 0 else 0.0
    
    return global_miop, chunk_scores

