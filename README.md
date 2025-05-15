# 🎌 Japanese Movie Transcriber

A Python script that uses [OpenAI Whisper](https://github.com/openai/whisper) to transcribe Japanese-language audio or video content into clean `.srt` subtitles (and optionally `.txt` transcripts).

It preprocesses the audio to reduce background noise, boost clarity, and outputs high-quality subtitles that skip ultra-short or duplicate segments.

---

## 🧐 The Problem

I've noticed that generating transcripts using regular Whisper wasn't quite as accurate and effective. Sometimes Whisper would hallucinate, repeat words or phrases, or fail to generate subtitles even though the audio was clear and there was minimal background music.

This script aims to fix that by using `ffmpeg` to enhance audio quality before transcription and adding other useful features for better output.

---

## ✨ Features

* ✅ Whisper Large-v3 for accurate Japanese transcription
* 🔊 Audio preprocessing with `ffmpeg` (noise reduction, normalization, dynamic gain)
* 🧹 Filters out ultra-short or repeated subtitle segments for cleaner output
* 📝 Outputs clean `.srt` subtitle files and optional plain `.txt` transcripts
* ⚙️ **Multiple transcription modes:**

  * `fast`: Greedy decoding with `best_of=3` (faster, less accurate)
  * `balanced` (default): Beam search with `beam_size=2` (good balance of speed and accuracy)
  * `accurate`: Beam search with `beam_size=5` (more accurate, slower)
* 🗑️ Automatically deletes temporary audio files after transcription
* 🎛️ User-friendly command line interface powered by `argparse`

---

## 📦 Requirements

* Python 3.8+
* `ffmpeg` (installed and accessible via your system PATH)
* Python packages:

  * `whisper`
  * `ffmpeg-python`

Install requirements with:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Usage

Show help and available options:

```bash
python transcribe_japanese.py --help
```

Basic usage (outputs `.srt` and optional `.txt`):

```bash
python transcribe_japanese.py path_to_audio_or_video_file
```

Example:

```bash
python transcribe_japanese.py "C:\Users\will\Documents\JP Media\dramas and movies\Perfect Days\Perfect Days.mkv" --txt --mode accurate
```

