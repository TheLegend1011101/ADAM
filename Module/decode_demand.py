import re
import syllapy

high_freq_words = {"the", "of", "and", "a", "to", "in", "is", "you", "that", "it", "he", "was", "for", "on", "are",
                   "as", "with", "his", "they", "I", "at", "be", "this", "have", "from", "or", "one", "had", "by"}


def count_syllables(word):
    return syllapy.count(word)
   
# Compute decoding demand of words in a text
def decoding_demand(text):
    words = re.findall(r"\b[a-zA-Z']+\b", text.lower())  # Tokenize words
    total_demand = 0
    word_scores = {}

    for word in words:
        score = 0
        word_length = len(word)

        if word_length <= 4:
            score += 1
        elif word_length <= 6:
            score += 2
        else:
            score += 3

        score += max(0, count_syllables(word) - 1)

        if word in high_freq_words:
            score -= 1

        if re.search(r"(ph|ough|tion|tious|ious|gue)", word):
            score += 1

        word_scores[word] = score
        total_demand += score

    return total_demand, word_scores


