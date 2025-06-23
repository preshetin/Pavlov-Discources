from openai import OpenAI
import os
import re
import time

# Set your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

# 'gpt-4' is too expensive.
# gpt-4o-mini $0.15 / 1m input tokens, $0.60 / 1m output tokens
MODEL_NAME = "gpt-4o-mini" 

# Known transcription errors and their corrections
CORRECTION_MAP = {
    "satie ботаны": "Сатипаттханы",
    "Гуда": "Будда",
    # Add more known errors here as needed
}

# Function to apply hardcoded corrections
def apply_known_corrections(text):
    for wrong, correct in CORRECTION_MAP.items():
        text = text.replace(wrong, correct)
    return text

# Function to split text into chunks with overlap
def split_into_chunks(text, chunk_size=500, overlap=0):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # Move forward, keeping overlap
    return chunks

# Function to correct text using OpenAI API
def correct_text_with_openai(text):
    system_prompt = (
        "You are an expert in Russian language and Buddhist terminology. "
        "Correct transcription errors in the following Russian text, ensuring "
        "proper spelling and terminology related to Buddha and Buddhist texts. "
        "Maintain the original meaning and context. "
        "For example, 'satie ботаны' should be 'Сатипаттханы', 'Гуда' should be 'Будда'. "
        "Also, the author users filler words like 'да', 'так сказать', 'то есть', 'ну', 'вот', etc. "
        "which should be removed. It should be nice to read the text. "
        "Split the result text into paragraphs. Return only the corrected text."
    )

    try:
        response = client.chat.completions.create(model=MODEL_NAME,  # Switch to "gpt-3.5-turbo" if preferred
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        max_tokens=1500,  # Adjust based on chunk size
        timeout=600,
        temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in API call: {e}")
        return text  # Return original text if API fails

# Function to split text into paragraphs
def split_into_paragraphs(text):
    # Split on double newlines or after sentence-ending punctuation with newline
    paragraphs = re.split(r'\n{2,}|\.\s*\n', text)
    # Clean up paragraphs and remove empty ones
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    return paragraphs

# Main function to process the file
def process_text_file(input_file, output_file):
    # Read the input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Apply known corrections first
    # text = apply_known_corrections(text)

    # Split text into chunks
    chunks = split_into_chunks(text)

    # Process each chunk with OpenAI API
    corrected_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)}...")
        corrected_chunk = correct_text_with_openai(chunk)
        corrected_chunks.append(corrected_chunk)
        time.sleep(1)  # Avoid rate limits

    # Reassemble corrected text
    corrected_text = " ".join(corrected_chunks)

    # Split into paragraphs
    # paragraphs = split_into_paragraphs(corrected_text)

    # Save to output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(corrected_text + "\n\n")
        print(f"Corrected text saved to {output_file}")
    except Exception as e:
        print(f"Error writing file: {e}")

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python build_result.py <folder_path>")
        sys.exit(1)
        
    folder_path = sys.argv[1]
    
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a directory")
        sys.exit(1)
    
    # Process all txt files in the folder
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    
    if not txt_files:
        print(f"No .txt files found in {folder_path}")
        sys.exit(0)
    
    print(f"Found {len(txt_files)} .txt files to process")
    
    for txt_file in txt_files:
        input_file = os.path.join(folder_path, txt_file)
        output_file = os.path.join(folder_path, f"{MODEL_NAME}_{txt_file}")
        
        print(f"\nProcessing: {txt_file}")
        process_text_file(input_file, output_file)