#from gtts import gTTS
import pyttsx3
import os
import sys
import re

def read_and_join_lines(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Inizializza una stringa vuota per memorizzare il testo elaborato
    processed_text = ""

    # Itera sulle righe
    for i in range(len(lines)):
        # Se la riga non termina con un punto e la riga successiva inizia con una lettera o un numero
        if i < len(lines) - 1 and not lines[i].endswith('.') and re.match(r'^[A-Za-z0-9]', lines[i+1]):
            # Rimuovi il carattere di nuova riga alla fine della riga e aggiungi uno spazio
            processed_text += lines[i].rstrip('\n') + ' '
        else:
            # Altrimenti, mantieni il carattere di nuova riga
            processed_text += lines[i]

    # Sostituisci "ICS" con "I.C.S." in tutto il testo elaborato
    processed_text = processed_text.replace("ICS", "I.C.S.")

    # Scrivi il testo elaborato nel file di output
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(processed_text)

def text_to_speech_pezzo(text_file, audio_file):
    # Apri il file di testo e leggi il contenuto
    with open(text_file, 'r') as file:
        text = file.read()

    # Dividi il testo in frasi
    sentences = text.split('.')

    # Inizializza un indice per i file audio
    index = 1

    # Inizializza una stringa per il testo corrente
    current_text = ''

    # Itera su ogni frase
    for sentence in sentences:
        # Aggiungi la frase e un punto al testo corrente
        new_text = current_text + sentence + '.'

        # Controlla se il nuovo testo supera il limite di dimensione
        if len(new_text.encode('utf-8')) > 5000:
            # Crea un oggetto gTTS con il testo corrente
            tts = gTTS(text=current_text, lang='it')

            # Salva l'audio della lettura in un file MP3
            tts.save(f'{audio_file}_{index}.mp3')

            # Stampa la dimensione in byte della richiesta
            print(f'Dimensione in byte della richiesta: {len(current_text.encode("utf-8"))}')

            # Incrementa l'indice
            index += 1

            # Imposta il testo corrente alla frase corrente
            current_text = sentence + '.'
        else:
            # Altrimenti, aggiorna il testo corrente
            current_text = new_text

    # Crea un oggetto gTTS con l'ultimo pezzo di testo
    tts = gTTS(text=current_text, lang='it')

    # Salva l'audio della lettura in un file MP3
    tts.save(f'{audio_file}_{index}.mp3')

    # Stampa la dimensione in byte della richiesta
    print(f'Dimensione in byte della richiesta: {len(current_text.encode("utf-8"))}')

    # Unisci tutti i file audio in un unico file
    os.system(f'cat {audio_file}_*.mp3 > {audio_file}')

def text_to_speech(text_file, audio_file):
    # Apri il file di testo e leggi il contenuto
    with open(text_file, 'r') as file:
        text = file.read()

    # Dividi il testo in frasi
    sentences = text.split('.')

    # Inizializza un indice per i file audio
    index = 1

    # Inizializza una stringa per il testo corrente
    current_text = ''

    # Itera su ogni frase
    for sentence in sentences:
        # Aggiungi la frase e un punto al testo corrente
        new_text = current_text + sentence + '.'

        # Controlla se il nuovo testo supera il limite di dimensione
        if len(new_text.encode('utf-8')) > 5000:
            # Crea un oggetto gTTS con il testo corrente
            tts = gTTS(text=current_text, lang='it')

            # Salva l'audio della lettura in un file MP3
            tts.save(f'{audio_file}_{index}.mp3')

            # Stampa la dimensione in byte della richiesta
            print(f'Dimensione in byte della richiesta: {len(current_text.encode("utf-8"))}')

            # Incrementa l'indice
            index += 1

            # Imposta il testo corrente alla frase corrente
            current_text = sentence + '.'
        else:
            # Altrimenti, aggiorna il testo corrente
            current_text = new_text

    # Crea un oggetto gTTS con l'ultimo pezzo di testo
    tts = gTTS(text=current_text, lang='it')

    # Salva l'audio della lettura in un file MP3
    tts.save(f'{audio_file}_{index}.mp3')

    # Stampa la dimensione in byte della richiesta
    print(f'Dimensione in byte della richiesta: {len(current_text.encode("utf-8"))}')

    # Unisci tutti i file audio in un unico file
    os.system(f'cat {audio_file}_*.mp3 > {audio_file}')

def text_to_speech_pyttsx3(text_file, audio_file):
    # Inizializza il motore di sintesi vocale
    engine = pyttsx3.init()

    # Ottieni la velocità attuale
    speed = engine.getProperty('rate')

    # Riduci la velocità (il valore può variare a seconda delle tue esigenze)
    engine.setProperty('rate', speed - 50)

    # Apri il file di testo e leggi il contenuto
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()
        current_text = text

    # Salva l'audio della lettura in un file WAV
    engine.save_to_file(current_text, f'{audio_file}')

    # Esegui la sintesi vocale
    engine.runAndWait()

    # Stampa la dimensione in byte della richiesta
    print(f'Dimensione in byte della richiesta: {len(current_text.encode("utf-8"))}')

if __name__ == "__main__":
    # Controlla se lo script è stato chiamato con i giusti argomenti
    if len(sys.argv) != 3:
        print("Uso: python main.py <file_di_testo> <file_audio>")
        sys.exit(1)

    # Estrai i percorsi del file di testo e del file audio dagli argomenti
    text_file = sys.argv[1]
    audio_file = sys.argv[2]

    # Chiama la funzione per convertire il testo in parlato
    ##text_to_speech(text_file, audio_file)
    ##text_to_speech_pezzo(text_file, audio_file)
    # Chiama la funzione per leggere ed elaborare il testo dal file
    read_and_join_lines(text_file, f'{text_file}_ok.txt')
    text_to_speech_pyttsx3(f'{text_file}_ok.txt', audio_file)

    # python /app/txttomp3.py /app/testo.txt /app/audio.mp3

#    python /app/txttomp3.py /app/515-1_translated_output.txt /app/515-1_translated_output.mp3
#    python /app/txttomp3.py /app/515-2_translated_output.txt /app/515-2_translated_output.mp3
#    python /app/txttomp3.py /app/515-3_translated_output.txt /app/515-3_translated_output.mp3
#    python /app/txttomp3.py /app/515-4_translated_output.txt /app/515-4_translated_output.mp3
#    python /app/txttomp3.py /app/515-workbook_translated_output.txt /app/515-workbook_translated_output.mp3



