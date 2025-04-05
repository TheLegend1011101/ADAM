import re
import syllapy


def count_syllables(word):
    return syllapy.count(word)

def count_syllables_in_words(text):

    words = re.findall(r"\b[a-zA-Z']+\b", text.lower()) 
    total_syllables = 0

    for word in words :
        syllable_count = syllapy.count(word)
        total_syllables += syllable_count
    return total_syllables


