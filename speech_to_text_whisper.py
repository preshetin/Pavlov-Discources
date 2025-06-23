import whisper
import os
import sys

def speech_to_text(audio_file):
    """
    Converts speech from an audio file to text using Whisper API and saves the transcript to a text file.

    Args:
        audio_file (str): Path to the audio file (mp3).
    """
    try:
        # Load the Whisper model
        model = whisper.load_model("base")  # You can choose different model sizes like "tiny", "base", "small", "medium", "large"

        # Transcribe the audio
        print(f"Transcribing {audio_file}...")
        result = model.transcribe(audio_file, fp16=False, language="ru")
        transcript = result["text"]

        # Create the text file path
        text_file = os.path.splitext(audio_file)[0] + ".txt"

        # Save the transcript to the text file
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(transcript)

        print(f"Transcription saved to {text_file}\n")

    except Exception as e:
        print(f"Error processing {audio_file}: {e}")

def process_directory(directory):
    """
    Processes all mp3 files in a directory.

    Args:
        directory (str): Path to the directory containing the mp3 files.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            audio_file = os.path.join(directory, filename)
            speech_to_text(audio_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python speech_to_text_whisper.py <audio_directory>")
        sys.exit(1)
    audio_directory = sys.argv[1]
    process_directory(audio_directory)
    print("Finished processing all files.")