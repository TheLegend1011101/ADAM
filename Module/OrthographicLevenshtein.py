from fuzzywuzzy import fuzz
import multiprocessing

def process_word(word, unique_words, num_closest):
    similarities = [(other_word, fuzz.ratio(word, other_word)) for other_word in unique_words if other_word != word]
    if not similarities:
        return word, 3.0  # Max similarity if no other words
    sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    closest_words = [similarity for _, similarity in sorted_similarities[:num_closest]] #get the similarities only
    max_similarity = max(closest_words)
    scaled_similarity = 1.0 + (max_similarity / 100.0) * 2.0
    return word, scaled_similarity

def rate_text_orthographic_similarity_fuzzy_parallel(text, num_closest=20, num_processes=6):
    words = text.split()
    unique_words = set(words) # Use a set to store unique words.
    ratings = {}
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(process_word, [(word, unique_words, num_closest) for word in unique_words])
        ratings.update(dict(results))
    return ratings

# from fuzzywuzzy import fuzz
# import multiprocessing

# def process_word(word, other_words, num_closest):
#     similarities = [(other_word, fuzz.ratio(word, other_word)) for other_word in other_words]
#     sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
#     closest_words = [other_word for other_word, similarity in sorted_similarities[:num_closest]]
#     if not closest_words:
#         return word, 3.0  # Max similarity if no other words
#     average_similarity = float(sum(similarity for _, similarity in sorted_similarities[:num_closest])) / len(closest_words)

#     # Scale the average similarity to a 1-3 range with decimals
#     scaled_similarity = 1.0 + (average_similarity / 100.0) * 2.0
#     return word, scaled_similarity

# def rate_text_orthographic_similarity_fuzzy_parallel(text, num_closest=20, num_processes=5):
#     words = text.split()
#     ratings = {}
#     with multiprocessing.Pool(processes=num_processes) as pool:
#         results = pool.starmap(process_word, [(word, words[:i] + words[i+1:], num_closest) for i, word in enumerate(words)])
#         ratings.update(dict(results))
#     return ratings
# from fuzzywuzzy import fuzz
# import multiprocessing

# def process_word(word, other_words, num_closest):
#     similarities = [(other_word, fuzz.ratio(word, other_word)) for other_word in other_words]
#     sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
#     closest_words = [other_word for other_word, similarity in sorted_similarities[:num_closest]]
#     average_similarity = sum(similarity for _, similarity in sorted_similarities[:num_closest]) / len(closest_words) if closest_words else 100.0
#     return word, average_similarity

# def rate_text_orthographic_similarity_fuzzy_parallel(text, num_closest=20, num_processes=4): #added num_processes = 4
#     words = text.split()
#     ratings = {}
#     with multiprocessing.Pool(processes=num_processes) as pool: # added processes=num_processes
#         results = pool.starmap(process_word, [(word, words[:i] + words[i+1:], num_closest) for i, word in enumerate(words)])
#         ratings.update(dict(results))
#     return ratings

def rate_text_orthographic_similarity_fuzzy(text, num_closest=20):
    """
    Rates the orthographic similarity of each word in a text to its 20 closest words using FuzzyWuzzy.

    Args:
        text (str): The input text.
        num_closest (int): The number of closest words to consider (default: 20).

    Returns:
        dict: A dictionary where keys are words from the text and values are their orthographic similarity ratings.
    """
    words = text.split()
    ratings = {}

    for i, word in enumerate(words):
        other_words = words[:i] + words[i+1:]  # Exclude the word itself

        if not other_words:
            ratings[word] = 100.0 #max similarity

        else:
            similarities = [(other_word, fuzz.ratio(word, other_word)) for other_word in other_words]
            sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)  # Sort descending

            closest_words = [other_word for other_word, similarity in sorted_similarities[:num_closest]]
            average_similarity = sum(similarity for _, similarity in sorted_similarities[:num_closest]) / len(closest_words) if closest_words else 100.0

            ratings[word] = average_similarity

    return ratings

def orthographic_levenshtein(s1, s2, orthographic_map=None):
    """
    Calculates the orthographic Levenshtein distance between two strings.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.
        orthographic_map (dict, optional): A dictionary defining orthographic
                                            similarities. If None, only exact
                                            character matches have 0 cost.

    Returns:
        int: The orthographic Levenshtein distance.
    """

    def orthographic_cost(c1, c2, orthographic_map):
        if c1 == c2:
            return 0
        elif orthographic_map and c1 in orthographic_map and c2 in orthographic_map[c1]:
            return 0.5  # Orthographic similarity cost
        else:
            return 1

    len1 = len(s1)
    len2 = len(s2)

    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = orthographic_cost(s1[i - 1], s2[j - 1], orthographic_map)
            dp[i][j] = min(
                dp[i - 1][j] + 1,        # Deletion
                dp[i][j - 1] + 1,        # Insertion
                dp[i - 1][j - 1] + cost  # Substitution
            )

    return dp[len1][len2]

def rate_orthographic_similarity(word, similar_words, orthographic_map=None, max_distance=3):
    """Rates orthographic similarity on a linear scale."""
    if not similar_words:
        return 1.0

    distances = [orthographic_levenshtein(word, other_word, orthographic_map) for other_word in similar_words]
    average_distance = sum(distances) / len(distances)

    if average_distance >= max_distance:
        return 1.0
    elif average_distance <= 0:
        return 3.0
    else:
        return 3.0 - (2.0 * average_distance / max_distance)

def rate_text_orthographic_similarity_from_text(text, orthographic_map=None, max_distance=3, num_similar=20):
    """
    Rates the orthographic similarity of each word in a text to the other words in the text.

    Args:
        text (str): The input text.
        orthographic_map (dict, optional): A dictionary defining orthographic similarities.
        max_distance (int, optional): The maximum Levenshtein distance to scale to.
        num_similar (int, optional): The maximum number of similar words to consider.

    Returns:
        dict: A dictionary where keys are words from the text and values are their orthographic similarity ratings.
    """
    words = text.split()
    ratings = {}

    for i, word in enumerate(words):
        other_words = words[:i] + words[i+1:]

        if not other_words:
            ratings[word] = 3.0 

        else:
          distances = [(other_word, orthographic_levenshtein(word, other_word, orthographic_map)) for other_word in other_words]
          sorted_distances = sorted(distances, key=lambda x: x[1])
          similar_words = [other_word for other_word, distance in sorted_distances[:num_similar]]
          ratings[word] = rate_orthographic_similarity(word, similar_words, orthographic_map, max_distance)

    return ratings


