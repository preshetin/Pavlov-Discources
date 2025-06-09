import os
import argparse

def count_words(filename):
    """Counts the number of words in a text file.

    Args:
        filename (str): The name of the text file.

    Returns:
        int: The number of words in the file.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            words = text.split()
            return len(words)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# usage:
# python count_words.py "./audio-files/test/sample.txt" 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Count words in a text file.')
    parser.add_argument('filepath', type=str, help='Path to the text file')
    args = parser.parse_args()
    
    word_count = count_words(args.filepath)
    if word_count is not None:
        print(f"The file '{args.filepath}' contains {word_count} words.")