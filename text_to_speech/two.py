from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import boto3
import os
import requests
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

app = Flask(__name__)

def convert_to_devanagari(text, source_script):
    devanagari_text = transliterate(text, source_script, sanscript.DEVANAGARI)
    return devanagari_text

def convert_gurmukhi_to_devanagari(text):
    return convert_to_devanagari(text, 'gurmukhi')

def convert_bengali_to_devanagari(text):
    return convert_to_devanagari(text, 'bengali')

def aws_polly_text_to_speech(text):
    # Your existing AWS Polly text-to-speech logic here

    aws_mag_con = boto3.session.Session(profile_name='test_user')
    client = aws_mag_con.client(service_name='polly', region_name='us-east-1')

    chunk_size = 2000
    i = 0
    audio_chunks = []  # Store audio chunks filenames

    while i < len(text):
        chunk = text[i:i + chunk_size]

        response = client.synthesize_speech(
            VoiceId='Aditi',
            OutputFormat='mp3',
            Text=chunk,
            Engine='standard'
        )

        if "AudioStream" in response:
            audio_filename = f"output_chunk_{i // chunk_size}.mp3"
            with open(audio_filename, "wb") as f:
                f.write(response["AudioStream"].read())
            audio_chunks.append(audio_filename)
            print(f"Speech synthesis successful for chunk {i // chunk_size}.")
        else:
            print(f"Speech synthesis failed for chunk {i // chunk_size}.")

        i += chunk_size

    # Combine audio chunks into a single audio file
    combined_audio = b"".join([open(filename, "rb").read() for filename in audio_chunks])

    # Save the combined audio to a file
    with open("output_combined.mp3", "wb") as f:
        print("rdtftgh")
        f.write(combined_audio)

    # Clean up individual audio chunk files
    for filename in audio_chunks:
        os.remove(filename)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    input_option = request.form.get('inputOption')

    if input_option == 'url':
        url_input = request.form.get('urlInput')
        try:
            r = requests.get(url_input)
            html_content = r.content

            soup = BeautifulSoup(html_content, 'html.parser')
            extracted_text = soup.get_text()

            # Convert text to Devanagari based on the detected script
            detected_script = 'gu'  # Replace with actual script detection result

            if detected_script == 'gu':
                devanagari_text = convert_gurmukhi_to_devanagari(extracted_text)
            elif detected_script == 'bn':
                devanagari_text = convert_bengali_to_devanagari(extracted_text)
            else:
                devanagari_text = extracted_text

            aws_polly_text_to_speech(devanagari_text)
            return f"<h2>Conversion Result</h2><p>Text extracted from URL: {devanagari_text}</p>"

        except requests.exceptions.RequestException as e:
            return f"<h2>Error</h2><p>Failed to fetch URL: {e}</p>"

    else:
        text_input = request.form.get('textInput')
        aws_polly_text_to_speech(text_input)
        return f"<h2>Conversion Result</h2><p>Text input: {text_input}</p>"

if __name__ == '__main__':
    app.run(debug=True)
