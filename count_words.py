import os

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

if __name__ == "__main__":
    filename = "updated.txt"  # Replace with the actual filename if different
    word_count = count_words(filename)
    if word_count is not None:
        print(f"The file '{filename}' contains {word_count} words.")