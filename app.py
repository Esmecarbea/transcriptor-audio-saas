import streamlit as st
import whisper
import os
from io import BytesIO
import tempfile

# Cargar el modelo de Whisper (usa 'base' para simplicidad y bajo uso de recursos)
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# Título de la app
st.title("Transcriptor de Audio a Español - App SaaS Simple")

# Subir archivo de audio
uploaded_file = st.file_uploader("Sube un archivo de audio (MP3, WAV, M4A, etc.)", type=["mp3", "wav", "m4a", "ogg"])

if uploaded_file is not None:
    # Guardar temporalmente el archivo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_path = temp_file.name
    
    # Transcribir a español
    with st.spinner("Transcribiendo el audio..."):
        result = model.transcribe(temp_path, language="es")
        transcription = result["text"]
    
    # Mostrar la transcripción
    st.subheader("Transcripción en Español:")
    st.text_area("Texto transcrito:", transcription, height=300)
    
    # Exportar a TXT
    txt_data = BytesIO(transcription.encode("utf-8"))
    st.download_button(
        label="Descargar como TXT",
        data=txt_data,
        file_name="transcripcion.txt",
        mime="text/plain"
    )
    
    # Copiar al portapapeles (usando HTML/JS)
    st.subheader("Copiar al portapapeles")
    copy_button = """
    <button onclick="navigator.clipboard.writeText(document.getElementById('transcription').value).then(() => alert('Copiado al portapapeles!'))">
        Copiar texto
    </button>
    <textarea id="transcription" style="display:none;">%s</textarea>
    """ % transcription
    st.components.v1.html(copy_button, height=50)
    
    # Limpiar archivo temporal
    os.remove(temp_path)
else:
    st.info("Sube un archivo de audio para comenzar.")
