from flask import Flask, request, send_file, jsonify, render_template
import yt_dlp
import os
import uuid

app = Flask(__name__, static_url_path='',
            static_folder='.', template_folder='.')

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.route('/')
def home():
    return render_template('index1.html')


@app.route('/download_dailymotion', methods=['POST'])
def download_dailymotion():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    if "dailymotion.com" not in url:
        return jsonify({"error": "URL is not a valid Dailymotion video"}), 400

    filename = f"{uuid.uuid4()}.%(ext)s"
    output_path = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        'outtmpl': output_path,
        'quiet': True,
        'format': 'best',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)

        if not os.path.exists(downloaded_file):
            return jsonify({"error": "Downloaded file not found"}), 500

        return send_file(downloaded_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5004)
