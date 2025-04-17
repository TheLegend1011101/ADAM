import sys
import os
import re
from Module import text_abstract_ratio, text_rareness_score, compute_miop_chunks, analyze_text_orthographic_similarity,calculate_aoa,decoding_demand,count_sight_words,count_syllables_in_words,get_sentence_complexity,analyze_dependency_links

def clean_text(text):
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def process_file_content(filepath, function_name=None, output_dir="output"):
    """Processes file content using specified function or all functions and saves output."""

    if not os.path.isfile(filepath):
        print(f"Error: File not found: {filepath}")
        return

    print(f"Processing file: {filepath}")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            file_content = f.read()
            file_content = clean_text(file_content)
    except IOError:
        print(f"Error: Could not read file: {filepath}")
        return

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.splitext(os.path.basename(filepath))[0]

    if function_name is None or function_name == "all":
        with open(os.path.join(output_dir, f"{filename}_abstract.txt"), "w", encoding="utf-8") as f:
            f.write(f"Abstract Ratio: {str(text_abstract_ratio(file_content))}")
        with open(os.path.join(output_dir, f"{filename}_miop.txt"), "w", encoding="utf-8") as f:
            f.write(f"MIOP: {compute_miop_chunks(file_content)[1]}")
        with open(os.path.join(output_dir, f"{filename}_levenshtein.txt"), "w", encoding="utf-8") as f:
            orthographic_similarity = analyze_text_orthographic_similarity(file_content)
            f.write(f"Orthographic Levenshtein Distance: {orthographic_similarity[0]}\n")
            f.write(f"Mean Orthographic Levenshtein Distance: {orthographic_similarity[1]}")
        with open(os.path.join(output_dir, f"{filename}_rareness.txt"), "w", encoding="utf-8") as f:
            text_rareness = text_rareness_score(file_content)
            f.write(f"Average Rareness Score: {text_rareness[0]}")
            f.write(f"\nIndividual Rareness Scores: {text_rareness[1]}")
        with open(os.path.join(output_dir, f"{filename}_acquisition.txt"), "w", encoding="utf-8") as f:
            aoa_score = calculate_aoa(file_content)
            f.write(f"Average Age of Acquisition (AoA) for the passage: {aoa_score}")
        with open(os.path.join(output_dir, f"{filename}_decoding_demand.txt"), "w", encoding="utf-8") as f:
            decoding_demand_score = decoding_demand(file_content)[0]
            f.write(f"Decoding Demand: {decoding_demand_score}")
        with open(os.path.join(output_dir, f"{filename}_sight_word.txt"), "w", encoding="utf-8") as f:
            sight_word_count = count_sight_words(file_content)
            f.write(f"Number of Sight Words: {sight_word_count}")
        with open(os.path.join(output_dir, f"{filename}_syllable_count.txt"), "w", encoding="utf-8") as f:
            syllable_count = count_syllables_in_words(file_content)
            f.write(f"Total number of syllables in the text: {syllable_count}")
        with open(os.path.join(output_dir, f"{filename}_sentence_length.txt"), "w", encoding="utf-8") as f:
            mean_length = get_sentence_complexity(file_content)
            f.write(f"Mean number of letters and spaces: {mean_length:.2f}\n")
        with open(os.path.join(output_dir, f"{filename}_grammar.txt"), "w", encoding="utf-8") as f:
            mean_link = analyze_dependency_links(file_content)
            f.write(f"Mean Link Count: {mean_link:.2f}")

        print(f"Finished processing all functions for: {filepath}")

    elif function_name == "abstract":
        with open(os.path.join(output_dir, f"{filename}_abstract.txt"), "w", encoding="utf-8") as f:
            f.write(f"Abstract Ratio: {str(text_abstract_ratio(file_content))}")
        print(f"Finished abstract for: {filepath}")

    elif function_name == "miop":
        with open(os.path.join(output_dir, f"{filename}_miop.txt"), "w", encoding="utf-8") as f:
            f.write(f"MIOP: {compute_miop_chunks(file_content)[1]}")
        print(f"Finished miop for: {filepath}")

    elif function_name == "levenshtein":
        with open(os.path.join(output_dir, f"{filename}_levenshtein.txt"), "w", encoding="utf-8") as f:
            orthographic_similarity = analyze_text_orthographic_similarity(file_content)
            f.write(f"Orthographic Levenshtein Distance: {orthographic_similarity[0]}\n")
            f.write(f"Mean Orthographic Levenshtein Distance: {orthographic_similarity[1]}")
        print(f"Finished levenshtein for: {filepath}")

    elif function_name == "rareness":
        with open(os.path.join(output_dir, f"{filename}_rareness.txt"), "w", encoding="utf-8") as f:
            text_rareness = text_rareness_score(file_content)
            f.write(f"Average Rareness Score: {text_rareness[0]}")
            f.write(f"\nIndividual Rareness Scores: {text_rareness[1]}")
        print(f"Finished rareness for: {filepath}")

    elif function_name == "acquisition":
        with open(os.path.join(output_dir, f"{filename}_acquisition.txt"), "w", encoding="utf-8") as f:
            aoa_score = calculate_aoa(file_content)
            f.write(f"Average Age of Acquisition (AoA) for the passage: {aoa_score}")
        print(f"Finished acquisition for: {filepath}")

    elif function_name == "decoding_demand":
        with open(os.path.join(output_dir, f"{filename}_decoding_demand.txt"), "w", encoding="utf-8") as f:
            decoding_demand_score = decoding_demand(file_content)[0]
            f.write(f"Decoding Demand: {decoding_demand_score}")
        print(f"Finished decoding demand for: {filepath}")
    
    elif function_name == "sight_word":
        with open(os.path.join(output_dir, f"{filename}_sight_word.txt"), "w", encoding="utf-8") as f:
            sight_word_count = count_sight_words(file_content)
            f.write(f"Number of Sight Words: {sight_word_count}")
        print(f"Finished sight word for: {filepath}")
    
    elif function_name == "syllable_count":
        with open(os.path.join(output_dir, f"{filename}_syllable_count.txt"), "w", encoding="utf-8") as f:
            syllable_count = count_syllables_in_words(file_content)
            f.write(f"Total number of syllables in the text: {syllable_count}")
        print(f"Finished syllable count for: {filepath}")

    elif function_name == "sentence_length":
        with open(os.path.join(output_dir, f"{filename}_sentence_length.txt"), "w", encoding="utf-8") as f:
            mean_length = get_sentence_complexity(file_content)
            f.write(f"Mean number of letters and spaces: {mean_length:.2f}\n")
        print(f"Finished sentence length for: {filepath}")
    elif function_name == "grammar":
        with open(os.path.join(output_dir, f"{filename}_grammar.txt"), "w", encoding="utf-8") as f:
            mean_link = analyze_dependency_links(file_content)
            f.write(f"Mean Link Count: {mean_link:.2f}")
        print(f"Finished grammar for: {filepath}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <filepath> [function_name] [output_directory]")
        print("       function_name: abstract, miop, levenshtein, rareness, or all (default)")
        print("       output_directory: Directory to save output files (default: 'output')")
        sys.exit(1)

    filepath = sys.argv[1]
    function_name = sys.argv[2] if len(sys.argv) > 2 else "all"
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "output"

    process_file_content(filepath, function_name, output_dir)

