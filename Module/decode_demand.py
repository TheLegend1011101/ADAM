import re
import syllapy

high_freq_words = {"the", "of", "and", "a", "to", "in", "is", "you", "that", "it", "he", "was", "for", "on", "are",
                   "as", "with", "his", "they", "I", "at", "be", "this", "have", "from", "or", "one", "had", "by"}

try:
    with open("Passage1.txt", "r") as f:
        data = f.read()
except FileNotFoundError:
    print("File not found")
    exit()

print("Passage content:\n")
#print(data)


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

        # Word length factor
        if word_length <= 4:
            score += 1
        elif word_length <= 6:
            score += 2
        else:
            score += 3

        # Syllable factor
        score += max(0, count_syllables(word) - 1)

        # High-frequency word adjustment
        if word in high_freq_words:
            score -= 1

        # Complex letter sequences
        if re.search(r"(ph|ough|tion|tious|ious|gue)", word):
            score += 1

        word_scores[word] = score
        total_demand += score

    return total_demand, word_scores

text = "The explanation of phonetic syllables in comprehension is quite difficult."
total_score, word_demand = decoding_demand(text)

print(f"Total Decoding Demand: {total_score}")
print("Word-wise Decoding Scores:", word_demand)
