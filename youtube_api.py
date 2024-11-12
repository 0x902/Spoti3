# youtube_api.py
from pytubefix import YouTube, Search
from pytubefix.cli import on_progress

def search_youtube(title, artist):
    results = Search(f"{title} by {artist}").videos
    if results:
        return results[0].watch_url, results[0].title
    else:
        return None, None

def download_mp3(url, folder, filename):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        ys = yt.streams.get_audio_only()
        ys.download(output_path=folder, filename=filename)
        return True, f"Downloaded: {filename}"
    except Exception as e:
        return False, f"Error downloading {filename}: {e}"
