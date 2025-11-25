import os
import subprocess
from datetime import datetime

from app.services.transcription_service import TranscriptionService


class SubtitleService:
    """
    Takes an audio file -> transcribes -> creates SRT -> burns subtitles into video using ffmpeg.
    """

    def __init__(self):
        self.transcriber = TranscriptionService()

    def embed_subtitles_from_audio(self, audio_path: str) -> str:
        # output dirs
        outputs_dir = os.path.join("app", "static", "outputs")
        os.makedirs(outputs_dir, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        srt_path = os.path.join(outputs_dir, f"{base_name}_{stamp}.srt")
        print(f"str output path was set to {srt_path}")
        video_path = os.path.join(outputs_dir, f"{base_name}_{stamp}.mp4")
        print(f"mp4 output path was set to {video_path}")

        # 1) transcribe to segments with timestamps
        print("calling subscribe service ")
        segments = self.transcriber.transcribe_with_timestamps(audio_path)

        print(f"below are the segments to be handled : {segments}")
        # 2) build SRT
        self._write_srt(segments, srt_path)

        # 3) create video with burned subtitles
        self._burn_subtitles(audio_path, srt_path, video_path)

        return video_path

    def _write_srt(self, segments, srt_path):
        """
        segments = list of dicts:
           [{ "start": 0.0, "end": 2.3, "text": "hello world" }, ...]
        """
        def format_ts(sec: float):
            ms = int((sec - int(sec)) * 1000)
            h = int(sec) // 3600
            m = (int(sec) % 3600) // 60
            s = int(sec) % 60
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        with open(srt_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segments, start=1):
                f.write(f"{i}\n")
                f.write(f"{format_ts(seg['start'])} --> {format_ts(seg['end'])}\n")
                f.write(seg["text"].strip() + "\n\n")

        print("successfully handled segments")

    import os
    import subprocess

    def _burn_subtitles(self, audio_path, srt_path, video_path):
        """
        Creates a black background video with audio,
        then burns subtitles into it (hard subtitles).
        """

        # 🔹 Use absolute path and forward slashes (ffmpeg-friendly)
        srt_abs = os.path.abspath(srt_path)
        srt_for_filter = srt_abs.replace("\\", "/")

        # Optional: also make audio/video paths absolute
        audio_abs = os.path.abspath(audio_path)
        video_abs = os.path.abspath(video_path)
        FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
        # 🔹 For the filter: escape backslashes and colon for Windows
        srt_for_filter = srt_abs.replace("\\", "\\\\").replace(":", "\\:")

        # 🔹 No styling yet – just get subtitles working
        vf_arg = f"subtitles='{srt_for_filter}'"
        cmd = [
            FFMPEG_PATH,
            "-y",
            "-i", audio_abs,
            "-f", "lavfi",
            "-i", "color=c=black:s=1280x720:r=30",
            "-shortest",
            "-vf", vf_arg,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-pix_fmt", "yuv420p",
            video_abs,
        ]

        print("starting to burn the mp4")
        print("FFmpeg command:", cmd)

        result = subprocess.run(cmd, capture_output=True, text=True)

        print("FFmpeg stdout:\n", result.stdout)
        print("FFmpeg stderr:\n", result.stderr)

        if result.returncode != 0:
            print("FFmpeg stderr:\n", result.stderr)
            raise RuntimeError(
                "ffmpeg failed:\n"
                f"{result.stderr}"
            )
