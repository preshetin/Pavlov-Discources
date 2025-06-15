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

# Example: python youtube_downloader.py "https://youtu.be/example" "cookies.txt"
if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python youtube_downloader.py <youtube_url> [cookies_file]")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    cookies_file = sys.argv[2] if len(sys.argv) == 3 else None
    download_youtube_audio(youtube_url, cookies_file)