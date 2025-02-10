from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os

temp_folder = "downloads"
os.makedirs(temp_folder, exist_ok=True)

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        video_url = data.get('url')
        
        if not video_url:
            return jsonify({"error": "URL is required"}), 400
        
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        
        file_path = os.path.join(temp_folder, f"{yt.title}.mp4")
        stream.download(output_path=temp_folder, filename=f"{yt.title}.mp4")
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
