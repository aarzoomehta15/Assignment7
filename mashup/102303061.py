import sys
import os
from pydub import AudioSegment
import yt_dlp
import static_ffmpeg

static_ffmpeg.add_paths()

DOWNLOAD_DIR = "downloads"


def validate_args():
    if len(sys.argv) != 5:
        print("Usage:")
        print("python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]

    try:
        n = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        sys.exit("NumberOfVideos and AudioDuration must be integers")

    output = sys.argv[4]

    if n <= 10:
        sys.exit("NumberOfVideos must be greater than 10")

    if duration <= 20:
        sys.exit("AudioDuration must be greater than 20 seconds")

    return singer, n, duration, output


def download_audios(singer, n):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": False,
        "ignoreerrors": True,

        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        },
        "user_agent": "com.google.android.youtube/17.31.35",

        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    query = f"ytsearch{n}:{singer} song"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])


def trim_audios(duration):
    trimmed = []

    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith(".mp3") and "_cut" not in file:
            path = os.path.join(DOWNLOAD_DIR, file)
            audio = AudioSegment.from_mp3(path)

            cut_audio = audio[:duration * 1000]
            new_path = path.replace(".mp3", "_cut.mp3")
            cut_audio.export(new_path, format="mp3")

            trimmed.append(new_path)

    if not trimmed:
        sys.exit("No audio files were processed")

    return trimmed


def merge_audios(files, output):
    final = AudioSegment.empty()

    for f in files:
        final += AudioSegment.from_mp3(f)

    final.export(output, format="mp3")


def main():
    singer, n, duration, output = validate_args()

    print("\nDownloading videos...")
    download_audios(singer, n)

    print("\nCutting audio clips...")
    clips = trim_audios(duration)

    print("\nMerging audio files...")
    merge_audios(clips, output)

    print(f"\nMashup created successfully: {output}")


if __name__ == "__main__":
    main()
