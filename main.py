import os
import sys
import re
import pytesseract
from pdf2image import convert_from_path
#from googletrans import Translator
from mtranslate import translate

#import nltk
#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize

#nltk.download('punkt')
#nltk.download('stopwords')

#from sumy.parsers.plaintext import PlaintextParser
#from sumy.nlp.tokenizers import Tokenizer
#from sumy.summarizers.lsa import LsaSummarizer

def translate_with_nltk(input_file, output_file):
    with open(input_file, 'r') as f:
        text = f.read()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('italian'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    translated_text = ' '.join(filtered_tokens)
    sostituisci_testo(translated_text, '© 2021 Robert M. Lee', 'Visibilità, rilevamento e risposta')

    with open(output_file, 'w') as f:
        f.write(translated_text)

    print(f"Testo tradotto con NLTK e salvato in {output_file}")

#def translate_with_sumy(input_file, output_file):
#    with open(input_file, 'r') as f:
#        text = f.read()
#    parser = PlaintextParser.from_string(text, Tokenizer("italian"))
#    summarizer = LsaSummarizer()
#    translated_text = ' '.join([str(sentence) for sentence in summarizer(parser.document, 1)])
#    sostituisci_testo(translated_text, inizio, fine)
#    with open(output_file, 'w') as f:
#        f.write(translated_text)
#    print(f"Testo tradotto con Sumy (LSA) e salvato in {output_file}")

#def translate_text(text, src_lang, dest_lang):
#    try:
#        translated_text = translate(text, dest_lang, src_lang)
#    except Exception as e:
#        print(f"An error occurred during translation: {e}")
#        translated_text = text  # Use the original text if translation fails
#    return translated_text
#from summarizer import Summarizer

def extract_text_from_pdf(pdf_file_path):
    # Convert PDF to images
    images = convert_from_path(pdf_file_path)

    # Initialize an empty string to store extracted text
    extracted_text = ""

    # Extract text from each image using OCR
    for i, img in enumerate(images, start=1):
        text = pytesseract.image_to_string(img, lang="eng")
#        print(f"Processing image {i} of {len(images)}")
#        print(len(text))
        extracted_text += text
    sostituisci_testo(extracted_text, '© 2021 Robert M. Lee', 'Visibilità, rilevamento e risposta')
    return extracted_text

def translate_text(file_path, src_lang, dest_lang):
    # Read the content of the file
    with open(file_path, "r", encoding="utf-8") as text_file:
        text = text_file.read()

    # Split the text into chunks of up to 5000 characters, breaking at the nearest full stop
    chunks = []
    start = 0
    while start < len(text):
        end = start + 5000
        if end < len(text):
            end = text.rfind('.', start, end) + 1
        chunks.append(text[start:end].strip())
        start = end

    # Translate each chunk and join them together
    translated_text = ""
    for chunk in chunks:
        try:
            translated_chunk = translate(chunk, dest_lang, src_lang)
            if not isinstance(translated_chunk, str):
                raise ValueError("Translation did not return a string.")
            # Replace all occurrences
            ##translated_chunk = translated_chunk.replace("© 2021 Robert M. Lee", "")
            ##translated_chunk = translated_chunk.replace("ICS5IS | Visibilità, rilevamento e risposta dell'ICS", "")
            translated_text += translated_chunk
        except Exception as e:
            print(f"An error occurred during translation: {e}")
            translated_text += str(chunk)  # Use the original chunk if translation fails
    mytext = sostituisci_testo(translated_text, '© 2021 Robert M. Lee', 'Visibilità, rilevamento e risposta')
#    print(mytext)
    return mytext

#def summarize_text(text, ratio=0.2):
#    model = Summarizer(model='distilbert-base-uncased')
#    summary = model(text, ratio=ratio)
#    return summary

# Test
inizio = '© 2021 Robert'
fine = 'Visibility, Detection, and Response'
fine1 = 'Visibility , Detection , and Response'

def sostituisci_testo(stringa, inizio, fine):
    pattern = r'{}.*?{}'.format(re.escape(inizio), re.escape(fine))
    nuova_stringa = re.sub(pattern, '', stringa, flags=re.DOTALL)
    return nuova_stringa

#print(sostituisci_testo(s, '© 2021 Robert M. Lee', 'Visibilità, rilevamento e risposta'))


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_pdf_file>")
        sys.exit(1)

    input_pdf_file = sys.argv[1]
    base_name = os.path.splitext(input_pdf_file)[0]

    # Define the output directory
    output_dir = "/app"

    text_file_path = os.path.join(output_dir, f"{base_name}_output.txt")

    # Extract text from PDF
###    extracted_text = extract_text_from_pdf(input_pdf_file)
#    print(f"Text extracted from PDF and saved to {text_file_path}")

    # Write extracted text to a file
#    with open(text_file_path, "w", encoding="utf-8") as text_file:
#        text_file.write(extracted_text)
    translated_text = translate_text(text_file_path, src_lang="en", dest_lang="it")

    translated_file_path = os.path.join(output_dir, f"{base_name}_translated_output.txt")
    with open(translated_file_path, "w", encoding="utf-8") as translated_file:
        translated_file.write(translated_text)
    print(f"Translated text saved to {translated_file_path}")

##    translated_file_path1 = os.path.join(output_dir, f"{base_name}_summarized_output1.txt")
##    translated_file_path2 = os.path.join(output_dir, f"{base_name}_summarized_output2.txt")
##    translate_with_nltk(text_file_path, translated_file_path1)
##    translate_with_sumy(text_file_path, translated_file_path2)

    # Summarize the translated text
#    summarized_text = summarize_text(translated_text, ratio=0.2)
#    summarized_file_path = os.path.join(output_dir, f"{base_name}_summarized_output.txt")
#    with open(summarized_file_path, "w", encoding="utf-8") as summarized_file:
#        summarized_file.write(summarized_text)
#    print(f"Summarized text saved to {summarized_file_path}")

if __name__ == "__main__":
    main()
