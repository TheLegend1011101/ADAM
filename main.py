import sys
import os

from Module import text_abstract_ratio, text_rareness_score, compute_miop_chunks, analyze_text_orthographic_similarity
import re

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

    else:
        print(f"Error: Invalid function name: {function_name}")

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