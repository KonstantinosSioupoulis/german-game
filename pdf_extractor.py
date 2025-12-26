import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def process_text_and_save(text,translations_file):
    """Processes the extracted text to find German-Greek pairs and saves them."""
    lines = text.split('\n')
    translations = []
    i = 0
    while i < len(lines) - 1:
        german_line = lines[i].strip()
        greek_line = lines[i+1].strip()

        # Heuristic to identify a German line followed by a Greek line
        if re.search(r'^[a-zA-ZÄÖÜäöüß]', german_line) and not re.search(r'[α-ωΑ-Ω]', german_line) and re.search(r'[α-ωΑ-Ω]', greek_line):
            # Check if the german line is not a page number or other noise
            if not re.match(r'^Seite \d+$', german_line, re.IGNORECASE):
                translations.append((german_line, greek_line))
                i += 2  # Move to the line after the Greek translation
            else:
                i += 1
        else:
            i += 1

    with open(translations_file, "w", encoding="utf-8") as f:
        for german, greek in translations:
            f.write(f"{german}\t{greek}\n")
    return translations

def main(pdf_path,translations_file):
    """Main function to run the script."""
    #pdf_path = "Cornelsen-Das_Leben_A1_GLDEGR (1).pdf"
    raw_text = extract_text_from_pdf(pdf_path)
    
    # Let's first save the raw text to a file to inspect it
    with open("raw_text.txt", "w", encoding="utf-8") as f:
        f.write(raw_text)
        
    print("Raw text extracted from PDF and saved to raw_text.txt")
    
    translations = process_text_and_save(raw_text,translations_file)
    
    if translations:
        print(f"Found and saved {len(translations)} translations to {translations_file}")
    else:
        print("No translations found based on the current pattern. The raw text is available in raw_text.txt for inspection.")

if __name__ == "__main__":
    main("Cornelsen-Das_Leben_A1_GLDEGR (1).pdf","translations_a1.txt")
    main("Cornelsen-Das_Leben_A2_GLDEGR.pdf","translations_a2.txt")
