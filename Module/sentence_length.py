import re
import numpy as np

# try:
#     with open("Passage1.txt", "r") as f:
#         text = f.read()
# except FileNotFoundError:
#     print("File not found")
#     exit()


def get_sentence_complexity(text):
    
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if s.strip()]  
    
    sentence_data = []
    char_counts = []  

    for sentence in sentences:
        num_chars = len(sentence)  
        words = sentence.split()
        num_words = len(words)  
        unique_words = len(set(words))  
        num_phrases = len(re.split(r'[,:;]', sentence))  
        
        char_counts.append(num_chars)

        sentence_data.append({
            "sentence": sentence,
            "num_chars": num_chars,
            "num_words": num_words,
            "unique_words": unique_words,
            "num_phrases": num_phrases
        })

    mean_chars = np.mean(char_counts) if char_counts else 0


    for data in sentence_data:
        data["complexity_score"] = 1 if data["num_chars"] < mean_chars else 1.5  

    return mean_chars
