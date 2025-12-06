from flask import Flask, request, jsonify
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import tempfile

app = Flask(__name__)

@app.route("/api/convert", methods=["POST"])
def convert():
    try:
        data = request.get_json()
        url = data.get("url")
        if not url:
            return jsonify({"success": False, "error": "No URL provided"})

        # Download audio
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        temp_dir = tempfile.gettempdir()
        out_file = video.download(output_path=temp_dir)
        
        # Convert to MP3
        mp3_file = out_file.replace(".mp4", ".mp3")
        audio_clip = AudioFileClip(out_file)
        audio_clip.write_audiofile(mp3_file)
        audio_clip.close()
        os.remove(out_file)

        # Return downloadable file path
        return jsonify({"success": True, "file": mp3_file})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run()

