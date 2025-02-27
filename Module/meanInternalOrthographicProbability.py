import numpy as np
from collections import Counter
from nltk.util import ngrams

def compute_miop(text, chunk_size=125, debug=False):
    text = text.lower().replace(" ", "")
    trigrams = [''.join(tri) for tri in ngrams(text, 3)]
    trigram_counts = Counter(trigrams)
    
    if not trigram_counts or len(trigrams) == 1:
        return 0  

    total_trigrams = sum(trigram_counts.values())
    trigram_probs = {tri: count / total_trigrams for tri, count in trigram_counts.items()}

    if debug:
        print("Trigram Counts:", trigram_counts)
        print("Trigram Probabilities:", trigram_probs)

    miop_values = []

    for i in range(0, len(text) - chunk_size + 1, chunk_size // 4):
        chunk = text[i:i+chunk_size]
        chunk_trigrams = [''.join(tri) for tri in ngrams(chunk, 3)]

        if debug:
            print(f"\nChunk: {chunk}")
            print("Chunk Trigrams:", chunk_trigrams)

        if chunk_trigrams:
            chunk_probabilities = [trigram_probs.get(tri, 0) for tri in chunk_trigrams]
            miop_values.append(np.mean(chunk_probabilities))

    if len(trigrams) == 1:
        return 0

    return np.mean(miop_values) if miop_values else np.mean(list(trigram_probs.values()))

# words = ["banana", "bug", "abababab", "abcdefg", "asasa"]
# for word in words:
#     print(f"MIOP Score for '{word}': {compute_miop(word):.4f}")
