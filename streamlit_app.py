# Import de librerias
import streamlit as st
import requests
import base64
import time

# Título de la aplicación
st.title("Generador de Superhéroes")

# Formulario para la creación del prompt
with st.form("form_imagen"):
    # Entrada de texto (por defecto)
    prompt = st.text_input("Prompt", "superhero in Marvel comic style, dynamic action pose")
    # Entrada negativa del texto (por defecto)
    negative_prompt = st.text_input("Negative Prompt", "low quality, blurry")
    # Entrada de pasos para crear la imagen
    steps = st.number_input("Steps", min_value=1, max_value=100, value=20)
    # Entrada de la imaginación de la imagen
    cfg_scale = st.number_input("CFG Scale", min_value=1.0, max_value=20.0, value=7.0)
    # Entrada del ancho
    width = st.number_input("Width", min_value=64, max_value=1024, value=256, step=64)
    # Entrada del alto
    height = st.number_input("Height", min_value=64, max_value=1024, value=256, step=64)
    # Seleccionador del "sampler"
    sampler_index = st.selectbox("Sampler", ["Euler a", "DDIM", "PLMS"])
    # Botón de envío del formulario
    submitted = st.form_submit_button("Generar Héroe")

# Si se ha enviado el formulario
if submitted:
    # URL de la API
    url = "http://host.docker.internal:7860/sdapi/v1/txt2img"
    # Payload de la petición
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": int(steps),
        "cfg_scale": cfg_scale,
        "width": int(width),
        "height": int(height),
        "sampler_index": sampler_index
    }
    
    # Se puede usar un spinner, y opcionalmente mostrar un GIF o una barra de progreso simulado.
    with st.spinner("Generando imagen, por favor espere..."):
        # (Opcional) Mostrar un GIF animado mientras se procesa
        loading_placeholder = st.empty()
        # Reemplaza el siguiente URL por el de tu GIF de carga si lo deseas.
        loading_gif = "https://media.giphy.com/media/y1ZBcOGOOtlpC/giphy.gif"
        loading_placeholder.image(loading_gif, use_container_width=True)
        
        # Simular una barra de progreso (solo es visual, sin feedback real de la API)
        progress_bar = st.progress(0)
        for i in range(0, 101, 10):
            time.sleep(0.1)
            progress_bar.progress(i)
        
        response = requests.post(url, json=payload)
        loading_placeholder.empty()  # Oculta el GIF al completarse la petición

    if response.status_code == 200:
        image_data = base64.b64decode(response.json()["images"][0])
        with open("output.png", "wb") as f:
            f.write(image_data)
        # Centrar la imagen en la página
        st.markdown(
            """
            <style>
            .centered {
                display: flex;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown('<div class="centered">', unsafe_allow_html=True)
        st.image("output.png", caption="Imagen Generada")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

# Pie de página
st.markdown("---")
st.markdown("Especialización en Inteligencia Artificial y Big Data - CPIFP Alan Turing")
st.markdown("© [Pablo García Muñoz](https://www.linkedin.com/in/pablo-garc%C3%ADa-mu%C3%B1oz-a9b2402a9/) y [Hugo Peralta Muñoz](https://github.com/Pykoncio)")


