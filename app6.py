from flask import Flask, Blueprint, request, send_file, jsonify
import yt_dlp
import os
import uuid
import traceback

app = Flask(__name__)
tiktok_bp = Blueprint('tiktok', __name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@tiktok_bp.route('/download_tiktok', methods=['POST'])
def download_tiktok():
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({"error": "Missing URL"}), 400

        if "tiktok.com" not in url:
            return jsonify({"error": "Invalid tiktok URL"}), 400

        filename = f"{uuid.uuid4()}.%(ext)s"
        output_path = os.path.join(DOWNLOAD_DIR, filename)

        ydl_opts = {
            'outtmpl': output_path,
            'quiet': True,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)
            if not downloaded_file.endswith(".mp4"):
                downloaded_file = downloaded_file.rsplit('.', 1)[0] + ".mp4"

        return send_file(downloaded_file, as_attachment=True)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


def register_tiktok_routes(app):
    app.register_blueprint(tiktok_bp)


if __name__ == '__main__':
    register_tiktok_routes(app)
    app.run()
