import os
from tts import generate_speech, INDIAN_LANGUAGES

def main():
    """Simple TTS generator for news content."""
    print("News Text-to-Speech Generator")
    print("============================")
    
    # Show language options
    print("\nAvailable Languages:")
    language_mapping = []
    for i, (code, name) in enumerate(INDIAN_LANGUAGES.items(), 1):
        print(f"{i}. {name.replace('_', ' ')}")
        language_mapping.append((code, name))
    
    while True:
        # Get language selection
        try:
            selection = input("\nSelect language (number) or 'q' to quit: ")
            
            if selection.lower() == 'q':
                print("Exiting...")
                break
            
            lang_index = int(selection) - 1
            if 0 <= lang_index < len(language_mapping):
                language_code = language_mapping[lang_index][0]
                language_name = language_mapping[lang_index][1].replace('_', ' ')
            else:
                print("Invalid selection. Please try again.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")
            continue
        
        # Get text to convert
        text = input(f"\nEnter news text to convert to speech in {language_name}: ")
        
        if not text.strip():
            print("Text cannot be empty. Please try again.")
            continue
        
        # Generate speech
        print(f"\nGenerating speech in {language_name}...")
        success = generate_speech(text, language_code)
        
        if success:
            print("Speech generated successfully!")
        else:
            print("Failed to generate speech. Please try again.")
        
        # Ask to generate another file
        another = input("\nGenerate another audio file? (y/n): ")
        if another.lower() != 'y':
            print("Exiting...")
            break

if __name__ == "__main__":
    main() 