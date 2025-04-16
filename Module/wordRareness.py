from wordfreq import word_frequency
import re

def calculate_word_rareness_wordfreq(word, lang='en'):

    frequency = word_frequency(word, lang)
    if frequency == 0:
        return 6
    else:
        rareness_score = 1 / frequency
        scaled_score = min(6, 0.10 + (rareness_score / 1000000)) 
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
