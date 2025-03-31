import csv
import re



# try:
#     with open("Passage1.txt", "r") as f:
#         data = f.read()
# except FileNotFoundError:
#     print("File not found")
#     exit()


sight_words = []
try:
    with open("data/sight_words.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            sight_words.append(row[0].strip().lower()) 
except FileNotFoundError:
    print("Sight words CSV file not found")
    exit()


def count_sight_words(text, sight_words):
    words = re.findall(r'\b\w+\b', text.lower())  
    for word in words:
        if word in sight_words:
            sight_word_count = sight_word_count + 1
    return sight_word_count


#num_sight_words = count_sight_words(data, sight_words)

# Print results
# print("\nResults:")
# print(f"Number of Sight Words: {num_sight_words}")