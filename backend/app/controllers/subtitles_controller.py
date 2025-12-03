import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from app.services.subtitle_service import SubtitleService

subtitles_bp = Blueprint("subtitles", __name__)


@subtitles_bp.route("/embedSubtitle", methods=["POST"])
def embed_subtitle():
    # 1) validate file
    if "audio" not in request.files:
        return jsonify({"error": "Missing 'audio' file in form-data"}), 400

    audio_file = request.files["audio"]
    if audio_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # 2) save uploaded audio
    filename = secure_filename(audio_file.filename)
    upload_dir = current_app.config.get("UPLOAD_DIR", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    print("saving uploaded file")
    audio_path = os.path.join(upload_dir, filename)
    audio_file.save(audio_path)

    print("sudio file uploaded and saved")

    # 3) call service
    subtitle_service = SubtitleService()
    try:
        video_path = subtitle_service.embed_subtitles_from_audio(audio_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # 4) return location of created video
    return jsonify({
        "message": "Video created successfully",
        "video_path": video_path
    }), 200
