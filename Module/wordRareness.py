from wordfreq import word_frequency
import re
import math

def calculate_word_rareness_wordfreq(word, lang='en'):

    frequency = word_frequency(word, lang)
    if frequency == 0:
        return 6
    else:
        rareness_score = 1 / frequency
        log_rareness = math.log10(rareness_score)
        scaled_score = min(6, max(0.1, (log_rareness / 8) * 6))
        return scaled_score

def text_rareness_score(text, lang='en'):

    words = sorted(set(re.findall(r'\b\w+\b', text.lower())))
    # Filter out purely numeric tokens
    words = [word for word in words if not word.isdigit()]
    rareness_scores = []

    for word in words:
        rareness = calculate_word_rareness_wordfreq(word, lang)
        rareness_scores.append((word, rareness))

    if rareness_scores:
        average_rareness = sum(score for _, score in rareness_scores) / len(rareness_scores)
        return average_rareness, rareness_scores
    else:
        return 0, rareness_scores


def plot_word_rareness_from_text(text, lang='en'):
    average_rareness, rareness_scores = text_rareness_score(text, lang)
    if not rareness_scores:
        print("No words found in text.")
        return

    import matplotlib.pyplot as plt
    import seaborn as sns

    scores = [score for _, score in rareness_scores]
    plt.figure(figsize=(8, 5))
    sns.histplot(scores, bins=10, kde=True, color='teal', edgecolor='black')

    plt.xlabel('Rareness Score (0.1–6)')
    plt.ylabel('Number of Words')
    plt.title(f'Distribution of Word Rareness (Avg: {average_rareness:.2f})')
    # plt.grid(True)
    plt.tight_layout()
    plt.show()