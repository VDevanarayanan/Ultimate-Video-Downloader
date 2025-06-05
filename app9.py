from flask import Flask, Blueprint, request, send_file, jsonify
import yt_dlp
import os
import uuid
import traceback

app = Flask(__name__)
youtube_bp = Blueprint('youtube', __name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@youtube_bp.route('/download_youtube', methods=['POST'])
def download_youtube():
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({"error": "Missing URL"}), 400

        if not ("youtube.com" in url or "youtu.be" in url):
            return jsonify({"error": "Invalid YouTube URL"}), 400

        # Output template with UUID
        filename_template = f"{uuid.uuid4()}.%(ext)s"
        output_path = os.path.join(DOWNLOAD_DIR, filename_template)

        # yt_dlp options
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

            # Ensure .mp4 extension if merged
            if not downloaded_file.endswith(".mp4"):
                downloaded_file = downloaded_file.rsplit(".", 1)[0] + ".mp4"

        # Final file check
        if not os.path.exists(downloaded_file):
            return jsonify({"error": "Downloaded file not found"}), 500

        return send_file(
            downloaded_file,
            as_attachment=True,
            download_name=os.path.basename(downloaded_file),
            mimetype='video/mp4'
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


def register_youtube_routes(app):
    app.register_blueprint(youtube_bp)


if __name__ == '__main__':
    register_youtube_routes(app)
    app.run(debug=True, port=5000)
