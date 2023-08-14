import requests
from bs4 import BeautifulSoup
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

def convert_to_devanagari(text, source_script):
    # Transliterate the text from the source script to Devanagari
    devanagari_text = transliterate(text, source_script, sanscript.DEVANAGARI)
    return devanagari_text

def convert_gurmukhi_to_devanagari(text):
    return convert_to_devanagari(text, 'gurmukhi')

def convert_bengali_to_devanagari(text):
    return convert_to_devanagari(text, 'bengali')

# Detected language code (e.g., 'gu' for Gujarati)
detected_language = 'gu'  # Replace with actual detection result

# URL to be parsed
url = "https://www.punjabijagran.com/editorial/general-the-whole-country-should-contribute-to-the-war-against-corruption-9265177.html"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
extracted_text = soup.get_text()

# Convert to Devanagari based on the detected script
if detected_language == 'gu':
    devanagari_text = convert_gurmukhi_to_devanagari(extracted_text)
    print("Devanagari Conversion (Gurmukhi):", devanagari_text)
elif detected_language == 'bn':
    devanagari_text = convert_bengali_to_devanagari(extracted_text)
    print("Devanagari Conversion (Bengali):", devanagari_text)
else:
    print("No conversion needed. Detected language is English.")
