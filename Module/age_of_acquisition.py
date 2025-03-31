import nltk
import pandas as pd
from nltk.tokenize import word_tokenize

# Load AoA data
aoa_df = pd.read_giexcel('data/AoA_51715_words.xlsx')

# Keep only relevant columns
aoa_df = aoa_df[['Word', 'AoA_Kup_lem']]
# print("Size of AoA dataframe: ", aoa_df.shape)

# Create AoA lookup dictionary
aoa_directory = {}

for _, row in aoa_df.iterrows():
    word = row['Word']
    
    if isinstance(word, str) and pd.notna(row['AoA_Kup_lem']):
        word = word.lower()
        aoa_directory[word] = row['AoA_Kup_lem'] 

# Load passage
# try:
#     with open("Passage1.txt", "r") as f:
#         data = f.read()
# except FileNotFoundError:
#     print("File not found")
#     exit()

# Calculate AoA for a passage
def calculate_aoa(text, aoa_directory):
    tokens = word_tokenize(text.lower())  
    #print("Number of words in AoA directory:", len(aoa_directory))  
    
    total_aoa = 0  
    count = 0  
    
    for word in tokens:
        if word in aoa_directory:
            #print(f"Found: {word} → {aoa_directory[word]}") 
            total_aoa += aoa_directory[word]  # Add AoA score
            count += 1  # Increment count
    
    if count == 0:
        return None  
    
    return total_aoa / count  # Compute the average AoA

# Compute AoA for passage
# aoa_score = calculate_aoa(data, aoa_directory)

# print(f"Average Age of Acquisition (AoA) for the passage: {aoa_score}")