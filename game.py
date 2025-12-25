import random
import os
import time

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_translations(filename="translations.txt"):
    """Loads translations from a file."""
    translations = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                translations.append((parts[0], parts[1]))
    return translations

def main():
    """Main function for the game."""
    translations = load_translations()
    if not translations:
        print("No translations found. Please run pdf_extractor.py first.")
        return

    while True:
        clear_screen()
        german_word, greek_word = random.choice(translations)
        
        print("German word (type 'exit' to quit):")
        print(german_word)
        
        user_input = input("\nPress Enter to see the translation or type 'exit' to quit: ")
        
        if user_input.lower() == 'exit':
            break
        
        print("\nGreek translation:")
        print(greek_word)
        
        time.sleep(2) # Wait for 2 seconds before the next word

if __name__ == "__main__":
    main()
