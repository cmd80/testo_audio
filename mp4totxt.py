# Importare le librerie necessarie
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import sys

# Definire una funzione per trascrivere il file audio
def transcribe_audio(audio_path, text_path):
    # Caricare il file audio
    audio = AudioSegment.from_file(audio_path)

    # Suddividere il file audio in segmenti
    chunks = split_on_silence(audio, min_silence_len=500, silence_thresh=-30)

    # Inizializzare il riconoscitore
    r = sr.Recognizer()

    # Aprire il file di testo in modalità di scrittura
    with open(text_path, 'w') as f:
        # Iterare su ogni segmento
        for i, chunk in enumerate(chunks):
            # Salvare il segmento come file audio temporaneo
            chunk.export("temp.wav", format="wav")

            # Caricare il file audio temporaneo
            with sr.AudioFile("temp.wav") as source:
                # Leggere il file audio
                audio_listened = r.record(source)

                # Tentare di riconoscere il discorso nel file audio
                try:
                    text = r.recognize_google(audio_listened, language='it-IT')
                except sr.UnknownValueError as e:
                    print("Errore:", str(e))
                else:
                    # Scrivere il testo riconosciuto nel file di testo
                    f.write(text + "\\n")

# Prendere il percorso del file audio come primo argomento dello script
audio_path = sys.argv[1]

# Prendere il percorso del file di testo come secondo argomento dello script
text_path = sys.argv[2]

# Chiamare la funzione per trascrivere l'audio
transcribe_audio(audio_path, text_path)

# Stampare un messaggio di successo
print("Il video è stato trascritto con successo nel file di testo.")

#### python /app/main.py /app/video.mp4 /app/transcription.txt