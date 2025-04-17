import sys
import os
import json
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
    """Processes file content using requested functions and saves structured JSON output."""

    if not os.path.isfile(filepath):
        print(f"Error: File not found: {filepath}")
        return

    print(f"Processing file: {filepath}")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            file_content = clean_text(f.read())
    except IOError:
        print(f"Error: Could not read file: {filepath}")
        return

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.splitext(os.path.basename(filepath))[0]
    output_path = os.path.join(output_dir, f"{filename}_{function_name or 'all'}.json")

    results = {}

    def should_run(key):
        return function_name in [None, "all", key]

    if should_run("abstract"):
        results["abstract"] = text_abstract_ratio(file_content)

    if should_run("miop"):
        _, miop_score = compute_miop_chunks(file_content)
        results["miop"] = miop_score

    if should_run("levenshtein"):
        lev_distance, mean_distance = analyze_text_orthographic_similarity(file_content)
        results["levenshtein"] = {
            "Orthographic Levenshtein Distance": lev_distance,
            "Mean Orthographic Levenshtein Distance": mean_distance
        }

    if should_run("rareness"):
        avg_score, rareness_scores = text_rareness_score(file_content)
        results["rareness"] = {
            "Average Rareness Score": avg_score,
            "Individual Rareness Scores": [
                {"word": word, "score": score}
                for word, score in rareness_scores
            ]
        }

    if should_run("acquisition"):
        results["acquisition"] = calculate_aoa(file_content)

    if should_run("decoding_demand"):
        score, *_ = decoding_demand(file_content)
        results["decoding_demand"] = score

    if should_run("sight_word"):
        results["sight_word"] = count_sight_words(file_content)

    if should_run("syllable_count"):
        results["syllable_count"] = count_syllables_in_words(file_content)

    if should_run("sentence_lenght"):
        sentence_data, mean_length = get_sentence_complexity(file_content)
        results["sentence_lenght"] ={
            "mean_length": mean_length,
            "sentence_data": sentence_data
        }
        results["sentence_length"] = get_sentence_complexity(file_content)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Saved results to {output_path}")

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