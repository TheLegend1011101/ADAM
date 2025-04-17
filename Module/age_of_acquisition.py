import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from pathlib import Path


model_path = Path(__file__).resolve().parent.parent / "data" / "AoA_51715_words.xlsx"
if not model_path.exists():
    raise FileNotFoundError(f"Model file not found at {model_path}")
    exit()
aoa_df = pd.read_excel(model_path)
if aoa_df.empty:
    raise ValueError("AoA data is empty")

aoa_df = aoa_df[['Word', 'AoA_Kup_lem']]


aoa_directory = {}

for _, row in aoa_df.iterrows():
    word = row['Word']
    
    if isinstance(word, str) and pd.notna(row['AoA_Kup_lem']):
        word = word.lower()
        aoa_directory[word] = row['AoA_Kup_lem'] 

def calculate_aoa(text):
    tokens = word_tokenize(text.lower())  
    
    
    total_aoa = 0  
    count = 0  
    
    for word in tokens:
        if word in aoa_directory:
            total_aoa += aoa_directory[word]  
            count += 1  
    
    if count == 0:
        return None  
    
    return total_aoa / count  

