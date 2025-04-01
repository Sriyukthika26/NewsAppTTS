import os
import json
from google.cloud import texttospeech
from google.oauth2 import service_account

# Set credentials path directly
credentials_path = r"C:\Users\SRINIVAS\Downloads\awesome-aspect-455006-b6-e45e9e01c19e.json"
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Map of Indian languages with their codes
INDIAN_LANGUAGES = {
    "en": "English_Indian",
    "hi": "Hindi",
    "mr": "Marathi",
    "gu": "Gujarati",
    "te": "Telugu",
    "kn": "Kannada",
    "bn": "Bengali",
    "ta": "Tamil",
    "ml": "Malayalam"
}

def create_output_directory():
    """Create the output directory if it doesn't exist."""
    if not os.path.exists("output"):
        os.makedirs("output")
    
    # Create language directories
    for lang_dir in INDIAN_LANGUAGES.values():
        dir_path = os.path.join("output", lang_dir)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

def synthesize_speech(text, language_code, output_file):
    """Synthesize speech from text using Chirp3 HD Kore voice."""
    try:
        client = texttospeech.TextToSpeechClient(credentials=credentials)
        
        # Get the Chirp3 HD Kore voice for this language
        voice_name = f"{language_code}-Chirp3-HD-Kore"
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            effects_profile_id=["high-quality-studio"]
        )
        
        print(f"Generating speech with voice: {voice_name}")
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        
        print(f"Audio content written to '{output_file}'")
        return True
    except Exception as e:
        print(f"Error generating speech: {e}")
        return False

def process_json_file(data):
    """Process a JSON dictionary and generate speech for the given headline and summary."""
    if not isinstance(data, dict):
        print("Error: Expected a dictionary but got something else.")
        return False
    
    text = f"{data.get('headline', '')}. {data.get('summary', '')}".strip()
    language_code = data.get("language", "en") + "-IN"
    
    if language_code[:2] not in INDIAN_LANGUAGES:
        print(f"Error: Language '{language_code}' not supported.")
        return False
    
    # Make sure output directories exist
    create_output_directory()
    
    # Get the directory name for this language
    lang_dir = INDIAN_LANGUAGES[language_code[:2]]
    
    # Create a safe filename from the headline
    safe_text = "".join(c if c.isalnum() or c in " _-" else "_" for c in data.get("headline", "news")[:30])
    safe_text = safe_text.strip().replace(" ", "_")
    
    # Create output path in the language directory
    output_file = os.path.join("output", lang_dir, f"{safe_text}.mp3")
    
    return synthesize_speech(text, language_code, output_file)
