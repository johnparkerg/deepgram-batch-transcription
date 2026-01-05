# Audio/Video Transcription Tool

A simple tool to automatically transcribe audio and video files using Deepgram's AI.

## What This Tool Does

- Transcribes all audio/video files in a folder
- Saves transcriptions as text files in the same folder
- Can identify different speakers (diarization)
- Supports: MP4, MP3, WAV, M4A, FLAC, OGG, WEBM

---

## Setup (One-Time)

### Step 1: Get a Deepgram API Key

1. Go to [console.deepgram.com](https://console.deepgram.com/signup)
2. Create a free account (includes $200 free credit)
3. Go to "API Keys" and create a new key
4. Copy the key somewhere safe

### Step 2: Install Python (if you don't have it)

**Mac:**
Open Terminal and run:
```
brew install python
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/) and install.

### Step 3: Set Up the Tool

Open Terminal (Mac) or Command Prompt (Windows), then:

```
cd /path/to/this/folder
python3 -m venv venv
source venv/bin/activate
pip install requests
```

---

## How to Use

### Basic Usage

Open Terminal, navigate to this folder, then:

```
source venv/bin/activate
python3 transcribe.py /path/to/your/videos --api-key YOUR_API_KEY
```

Replace:
- `/path/to/your/videos` with the folder containing your files
- `YOUR_API_KEY` with your Deepgram API key

### With Speaker Identification

If your audio has multiple speakers:

```
python3 transcribe.py /path/to/your/videos --api-key YOUR_API_KEY --diarization
```

### Specify Language

For better accuracy, specify the language:

```
python3 transcribe.py /path/to/your/videos --api-key YOUR_API_KEY --lang es
```

Common language codes:
- `en` = English
- `es` = Spanish
- `fr` = French
- `de` = German
- `pt` = Portuguese
- `it` = Italian

### Full Example

Transcribe Spanish videos with speaker identification:

```
python3 transcribe.py ~/Desktop/my-recordings --api-key abc123 --diarization --lang es
```

---

## Output

For each file like `interview.mp4`, you'll get `interview.txt` containing:

```
[Speaker 0]: Hello, welcome to the show.

[Speaker 1]: Thank you for having me.

[Speaker 0]: Let's start with your background.
```

---

## Options Reference

| Option | What it does |
|--------|--------------|
| `--diarization` or `-d` | Identify different speakers |
| `--lang XX` or `-l XX` | Set language (e.g., `en`, `es`, `fr`) |
| `--ext XX` or `-e XX` | Change output extension (default: `txt`) |
| `--api-key XX` or `-k XX` | Your Deepgram API key |

---

## Troubleshooting

**"No module named requests"**
→ Run: `source venv/bin/activate && pip install requests`

**"command not found: python3"**
→ Install Python (see Setup Step 2)

**"API Error: 401"**
→ Check your API key is correct

**"No supported audio/video files found"**
→ Make sure your files end in .mp4, .mp3, .wav, etc.

---

## Save Your API Key (Optional)

To avoid typing your API key every time:

1. Create a file called `.env` in this folder
2. Add this line: `DEEPGRAM_API_KEY=your_key_here`
3. Now you can run without `--api-key`:
   ```
   source venv/bin/activate
   source .env
   python3 transcribe.py /path/to/videos --diarization
   ```
