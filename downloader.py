import os
import tempfile
from yt_dlp import YoutubeDL

def download_youtube_audio(url):
    """
    Download audio from YouTube and convert to MP3
    
    Args:
        url (str): YouTube video URL
    
    Returns:
        tuple: (file_path, title)
    """
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Configure yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        # Download and convert
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'audio')
            
            # Find the MP3 file
            mp3_file = None
            for file in os.listdir(temp_dir):
                if file.endswith('.mp3'):
                    mp3_file = os.path.join(temp_dir, file)
                    break
            
            if not mp3_file:
                raise Exception('MP3 file not found after conversion')
            
            return mp3_file, title
            
    except Exception as e:
        # Clean up temp files on error
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise Exception('Failed to download. Please check the URL and try again.')