# import sys
# import os
# import re
# import pandas as pd
# from Module import text_abstract_ratio, text_rareness_score, compute_miop_chunks, analyze_text_orthographic_similarity,calculate_aoa,decoding_demand,count_sight_words,count_syllables_in_words,get_sentence_complexity,analyze_dependency_links

# def clean_text(text):
#     # Remove punctuation
#     text = re.sub(r'[^\w\s]', '', text)
#     # Convert to lowercase
#     text = text.lower()
#     # Remove extra spaces
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# def process_passage(filepath):
#     """Processes a single passage and returns a dictionary of results."""
#     results = {}
#     try:
#         with open(filepath, "r", encoding="utf-8") as f:
#             file_content = f.read()
#             cleaned_content = clean_text(file_content)

#             results["abstract"] = text_abstract_ratio(cleaned_content)
#             results["miop"] = compute_miop_chunks(cleaned_content)[1]
#             orthographic = analyze_text_orthographic_similarity(cleaned_content)
#             results["levenshtein_dist"] = orthographic[0]
#             results["mean_levenshtein_dist"] = orthographic[1]
#             rareness = text_rareness_score(cleaned_content)
#             results["avg_rareness"] = rareness[0]
#             results["individual_rareness"] = rareness[1]
#             results["aoa"] = calculate_aoa(cleaned_content)
#             results["decoding_demand"] = decoding_demand(cleaned_content)[0]
#             results["sight_word_count"] = count_sight_words(cleaned_content)
#             results["syllable_count"] = count_syllables_in_words(cleaned_content)
#             results["sentence_length"] = get_sentence_complexity(cleaned_content)
#             results["grammar"] = analyze_dependency_links(cleaned_content) 
 
#     except IOError:
#         print(f"Error: Could not read file: {filepath}")
#         return None
#     return results

# def process_directory_to_dataframe(directory_path):
#     """Processes all text files in a directory and returns a Pandas DataFrame."""
#     all_results = {}
#     passage_files = sorted([f for f in os.listdir(directory_path) if f.endswith(".txt")])
#     data = {}
#     algorithms = ["abstract", "miop", "levenshtein_dist", "mean_levenshtein_dist", "avg_rareness", "aoa", "decoding_demand", "sight_word_count", "syllable_count", "sentence_length" , "grammar"]

#     for filename in passage_files:
#         filepath = os.path.join(directory_path, filename)
#         print(f"Processing: {filepath}")
#         results = process_passage(filepath)
#         if results:
#             passage_name = os.path.splitext(filename)[0]
#             data[passage_name] = {algo: results.get(algo) for algo in algorithms}

#     df = pd.DataFrame.from_dict(data, orient='index')
#     df.index.name = 'Passage'
#     return df

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print(f"Usage: python {sys.argv[0]} <directory_path_containing_text_files> [output_filename.csv (optional)]")
#         sys.exit(1)

#     directory_path = sys.argv[1]
#     if not os.path.isdir(directory_path):
#         print(f"Error: Invalid directory path: {directory_path}")
#         sys.exit(1)

#     df_output = process_directory_to_dataframe(directory_path)
#     print("\nDataFrame Output:")
#     print(df_output)

#     # Save the DataFrame to a CSV file
#     output_filename = "all_passages_analysis_book2.csv"  # Default filename
#     df_output.to_csv(output_filename)
    # if len(sys.argv) > 2:
    #     output_filename = sys.argv[2]

    # try:
    #     df_output.to_csv(output_filename, encoding='utf-8', index=True)
    #     print(f"\nDataFrame saved to: {output_filename}")
    # except Exception as e:
    #     print(f"Error saving DataFrame to CSV: {e}")