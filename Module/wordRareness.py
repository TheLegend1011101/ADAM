from wordfreq import word_frequency

def calculate_word_rareness_wordfreq(word, lang='en'):

    frequency = word_frequency(word, lang)
    if frequency == 0:
        return float('inf') 
    else:
        rareness_score = 1 / frequency
        scaled_score = min(6, 0.10 + (rareness_score / 1000000)) 
        return scaled_score

def text_rareness_score(text, lang='en'):

    words = text.split()
    rareness_scores = []
    valid_rareness_values = []

    for word in words:
        rareness = calculate_word_rareness_wordfreq(word, lang)
        rareness_scores.append((word, rareness)) 
        if rareness != float('inf'):
            valid_rareness_values.append(rareness)

    if valid_rareness_values:
        average_rareness = sum(valid_rareness_values) / len(valid_rareness_values)
        return average_rareness, rareness_scores
    else:
        return 0, rareness_scores

