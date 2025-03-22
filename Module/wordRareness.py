import nltk
import math
import re
import numpy as np
from wordfreq import word_frequency

# Download the necessary NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')


def strip_character(a_string):
    r = re.compile(r"[^a-zA-Z- ]")
    return r.sub(' ', a_string)

def remove_spaces(a_string):
    return re.sub(' +', ' ', a_string)

def remove_apos_s(a_string):
    return re.sub("'s", '', a_string)

def clean_input_text(input_text):
    # convert input to lowercase
    input_text = input_text.lower()
    # remove apostrophe-s from words
    input_text = remove_apos_s(input_text)
    # strip non-essential characters
    input_text = strip_character(input_text)
    # remove internal spaces
    input_text = remove_spaces(input_text)
    # remove end spaces
    input_text = input_text.strip()
    return input_text



def wordRareness(word, min_frequency = 1e-8):
    """
    Calculate the rareness of a word using the wordfreq library.
    
    Parameters:
    word (str): The word to check.
    
    Returns:
    float: The rareness score of the word.
    """
    
    word = word.lower()  # Convert word to lowercase
    
    # Get the frequency of the word in the English corpus
    frequency = word_frequency(word, 'en')
    frequency = max(frequency, min_frequency)  
    
    rareness_score = 1/frequency 
    
    return rareness_score
print(wordRareness("xzyqz"))
def text_rareness_score(text):
    """
    Calculates the overall rareness and complexity score of a given text.
    
    Parameters:
    text (str): The input text.
    
    Returns:
    float: A score in the range of 0.10 to 6 representing the rareness/complexity of the text.
    """
    # Tokenize the text into words
    text = clean_input_text(text)
    words = nltk.word_tokenize(text)
    
    # Calculate the rareness score for each word
    rareness_scores = [wordRareness(word) for word in words]
    
    # Calculate the average rareness score for the text
    average_rareness = np.mean(rareness_scores)
    
    # Normalize the score to be between 0.10 and 6, where 6 is the rarest
    min_rareness = 0.10
    max_rareness = 6.0
    
    # Calculate the max and min possible rareness from the list of scores
    min_rareness_score = min(rareness_scores)
    max_rareness_score = max(rareness_scores)
    
    # Scale the average score between the desired range
    # normalized_score = min_rareness + (max_rareness - min_rareness) * (average_rareness / 100)  # Adjust the divisor
    normalized_score = (average_rareness-min_rareness_score)/(max_rareness_score-min_rareness_score)
    
    return normalized_score

# Example usage:
text = "thout wight thout thout thout thout thout thout thout Uhtceare."
rareness_score = text_rareness_score(text)
print(f"Rareness/Complexity score of the text: {rareness_score}")
