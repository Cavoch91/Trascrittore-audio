import streamlit as st
import whisper
import os

# Titolo dell'applicazione
st.title("Trascrizione Audio Locale 🎙️")
st.write("Carica un file audio e trascrivilo usando il modello Whisper.")

# Caricamento del modello (viene fatto una sola volta)
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# Widget per caricare il file
uploaded_file = st.file_uploader("Scegli un file audio...", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    # Salva temporaneamente il file caricato
    with open("temp_audio.file", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.audio(uploaded_file)
    
    if st.button("Avvia Trascrizione"):
        with st.spinner("Trascrizione in corso..."):
            try:
                # Esecuzione della trascrizione
                result = model.transcribe("temp_audio.file")
                
                # Visualizzazione risultato
                st.subheader("Testo Trascritto:")
                st.text_area("Risultato", value=result["text"], height=300)
                
                # Opzione download
                st.download_button("Scarica Trascrizione", result["text"], file_name="trascrizione.txt")
            except Exception as e:
                st.error(f"Errore durante la trascrizione: {e}")
            finally:
                # Pulizia file temporaneo
                if os.path.exists("temp_audio.file"):
                    os.remove("temp_audio.file")