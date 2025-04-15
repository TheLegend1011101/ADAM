import spacy

def load_model(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    link_count = []

    for sent in doc.sents:
        unique_links = set()
        for token in sent:
            if token.dep_:  # Include all dependency types
                unique_links.add(token.dep_)
        
        link_count.append(len(unique_links))

    mean_link_count = sum(link_count) / len(link_count) if link_count else 0

    return mean_link_count

# try:
#     with open("Passage1.txt", "r") as f:
#         text = f.read()
# except FileNotFoundError:
#     print("File not found")
#     exit()

# mean_link = load_model(text)
# print(f"Mean Link Count: {mean_link:.2f}")