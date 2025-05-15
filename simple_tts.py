import json
from tts import process_json_file

def main():
    """Simple TTS generator that processes a JSON file."""
    print("News Text-to-Speech Generator")
    print("================================\n")
    
    json_file_path = "news_data9.json" 

    # Load JSON data
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file_path}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: JSON file '{json_file_path}' is not valid JSON.")
        return
    
    # Process the loaded JSON dictionary
    print(f"\nProcessing article: {data.get('headline', 'Unknown headline')}...")
    success = process_json_file(data)
    
    if success:
        print("Speech generated successfully!")
    else:
        print("Failed to generate speech.")

if __name__ == "__main__":
    main()
