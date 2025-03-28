# import os
# from Module import *
# file_content = None
# def process_file_content(content):
#     """Example processing function: Count words in the file."""
#     word_count = len(content.split())
#     print(f"Processing complete. Word count: {word_count}")

# def select_and_process_file():
#     """Prompt user for a file path, read its content, and process it."""
#     file_path = input("Enter the file path: ").strip()
    
#     if not os.path.isfile(file_path):
#         print("Error: File not found. Please try again.")
#         return

#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             file_content = file.read()  # Read file content
#             print("File loaded successfully.")
#             process_file_content(file_content)  # Auto-process the content
#     except Exception as e:
#         print(f"Error reading file: {e}")

# # Run the CLI
# if __name__ == "__main__":
#     while True:
#         command = input("Enter command (load/process/exit): ").strip().lower()
        
#         if command == "load":
#             select_and_process_file()
#         elif command == "process":
#             print("File is automatically processed upon loading.")
#         elif command == "exit":
#             print("Exiting program.")
#             break
#         elif command == "abstract_ratio":
#             print("The ratio of abstracts to the total number of articles is:")
#             print(text_abstract_ratio(file_content))
#         else:
#             print("Invalid command. Use 'load', 'process', or 'exit'.")


# import sys
# import os
# from Module import text_abstract_ratio, text_rareness_score, rate_text_orthographic_similarity_from_text, compute_miop_chunks
# # try:
# #     from my_functions import abstract, miop, levenshtein, rareness
# # except ImportError:
# #     print("Error: Could not import functions from my_functions.py. Make sure it exists and is in the same directory, or in your python path.")
# #     sys.exit(1)

# def process_file(filepath, function_name=None, output_dir="output"):
#     """Processes a single file using specified function or all functions and saves output."""

#     if not os.path.isfile(filepath):
#         print(f"Error: File not found: {filepath}")
#         return

#     print(f"Processing file: {filepath}")

#     # Create output directory if it doesn't exist
#     os.makedirs(output_dir, exist_ok=True)

#     filename = os.path.splitext(os.path.basename(filepath))[0]  # Get filename without extension

#     if function_name is None or function_name == "all":
#         with open(os.path.join(output_dir, f"{filename}_abstract.txt"), "w") as f:
#             f.write(text_abstract_ratio(filepath))
#         with open(os.path.join(output_dir, f"{filename}_miop.txt"), "w") as f:
#             f.write((filepath))
#         with open(os.path.join(output_dir, f"{filename}_levenshtein.txt"), "w") as f:
#             f.write(levenshtein(filepath))
#         with open(os.path.join(output_dir, f"{filename}_rareness.txt"), "w") as f:
#             f.write(rareness(filepath))
#         print(f"Finished processing all functions for: {filepath}")

#     elif function_name == "abstract":
#         with open(os.path.join(output_dir, f"{filename}_abstract.txt"), "w") as f:
#             f.write(abstract(filepath))
#         print(f"Finished abstract for: {filepath}")

#     elif function_name == "miop":
#         with open(os.path.join(output_dir, f"{filename}_miop.txt"), "w") as f:
#             f.write(miop(filepath))
#         print(f"Finished miop for: {filepath}")

#     elif function_name == "levenshtein":
#         with open(os.path.join(output_dir, f"{filename}_levenshtein.txt"), "w") as f:
#             f.write(levenshtein(filepath))
#         print(f"Finished levenshtein for: {filepath}")

#     elif function_name == "rareness":
#         with open(os.path.join(output_dir, f"{filename}_rareness.txt"), "w") as f:
#             f.write(rareness(filepath))
#         print(f"Finished rareness for: {filepath}")

#     else:
#         print(f"Error: Invalid function name: {function_name}")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print(f"Usage: python {sys.argv[0]} <filepath> [function_name] [output_directory]")
#         print("       function_name: abstract, miop, levenshtein, rareness, or all (default)")
#         print("       output_directory: Directory to save output files (default: 'output')")
#         sys.exit(1)

#     filepath = sys.argv[1]
#     function_name = sys.argv[2] if len(sys.argv) > 2 else "all"
#     output_dir = sys.argv[3] if len(sys.argv) > 3 else "output"

#     process_file(filepath, function_name, output_dir)


import sys
import os

from Module import text_abstract_ratio, text_rareness_score, rate_text_orthographic_similarity_fuzzy_parallel, rate_text_orthographic_similarity_from_text, compute_miop_chunks, rate_text_orthographic_similarity_fuzzy

def process_file_content(filepath, function_name=None, output_dir="output"):
    """Processes file content using specified function or all functions and saves output."""

    if not os.path.isfile(filepath):
        print(f"Error: File not found: {filepath}")
        return

    print(f"Processing file: {filepath}")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            file_content = f.read()
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
            f.write(f"Orthographic Levenshtein Distance: {rate_text_orthographic_similarity_from_text(file_content)}")
        with open(os.path.join(output_dir, f"{filename}_rareness.txt"), "w", encoding="utf-8") as f:
            f.write(f"Rareness Score: {text_rareness_score(file_content)}")
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
            f.write(f"Orthographic Levenshtein Distance: {rate_text_orthographic_similarity_fuzzy_parallel(file_content)}")
        print(f"Finished levenshtein for: {filepath}")

    elif function_name == "rareness":
        with open(os.path.join(output_dir, f"{filename}_rareness.txt"), "w", encoding="utf-8") as f:
            f.write(f"Rareness Score: {text_rareness_score(file_content)}")
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