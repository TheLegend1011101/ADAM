# import re
# import syllapy

# high_freq_words = {"the", "of", "and", "a", "to", "in", "is", "you", "that", "it", "he", "was", "for", "on", "are",
#                    "as", "with", "his", "they", "I", "at", "be", "this", "have", "from", "or", "one", "had", "by"}


# def count_syllables(word):
#     return syllapy.count(word)
   
# # Compute decoding demand of words in a text
# def decoding_demand(text):
#     words = re.findall(r"\b[a-zA-Z']+\b", text.lower())  # Tokenize words
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
#             score += 3

#         score += max(0, count_syllables(word) - 1)

#         if word in high_freq_words:
#             score -= 1

#         if re.search(r"(ph|ough|tion|tious|ious|gue)", word):
#             score += 1

#         word_scores[word] = score
#         total_demand += score

#     return total_demand, word_scores



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
        mean_demand = total_demand / len(words)
        percentage_demand = (mean_demand / 9) * 100

    return percentage_demand,mean_demand, 


# Assuming the scale is roughly 1 (least complex) to a theoretical maximum
# based on the highest possible score a word could get.
# Let's consider a very long word with many syllables and complex features.
# For example, a 10+ letter word (score 3), with 5 syllables (+4), not high-frequency,
# and containing a complex pattern (+1) would be 3 + 4 + 1 = 8.
# Given your scale goes to 9, let's use that as a rough maximum per "unit" of word.

# Standardize the mean demand to a percentage of the maximum scale (9)
# percentage_demand = (mean_demand / 9) * 100

# print(f"Total Decoding Demand: {total_demand}")
# print(f"Total Number of Words: {len(words)}")
# print(f"Mean Decoding Demand: {mean_demand:.2f}")
# print(f"Standardized Decoding Demand (as a percentage of 9): {percentage_demand:.2f}%")


