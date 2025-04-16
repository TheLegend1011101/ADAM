from wordfreq import word_frequency
import re
import math

def calculate_word_rareness_wordfreq(word, lang='en'):

    frequency = word_frequency(word, lang)
    if frequency == 0:
        return 6
    else:
        rareness_score = 1 / frequency
        rareness_score = 1 / frequency
        log_rareness = math.log10(rareness_score)
        scaled_score = min(6, max(0.1, (log_rareness / 8) * 6))
        return scaled_score

def text_rareness_score(text, lang='en'):

    words = sorted(set(re.findall(r'\b\w+\b', text.lower())))
    rareness_scores = []

    for word in words:
        rareness = calculate_word_rareness_wordfreq(word, lang)
        rareness_scores.append((word, rareness))

    if rareness_scores:
        average_rareness = sum(score for _, score in rareness_scores) / len(rareness_scores)
        return average_rareness, rareness_scores
    else:
        return 0, rareness_scores

