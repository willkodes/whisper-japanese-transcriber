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

## 🖥️ Hardware & Performance Notes

This script uses OpenAI’s Whisper model for transcription, which can run on both CPU and NVIDIA GPUs with CUDA support.

- **NVIDIA GPU (CUDA)**: If you have a compatible NVIDIA GPU, Whisper will utilize GPU acceleration for significantly faster transcription.
- **CPU-only or AMD/Intel GPU**: The script works perfectly on CPU without GPU acceleration, but transcription will be slower, especially with larger models like `large-v3`.
- For faster performance on CPU-only machines, consider using smaller Whisper models (`tiny`, `base`, or `small`) or selecting the `fast` transcription mode.
- An alternative implementation like [Faster Whisper](https://github.com/guillaumekln/faster-whisper) can provide improved speed on CUDA GPUs but is not officially integrated here.
- GPU acceleration is currently limited to NVIDIA CUDA-enabled hardware; AMD and Intel GPUs are not supported for acceleration in Whisper.

---

## 🎯 Intended Use

This script is best used for transcribing natural Japanese speech, such as in movies and YouTube videos. Note that anime may result in hallucinations or reduced accuracy due to its unique intonations and often exaggerated speech patterns—Whisper was primarily trained on natural conversational speech.

---

## 📊 Findings (Preliminary)

In practical testing across various Japanese audio and video sources (including movies and YouTube content), this script demonstrated a **significant improvement** in transcription quality compared to standard Whisper.

### Observed improvements:
- ✅ **Increased subtitle coverage**: Estimated **90–100%** subtitle generation across tested clips, including lines Whisper previously skipped.
- 🧠 **Fewer hallucinations**: Markedly fewer hallucinated or repeated phrases.
- 🔊 **Improved clarity**: Audio preprocessing resulted in more consistent recognition, especially in noisy or low-volume recordings.

> ⚠️ These findings are based on observational comparison and not yet backed by formal WER/CER testing or large-scale benchmarking. Scientific validation is encouraged for objective measurement of accuracy improvements.

---

## 🛠 Installation

To get started quickly, install Python dependencies and FFmpeg:

```bash
pip install -r requirements.txt
````

FFmpeg is required for audio preprocessing. For installation instructions, see:
[FFmpeg Installation Guide](https://ffmpeg.org/download.html)

---

For a complete step-by-step setup guide from a fresh PC—including installing Python, VS Code, Git, and FFmpeg—please visit the full installation guide:
[Full Installation Guide](https://your-google-doc-link)

---

## 📦 Requirements

* Python 3.8+
* `ffmpeg`
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