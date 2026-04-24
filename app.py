import streamlit as st
import whisper
import os
from pydub import AudioSegment

st.set_page_config(page_title="Trascrittore Dinamico", page_icon="🎙️")
st.title("🎙️ Trascrittore Audio con Avanzamento Reale")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

uploaded_file = st.file_uploader("Carica un file audio...", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    temp_filename = "temp_audio.mp3"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.audio(uploaded_file)
    
    if st.button("Avvia Trascrizione"):
        # Carica audio e dividilo in segmenti di 30 secondi
        audio = AudioSegment.from_file(temp_filename)
        chunk_length_ms = 30000 
        chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        full_text = []
        
        # Elabora ogni blocco
        for i, chunk in enumerate(chunks):
            # Aggiorna la UI
            percent = int(((i + 1) / len(chunks)) * 100)
            progress_bar.progress(percent)
            status_text.text(f"Trascrizione segmento {i+1} di {len(chunks)} ({percent}%)")
            
            # Salva il pezzetto temporaneo
            chunk.export("temp_chunk.mp3", format="mp3")
            
            # Trascrivi
            result = model.transcribe("temp_chunk.mp3", verbose=False)
            full_text.append(result["text"])
            
        # Unisci tutto
        final_text = " ".join(full_text)
        
        st.success("Trascrizione completata!")
        st.text_area("Risultato:", value=final_text, height=300)
        st.download_button("Scarica", final_text, file_name="trascrizione.txt")
        
        # Pulizia
        if os.path.exists("temp_audio.mp3"): os.remove("temp_audio.mp3")
        if os.path.exists("temp_chunk.mp3"): os.remove("temp_chunk.mp3")