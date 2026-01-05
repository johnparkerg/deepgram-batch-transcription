#!/usr/bin/env python3
"""CLI tool to transcribe audio/video files in a folder using Deepgram."""

import argparse
import os
import sys
from pathlib import Path

import requests


SUPPORTED_EXTENSIONS = (".mp4", ".mp3", ".wav", ".m4a", ".flac", ".ogg", ".webm")

CONTENT_TYPES = {
    ".mp4": "audio/mp4",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/mp4",
    ".flac": "audio/flac",
    ".ogg": "audio/ogg",
    ".webm": "audio/webm",
}


def find_audio_files(folder: Path) -> list[Path]:
    """Find all supported audio/video files in the given folder."""
    files = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(folder.glob(f"*{ext}"))
        files.extend(folder.glob(f"*{ext.upper()}"))
    return files


def transcribe_file(
    file_path: Path,
    api_key: str,
    language: str | None = None,
    diarization: bool = False,
) -> dict:
    """Transcribe a single audio/video file using Deepgram API."""
    url = "https://api.deepgram.com/v1/listen"

    params = {
        "punctuate": "true",
        "model": "nova-3",
        "smart_format": "true",
        "paragraphs": "true",
    }

    if language:
        params["language"] = language

    if diarization:
        params["diarize"] = "true"
        params["utterances"] = "true"
        params["utt_split"] = "2.0"

    content_type = CONTENT_TYPES.get(file_path.suffix.lower(), "audio/mpeg")
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": content_type,
    }

    with open(file_path, "rb") as f:
        response = requests.post(url, headers=headers, params=params, data=f)

    response.raise_for_status()
    return response.json()


def format_transcript(result: dict, diarization: bool = False) -> str:
    """Format the transcript from Deepgram response."""
    lines = []

    if diarization and "utterances" in result.get("results", {}):
        for utterance in result["results"]["utterances"]:
            speaker = utterance.get("speaker", 0)
            text = utterance.get("transcript", "").strip()
            lines.append(f"[Speaker {speaker}]: {text}")
    else:
        channels = result.get("results", {}).get("channels", [])
        if channels:
            alternatives = channels[0].get("alternatives", [])
            if alternatives:
                transcript = alternatives[0].get("transcript", "")
                lines.append(transcript)

    return "\n\n".join(lines)


def save_transcription(content: str, output_path: Path) -> None:
    """Save transcription to file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe all audio/video files in a folder using Deepgram.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported formats: mp4, mp3, wav, m4a, flac, ogg, webm

Examples:
  %(prog)s /path/to/videos
  %(prog)s /path/to/videos --lang en
  %(prog)s /path/to/videos --diarization
  %(prog)s /path/to/videos --diarization --ext srt
        """,
    )

    parser.add_argument(
        "folder",
        type=Path,
        help="Folder containing audio/video files to transcribe",
    )
    parser.add_argument(
        "--lang",
        "-l",
        type=str,
        default=None,
        help="Language code (e.g., 'en', 'es', 'fr'). Auto-detected if not specified.",
    )
    parser.add_argument(
        "--diarization",
        "-d",
        action="store_true",
        help="Enable speaker diarization",
    )
    parser.add_argument(
        "--ext",
        "-e",
        type=str,
        default="txt",
        help="Output file extension (default: txt)",
    )
    parser.add_argument(
        "--api-key",
        "-k",
        type=str,
        default=os.environ.get("DEEPGRAM_API_KEY"),
        help="Deepgram API key (defaults to DEEPGRAM_API_KEY env var)",
    )

    args = parser.parse_args()

    # Validate API key
    if not args.api_key:
        print(
            "Error: Deepgram API key required. Set DEEPGRAM_API_KEY env var or use --api-key.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate folder
    if not args.folder.exists():
        print(f"Error: Folder '{args.folder}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not args.folder.is_dir():
        print(f"Error: '{args.folder}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Find audio/video files
    audio_files = find_audio_files(args.folder)

    if not audio_files:
        print(f"No supported audio/video files found in '{args.folder}'.")
        sys.exit(0)

    print(f"Found {len(audio_files)} file(s) to transcribe.")

    # Process each file
    for i, audio_file in enumerate(audio_files, 1):
        output_path = audio_file.with_suffix(f".{args.ext.lstrip('.')}")

        print(f"\n[{i}/{len(audio_files)}] Transcribing: {audio_file.name}")

        try:
            result = transcribe_file(
                file_path=audio_file,
                api_key=args.api_key,
                language=args.lang,
                diarization=args.diarization,
            )

            content = format_transcript(result, diarization=args.diarization)
            save_transcription(content, output_path)

            print(f"  Saved to: {output_path.name}")

        except requests.exceptions.HTTPError as e:
            print(f"  API Error: {e.response.status_code} - {e.response.text}", file=sys.stderr)
            continue
        except Exception as e:
            print(f"  Error transcribing {audio_file.name}: {e}", file=sys.stderr)
            continue

    print("\nTranscription complete!")


if __name__ == "__main__":
    main()
