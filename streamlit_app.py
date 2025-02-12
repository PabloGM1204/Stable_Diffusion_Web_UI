import streamlit as st
import requests
import base64
import time
from tqdm import tqdm
import os
from datetime import datetime

st.title("Generador de Superhéroes")

with st.form("form_imagen"):
    st.header("🔧 Configuración de Imagen")
    prompt = st.text_area("Descripción del Héroe", "superhero in Marvel comic style, dynamic action pose")
    negative_prompt = st.text_area("Elementos No Deseados de la Imagen", "low quality, blurry")
    steps = st.slider("Pasos de Generación", min_value=1, max_value=100, value=20)
    cfg_scale = st.slider("Escala CFG", min_value=1.0, max_value=20.0, value=7.0)
    col1, col2 = st.columns(2)
    with col1:
        width = st.selectbox("Ancho de la imagen a generar", [64, 128, 256, 512, 1024], index=2)
    with col2:
        height = st.selectbox("Alto de la imagen a generar", [64, 128, 256, 512, 1024], index=2)

    sampler_index = st.selectbox("Algoritmo de Muestreo", ["Euler A", "DDIM", "PLMS"])
    submitted = st.form_submit_button("🚀 Generar Héroe")

if submitted:
    # URL de la API
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": int(steps),
        "cfg_scale": cfg_scale,
        "width": int(width),
        "height": int(height),
        "sampler_index": sampler_index
    }
    
    with st.spinner("Generando imagen, por favor espere..."):
        loading_placeholder = st.empty()
        loading_gif = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHFpeWhsOGlrMjdnbHRkdW43bnRpcXhmZXhhNnZkNXlxNGYweGVxciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xTkcEQACH24SMPxIQg/giphy.gif"
        loading_placeholder.image(loading_gif, width=300)

        # Realiza la solicitud a la API
        response = requests.post(url, json=payload)

    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        # Guarda el contenido JSON de la respuesta en una variable
        response_data = response.json()  # Asegúrate de consumir el JSON completo aquí

        # Decodifica la imagen generada (en base64) y la guarda en un archivo PNG
        image_data = base64.b64decode(response_data["images"][0])  # Decodifica la imagen
        output_dir = "generated_samples"  # Carpeta para guardar las imágenes
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Asigna un nombre único basado en la fecha/hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"hero_{timestamp}.png"
        image_path = os.path.join(output_dir, image_filename)

        with open(image_path, "wb") as f:
            f.write(image_data)  # Guarda la imagen en disco
        
        # Muestra la imagen generada en la interfaz de usuario
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        st.image(image_path, caption="Imagen Generada")
        # Agrega un botón para descargar la imagen generada
        st.download_button("📥 Descargar Imagen", data=open(image_path, "rb").read(), file_name=image_filename, mime="image/png")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # En caso de error, muestra un mensaje con el código y el texto del error
        st.error(f"❌ Error: {response.status_code} - {response.text}")


# Pie de página
st.markdown("---")
st.markdown("Especialización en Inteligencia Artificial y Big Data - CPIFP Alan Turing")
st.markdown("© [Pablo García Muñoz](https://www.linkedin.com/in/pablo-garc%C3%ADa-mu%C3%B1oz-a9b2402a9/) y [Hugo Peralta Muñoz](https://github.com/Pykoncio)")


