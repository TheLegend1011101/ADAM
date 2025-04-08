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

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from nltk.util import ngrams

def compute_miop_chunks(text, chunk_size=125, debug=False):
    text = text.lower().replace(" ", "")
    trigrams = [''.join(tri) for tri in ngrams(text, 3)]
    trigram_counts = Counter(trigrams)
    
    if not trigram_counts or len(trigrams) == 1:
        return [], 0

    total_trigrams = sum(trigram_counts.values())
    trigram_probs = {tri: count / total_trigrams for tri, count in trigram_counts.items()}

    miop_values = []

    # Iterate over chunks (with overlap)
    for i in range(0, len(text) - chunk_size + 1, chunk_size // 4):
        chunk = text[i:i+chunk_size]
        chunk_trigrams = [''.join(tri) for tri in ngrams(chunk, 3)]
        if chunk_trigrams:
            chunk_probabilities = [trigram_probs.get(tri, 0) for tri in chunk_trigrams]
            miop_values.append(np.mean(chunk_probabilities))

    overall_miop = np.mean(miop_values) if miop_values else np.mean(list(trigram_probs.values()))
    return miop_values, overall_miop

def plot_miop_across_chunks(text, chunk_size=125):
    miop_values, overall_miop = compute_miop_chunks(text, chunk_size)

    plt.figure(figsize=(12, 6))
    plt.plot(range(1, len(miop_values) + 1), miop_values, marker='o', linestyle='-', color='teal', label='Chunk MIOP')
    plt.axhline(y=overall_miop, color='r', linestyle='--', label=f'Overall MIOP: {overall_miop:.4f}')
    plt.xlabel('Chunk Number')
    plt.ylabel('MIOP')
    plt.title('MIOP Across Text Chunks for Republic Reader Passage')
    plt.legend()
    plt.grid(True)
    plt.show()


