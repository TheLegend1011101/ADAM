import numpy as np
import Levenshtein

def orthographic_levenshtein_similarity(word, text):

    words = text.lower().split()
    distances = []
    for other_word in words:
        if word != other_word:
            distances.append((other_word, Levenshtein.distance(word, other_word)))

    if len(distances) == 0:
        return 0, 0

    closest_words = sorted(distances, key=lambda x: x[1])[:20]

    if len(closest_words) == 0:
      return 0, 0

    mean_distance = np.mean([dist for _, dist in closest_words])


    if mean_distance == 0:
      scaled_distance = 3 
    else:
        scaled_distance = 1 + (2 * (1 / (1 + mean_distance))) 

    return mean_distance, scaled_distance

def analyze_text_orthographic_similarity(text):

    words = sorted(list(set(text.lower().split()))) 
    results = {}
    all_distances = []

    for word in words:
        mean_dist, similarity = orthographic_levenshtein_similarity(word, text)
        results[word] = {
            'mean_distance': mean_dist,
            'scaled_similarity': similarity
        }
        for other_word in words:
          if word != other_word:
            all_distances.append(Levenshtein.distance(word, other_word))

    overall_average_distance = np.mean(all_distances) if all_distances else 0

    return results, overall_average_distance





