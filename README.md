# News Text-to-Speech with Chirp3 HD Kore Voices

This application uses Google Cloud Text-to-Speech API to generate high-quality speech for news content in 9 Indian languages.

## Voice Selection

The application uses Chirp3 HD Kore voices for all languages, as they provide the highest quality speech output. The voice name format is:
```
{language_code}-Chirp3-HD-Kore
```

For example: `en-IN-Chirp3-HD-Kore`, `hi-IN-Chirp3-HD-Kore`, etc.

## Prerequisites

1. Python 3.7 or higher
2. Google Cloud account with Text-to-Speech API enabled
3. Google Cloud service account with access to Text-to-Speech API

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install google-cloud-texttospeech
   ```
3. Set up Google Cloud credentials:
   - Download your service account JSON key file
   - Update the credentials path in `tts.py`:
     ```python
     credentials_path = r"path/to/your/credentials.json"
     ```

## Usage

Run the interactive application:
```
python simple_tts.py
```

The application will:
1. Display a list of supported Indian languages
2. Ask you to select a language by entering its number
3. Prompt you to enter news text in that language
4. Use the Chirp3 HD Kore voice for the selected language
5. Generate the audio and save it in a language-specific directory
   (e.g., `output/Hindi/your_text.mp3`)
6. Ask if you want to generate another audio file

## Supported Languages

The application supports the following Indian languages:

- English (Indian)
- Hindi
- Marathi
- Gujarati
- Telugu
- Kannada
- Bengali
- Tamil
- Malayalam


## Output Files

Generated audio files are saved in the `output` directory, organized by language. Each file is named based on the text content.

## Output Organization

Audio files are organized into language-specific directories:
```
output/
├── Bengali/
│   └── your_text.mp3
├── English_Indian/
│   └── your_text.mp3
├── Hindi/
│   └── your_text.mp3
├── Gujarati/
│   └── your_text.mp3
├── Telugu/
│   └── your_text.mp3
├── Kannada/
│   └── your_text.mp3
├── Tamil/
│   └── your_text.mp3
└── Malayalam/
    └── your_text.mp3
``` 
