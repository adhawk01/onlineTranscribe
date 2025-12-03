import os
from faster_whisper import WhisperModel


class TranscriptionService:
    """
    Only responsibility:
      audio -> timestamped text segments
    Using faster-whisper.
    """

    def __init__(
        self,
        model_size: str = "base",     # tiny, base, small, medium, large-v3
        device: str = "auto",          # "cpu", "cuda", or "auto"
        compute_type: str = "int8",    # "int8", "float16", "float32"
        language: str = "he"           # e.g. "he", "en" (None = auto-detect)
    ):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.language = language

        # Load model once (cached in memory)
        self.model = WhisperModel(
            model_size_or_path=self.model_size,
            device=self.device,
            compute_type=self.compute_type,
            cpu_threads=8,
            num_workers=2
        )

    def transcribe_with_timestamps(self, audio_path: str):
        """
        Returns list of segments:
          [{ "start": float, "end": float, "text": str }, ...]
        """

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print("starting to transcribe the file ")
        segments, info = self.model.transcribe(
            audio_path,
            language=self.language,
            beam_size=1,
            vad_filter=False,               # removes silent parts
            vad_parameters=dict(
                min_silence_duration_ms=500
            )
        )
        print(f"handling transcription results of segments)")
        result_segments = []
        for seg in segments:
            result_segments.append({
                "start": float(seg.start),
                "end": float(seg.end),
                "text": seg.text.strip()
            })
        print(f"result segments list was built {result_segments}")
        return result_segments
