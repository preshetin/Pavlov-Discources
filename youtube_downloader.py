from yt_dlp import YoutubeDL
import sys

def download_youtube_audio(url, cookies_file=None):
    """
    Download YouTube video as MP3 using the video's title as filename
    Args:
        url: YouTube URL
        cookies_file: Path to cookies file (optional)
    """
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',  # Use video title as filename
    }

    # Add cookies if provided
    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Download the video
            ydl.download([url])
            print(f"Successfully downloaded audio from: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def batch_download_youtube_audio(links_md_path, cookies_file=None):
    """
    Download audio from a batch of YouTube links listed in a markdown file.
    Args:
        links_md_path: Path to the markdown file containing YouTube links (one per line)
        cookies_file: Path to cookies file (optional)
    """
    try:
        with open(links_md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # Extract links (ignore empty lines and lines not starting with http)
        links = [line.strip() for line in lines if line.strip().startswith('http')]
        if not links:
            print("No valid YouTube links found in the file.")
            return
        for url in links:
            print(f"Downloading: {url}")
            download_youtube_audio(url, cookies_file)
    except Exception as e:
        print(f"Error processing batch download: {str(e)}")

# Example: python youtube_downloader.py "https://youtu.be/example" "cookies.txt"
if __name__ == "__main__":
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        arg1 = sys.argv[1]
        cookies_file = sys.argv[2] if len(sys.argv) == 3 else None
        if arg1.endswith('.md'):
            batch_download_youtube_audio(arg1, cookies_file)
        else:
            download_youtube_audio(arg1, cookies_file)
    else:
        print("Usage:")
        print("  python youtube_downloader.py <youtube_url> [cookies_file]")
        print("  python youtube_downloader.py <links_md_file> [cookies_file]")
        sys.exit(1)