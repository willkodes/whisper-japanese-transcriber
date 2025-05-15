import os
import sys
import shutil
import argparse
import whisper
import ffmpeg

def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        sys.exit("❌ ffmpeg is not installed or not in your PATH. Please install it first.")

def preprocess_audio(input_path, output_wav):
    print("🔧 Preprocessing audio with ffmpeg...")
    try:
        (
            ffmpeg
            .input(input_path)
            .output(
                output_wav,
                af="highpass=f=100, lowpass=f=3000, afftdn, dynaudnorm=f=150:g=20, compand=attacks=0.3:decays=0.8:points=-80/-80|-20/-5|0/-3:soft-knee=6, volume=6dB",
                ar=16000,
                ac=1,
                acodec="pcm_s16le"
            )
            .run(overwrite_output=True, quiet=True)
        )
        print(f"✅ Cleaned audio saved to {output_wav}")
    except ffmpeg.Error as e:
        sys.exit(f"❌ ffmpeg failed: {e.stderr.decode()}")

def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def transcribe_to_srt(audio_path, output_srt, output_txt=None, beam_size=None, best_of=None):
    print("🧠 Loading Whisper large-v3 model...")
    try:
        model = whisper.load_model("large-v3")
    except Exception as e:
        sys.exit(f"❌ Failed to load Whisper model: {e}")

    if beam_size:  # beam search mode
        temperature = 0.0
    else:          # greedy + best_of
        temperature = 0.3

    print("📖 Transcribing...")
    try:
        result = model.transcribe(
            audio_path,
            language="ja",
            task="transcribe",
            word_timestamps=False,
            temperature=temperature,
            no_speech_threshold=0.3,
            condition_on_previous_text=False,
            beam_size=beam_size,
            best_of=best_of
        )

    except Exception as e:
        sys.exit(f"❌ Transcription failed: {e}")

    print(f"💾 Saving subtitles to {output_srt}...")
    try:
        with open(output_srt, "w", encoding="utf-8") as srt_file:
            txt_file = open(output_txt, "w", encoding="utf-8") if output_txt else None
            segment_index = 1
            min_duration = 0.5
            last_text = ""

            for segment in result["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()

                if (end - start) < min_duration or text == last_text:
                    continue
                if end <= start:
                    end = start + 0.5

                srt_file.write(f"{segment_index}\n")
                srt_file.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
                srt_file.write(f"{text}\n\n")

                if txt_file:
                    txt_file.write(f"{text}\n")

                last_text = text
                segment_index += 1

            if txt_file:
                txt_file.close()

        print(f"📏 Transcribed {segment_index - 1} segments over {result['segments'][-1]['end']:.2f} seconds")
        print(f"💾 Saving {output_srt} to '{os.path.abspath(output_srt)}'")
        if output_txt:
            print(f"💾 Saving {output_txt} to '{os.path.abspath(output_txt)}'")
    except Exception as e:
        sys.exit(f"❌ Failed to write output files: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="🎌 Transcribe Japanese audio/video to clean subtitles using Whisper."
    )
    parser.add_argument("input_file", help="Path to video or audio file (e.g., .mp4, .mkv, .mp3)")
    parser.add_argument("--txt", action="store_true", help="Also output a plain .txt transcript")
    parser.add_argument(
        "--mode", choices=["fast", "balanced", "accurate"], default="balanced",
        help="Transcription mode: fast (no beam), balanced (beam=2), accurate (beam=5)"
    )
    args = parser.parse_args()

    input_file = args.input_file

    if not os.path.exists(input_file):
        sys.exit(f"❌ File not found: {input_file}")

    # Beam search settings based on mode
    if args.mode == "fast":
        beam_size = None
        best_of = 3
    elif args.mode == "balanced":
        beam_size = 2
        best_of = None
    elif args.mode == "accurate":
        beam_size = 5
        best_of = None
    else:
        beam_size = None
        best_of = None

    base = os.path.splitext(os.path.basename(input_file))[0]
    cleaned_wav = f"{base}_clean.wav"
    output_srt = f"{base}_ja.srt"
    output_txt = f"{base}_ja.txt" if args.txt else None

    check_ffmpeg()
    preprocess_audio(input_file, cleaned_wav)

    try:
        transcribe_to_srt(
            cleaned_wav,
            output_srt,
            output_txt,
            beam_size=beam_size,
            best_of=best_of
        )
    finally:
        if os.path.exists(cleaned_wav):
            os.remove(cleaned_wav)
            print(f"🗑️ Deleted temporary file: {cleaned_wav}")


if __name__ == "__main__":
    main()
