import streamlit as st
import whisper
import os

st.set_page_config(page_title="Trascrittore con Barra", page_icon="🎙️")
st.title("🎙️ Trascrizione con Progresso")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

uploaded_file = st.file_uploader("Carica file audio...", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    temp_filename = "temp_audio.mp3"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.audio(uploaded_file)
    
    if st.button("Avvia Trascrizione"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Usiamo un approccio di callback simulato
        # Poiché il metodo nativo di Whisper non espone facilmente una % 
        # su server remoti, aggiorniamo la barra in fasi logiche.
        
        status_text.text("Caricamento modello e audio...")
        progress_bar.progress(10)
        
        # Elaborazione
        status_text.text("Trascrizione in corso (il processo può richiedere tempo)...")
        result = model.transcribe(temp_filename, verbose=False)
        
        progress_bar.progress(100)
        status_text.text("Trascrizione completata!")
        
        st.text_area("Risultato:", value=result["text"], height=300)
        st.download_button("Scarica", result["text"], file_name="trascrizione.txt")
        
        if os.path.exists(temp_filename): os.remove(temp_filename)