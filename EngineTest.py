import os
import subprocess
import yt_dlp as youtube_dl
import whisper
from pymongo import MongoClient

# MongoDB configuration
MONGO_URI = "mongodb+srv://saksham:11008712@sforsearch.fcv6ck5.mongodb.net/?retryWrites=true&w=majority&appName=sforsearch"
DB_NAME = "youtube_transcriptions"
COLLECTION_NAME = "transcriptions"

# YouTube channel URL
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/@AcquiredFM"

# Directory to save downloaded videos
DOWNLOAD_DIR = "/Users/sakshampoply/Downloads/SearchEngineApp/Downloads"

# Create download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# YouTube download options
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
}


def download_videos(channel_url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([channel_url])


def transcribe_video(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    return result["text"]


def save_transcription_to_mongo(video_title, transcription):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    document = {"title": video_title, "transcription": transcription}
    collection.insert_one(document)


def process_videos():
    for video_file in os.listdir(DOWNLOAD_DIR):
        if video_file.endswith((".mp4", ".mkv", ".webm")):
            video_path = os.path.join(DOWNLOAD_DIR, video_file)
            print(f"Transcribing video: {video_file}")
            transcription = transcribe_video(video_path)
            save_transcription_to_mongo(video_file, transcription)
            print(f"Saved transcription for: {video_file}")


if __name__ == "__main__":
    print("Downloading videos from channel...")
    download_videos(YOUTUBE_CHANNEL_URL)
    print("Download complete. Starting transcription...")
    process_videos()
    print("Transcription process complete.")
