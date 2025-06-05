import os
from dotenv import load_dotenv
from google.cloud import texttospeech
from google.oauth2 import service_account
from elevenlabs import ElevenLabs
import asyncio
import aiofiles
from openai import AsyncOpenAI

# Load environment variables from .env file
load_dotenv()

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Set credentials path directly
credentials_path = r"C:\Users\SRINIVAS\Downloads\awesome-aspect-455006-b6-66b76a86c2f4.json"
credentials = service_account.Credentials.from_service_account_file(credentials_path)

elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
eleven_client = ElevenLabs(api_key=elevenlabs_api_key)
eleven_voice_ids = {
    "hi": "cOkIhvYxjsVSr2hF7Qsh",
    "ta": "Q9XUbaP7Z0Az8OW9CyRg",
}
OPENAI_SUPPORTED_LANGUAGES = {
    "kn": "onyx",
    "te": "nova"
}
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

async def synthesize_with_openai(text, voice_name, output_file):
    try:
        async with openai_client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=voice_name,
            input=text,
            instructions="Speak in a clear and natural tone.",
            response_format="mp3",
        ) as response:
            async with aiofiles.open(output_file, 'wb') as f:
                async for chunk in response.iter_bytes():
                    await f.write(chunk)

        print(f"OpenAI voice audio saved: {output_file}")
        return True
    except Exception as e:
        print(f"OpenAI TTS error: {e}")
        return False
    
def synthesize_with_google(text, language_code, output_file):
    """Synthesize speech from text using Chirp3 HD Kore voice."""
    try:
        client = texttospeech.TextToSpeechClient(credentials=credentials)
        
        # Get the Chirp3 HD Kore voice for this language
        if(language_code == "mr-IN"):
            voice_name = f"{language_code}-Chirp3-HD-Algieba"
        elif(language_code == "en-IN") : voice_name = f"{language_code}-Chirp3-HD-Achernar"
        elif(language_code == "gu-IN") : voice_name = f"{language_code}-Chirp3-HD-Iapetus"
        elif(language_code == "bn-IN") : voice_name = f"{language_code}-Chirp3-HD-Rasalgethi"
        else: voice_name = f"{language_code}-Chirp3-HD-Kore"
        
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
    
def synthesize_with_elevenlabs(text, lang_code, output_file):
    """Synthesize speech from text using ElevenLabs API."""
    try:
        voice_id = eleven_voice_ids.get(lang_code)
        if not voice_id:
            raise ValueError("Voice ID not found for ElevenLabs.")

        stream = eleven_client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_44100_128",
            text=text,
            model_id="eleven_multilingual_v2"
        )

        with open(output_file, "wb") as f:
            for chunk in stream:
                f.write(chunk)

        print(f"ElevenLabs TTS audio saved: {output_file}")
        return True
    except Exception as e:
        print(f"ElevenLabs TTS error: {e}")
        return False

def process_json_file(data):
    """Process a JSON dictionary and generate speech for the given headline and summary."""
    if not isinstance(data, dict):
        print("Error: Expected a dictionary but got something else.")
        return False
    
    text = f"{data.get('headline', '')}. {data.get('summary', '')}".strip()
    language_code = data.get("language", "en")
    
    if language_code not in INDIAN_LANGUAGES:
        print(f"Error: Language '{language_code}' not supported.")
        return False
    
    # Make sure output directories exist
    create_output_directory()
    
    # Get the directory name for this language
    lang_dir = INDIAN_LANGUAGES[language_code]
    
    # Create a safe filename from the headline
    safe_text = "".join(c if c.isalnum() or c in " _-" else "_" for c in data.get("headline", "news")[:30])
    safe_text = safe_text.strip().replace(" ", "_")
    
    # Create output path in the language directory
    output_file = os.path.join("output", lang_dir, f"{safe_text}.mp3")
    full_language_code = f"{language_code}-IN"
    
    if language_code in OPENAI_SUPPORTED_LANGUAGES:
        voice_name = OPENAI_SUPPORTED_LANGUAGES[language_code]
        return asyncio.run(synthesize_with_openai(text, voice_name, output_file))
    elif language_code in eleven_voice_ids:
        return synthesize_with_elevenlabs(text, language_code, output_file)
    else:
        return synthesize_with_google(text, full_language_code, output_file)
