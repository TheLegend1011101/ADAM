import csv
import re
from pathlib import Path
model_path = Path(__file__).resolve().parent.parent / "data" / "sight_words.csv"
if not model_path.exists(): 
    raise FileNotFoundError(f"Model file not found at {model_path}")
# Open and read the CSV file containing sight words
sight_words = []
try:
    with open(model_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            sight_words.append(row[0].strip().lower())  # Add sight word to the list (strip and convert to lowercase)
except FileNotFoundError:
    print("Sight words CSV file not found")
    exit()


def count_sight_words(text):
    sight_word_count = 0 
    words = re.findall(r'\b\w+\b', text.lower())  
    for word in words:
        if word in sight_words:
            sight_word_count = sight_word_count + 1
    return sight_word_count


