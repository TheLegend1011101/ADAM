import spacy

def analyze_dependency_links(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    all_sentence_data = []  # To store sentence-level details
    link_counts = []        # To store number of unique links per sentence

    for i, sent in enumerate(doc.sents, 1):
        unique_links = set()
        for token in sent:
            if token.dep_:
                unique_links.add(token.dep_)
        
        link_counts.append(len(unique_links))
        
        all_sentence_data.append({
            "sentence_number": i,
            "sentence_text": sent.text.strip(),
            "unique_dependencies": unique_links,
            "count": len(unique_links)
        })

    mean_link_count = sum(link_counts) / len(link_counts) if link_counts else 0

    # Print breakdown
    # for data in all_sentence_data:
    #     print(f"Sentence {data['sentence_number']}: {data['sentence_text']}")
    #     print(f"Unique Dependencies ({data['count']}): {sorted(data['unique_dependencies'])}\n")

    # print(f"Overall Mean Link Count: {mean_link_count:.2f}")
    return mean_link_count


