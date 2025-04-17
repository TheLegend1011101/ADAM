# import re
# import syllapy

# high_freq_words = {"the", "of", "and", "a", "to", "in", "is", "you", "that", "it", "he", "was", "for", "on", "are",
#                     "as", "with", "his", "they", "I", "at", "be", "this", "have", "from", "or", "one", "had", "by"}

# def count_syllables(word):
#     return syllapy.count(word)


# def decoding_demand(text):
#     words = re.findall(r"\b[a-zA-Z']+\b", text.lower()) 
#     total_demand = 0
#     word_scores = {}

#     for word in words:
#         score = 0
#         word_length = len(word)

#         if word_length <= 4:
#             score += 1
#         elif word_length <= 6:
#             score += 2
#         else:
#             score += 7

#         score += max(0, count_syllables(word) - 1)

#         if word in high_freq_words:
#             score -= 1

#         if re.search(r"(ph|ough|tion|tious|ious|gue)", word):
#             score += 1

#         word_scores[word] = score
#         total_demand += score
#         mean_demand = total_demand / len(words)
#         percentage_demand = (mean_demand / 9) * 100

#     return percentage_demand,mean_demand, 




import re
import syllapy

# 50 most frequent English words (stoplist)
high_freq_words = {
    "the", "of", "and", "a", "to", "in", "is", "you", "that", "it", "he", "was", "for", "on", "are",
    "as", "with", "his", "they", "i", "at", "be", "this", "have", "from", "or", "one", "had", "by"
}

def count_syllables(word):
    return syllapy.count(word)

def decoding_demand(text):
    words = re.findall(r"\b[a-zA-Z']+\b", text.lower())  # Tokenize words
    total_demand = 0
    word_scores = {}

    for word in words:
        score = 0
        word_length = len(word)

        # Adjusted length-based scoring
        if word_length <= 4:
            score += 1
        elif word_length <= 6:
            score += 3
        else:
            score += 4

        # Multisyllabic boost
        syllable_count = count_syllables(word)
        if syllable_count > 1:
            score += (syllable_count - 1) * 2

        # Slight reduction for high-frequency words
        if word in high_freq_words:
            score -= 0.5

        # Add complexity points for tricky graphemes
        if re.search(r"(ph|ough|tion|tious|ious|gue)", word):
            score += 2

        # Ensure no negative scores
        score = max(score, 0)

        word_scores[word] = score
        total_demand += score

    mean_demand = total_demand / len(words)
    percentage_demand = (mean_demand / 9) * 100

    return percentage_demand, mean_demand, word_scores
