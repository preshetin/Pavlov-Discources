import openai
import os
import re
import time

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_KEY")  # Ensure OPENAI_KEY is set in your environment

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
def split_into_chunks(text, chunk_size=500, overlap=50):
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
    prompt = (
        "You are an expert in Russian language and Buddhist terminology. Correct transcription errors in the following Russian text, ensuring proper spelling and terminology related to Buddha and Buddhist texts. Maintain the original meaning and context. For example, 'satie ботаны' should be 'Сатипаттханы', 'Гуда' should be 'Будда'. Return only the corrected text.\n\n"
        f"Text:\n{text}"
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Switch to "gpt-3.5-turbo" if preferred
            messages=[
                {"role": "system", "content": "You are a precise text corrector."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,  # Adjust based on chunk size
            temperature=0.3  # Low temperature for precise corrections
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
    text = apply_known_corrections(text)

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
    paragraphs = split_into_paragraphs(corrected_text)

    # Save to output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for para in paragraphs:
                f.write(para + "\n\n")
        print(f"Corrected text saved to {output_file}")
    except Exception as e:
        print(f"Error writing file: {e}")

# Example usage
input_file = "input_russian_text.txt"  # Replace with your input file path
output_file = "corrected_russian_text.txt"  # Output file path
process_text_file(input_file, output_file)