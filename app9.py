from flask import Flask, request, send_file, jsonify, render_template
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.route('/')
def home():
    return render_template('index9.html')


@app.route('/download/youtube', methods=['POST'])
def download_youtube():
    data = request.json
    url = data.get('url')
    format_type = data.get('format', 'video')

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    filename = f"{uuid.uuid4()}.%(ext)s"
    output_path = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        'outtmpl': output_path,
        'quiet': True,
    }

    if format_type == 'audio':
        ydl_opts['format'] = 'bestaudio'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        ydl_opts['format'] = 'best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)
            if format_type == 'audio':
                downloaded_file = downloaded_file.rsplit('.', 1)[0] + '.mp3'

        return send_file(downloaded_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5010)
