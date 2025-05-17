# 🎌 Japanese Media Transcriber

A Python script that uses [OpenAI Whisper](https://github.com/openai/whisper) to transcribe Japanese-language audio or video content into clean `.srt` subtitles (and optionally `.txt` transcripts).

It preprocesses the audio to reduce background noise, boost clarity, and outputs high-quality subtitles that skip ultra-short or duplicate segments.

---

<p align="center">
  <img src="assets/demo.gif" width="600">
</p>

## 🧐 The Problem

Generating transcripts using regular Whisper can often be inaccurate or ineffective. Sometimes Whisper hallucinates, repeats words or phrases, or fails to generate subtitles—even when the audio is clear and there’s minimal background noise.

This script addresses that by using `ffmpeg` to enhance audio quality before transcription and adds other useful features for cleaner output.

---

## ✨ Features

* ✅ Supports Whisper models: `tiny`, `base`, `small`, `medium`, `large`, `turbo`. Default is `large-v3`.
* 🔊 Audio preprocessing with `ffmpeg` (noise reduction, normalization, dynamic gain)
* 🧹 Filters out ultra-short or repeated subtitle segments for cleaner output
* 📝 Outputs clean `.srt` subtitle files and optional plain `.txt` transcripts
* ⚙️ **Multiple transcription modes:**
  * `fast`: Greedy decoding with `best_of=3` (faster, less accurate)
  * `balanced` (default): Beam search with `beam_size=2` (good balance of speed and accuracy)
  * `accurate`: Beam search with `beam_size=5` (more accurate, slower)
* 🗑️ Automatically deletes temporary audio files after transcription
* 🎛️ User-friendly command-line interface powered by `argparse`

---

## 🎯 Intended Use

This script is best used for transcribing natural Japanese speech, such as in movies and YouTube videos. Note that anime may result in hallucinations or reduced accuracy due to its unique intonations and often exaggerated speech patterns—Whisper was primarily trained on natural conversational speech.

---

## 📦 Requirements

* Python 3.8+
* [`ffmpeg`](https://ffmpeg.org/download.html) (must be installed and accessible via your system's PATH)
* Python packages:
  * `whisper`
  * `ffmpeg-python`

It is **highly recommended** to use a virtual environment to manage dependencies. Create one using `venv`:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows
````

If you encounter an execution policy error on Windows, run this before activating the environment:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Install dependencies:

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