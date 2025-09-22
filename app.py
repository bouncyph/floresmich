import streamlit as st
import base64

# --- CONFIG ---
REQUIRED_NAME = "hojin"
QUESTIONS = [
    {"id": "q1", "type": "info", "text": "Hola, gracias por quererme tanto. Pulsa siguiente para continuar."},
    {"id": "q2", "type": "radio", "text": "¿Me quieres?", "options": ["Sí", "No"]},
    {"id": "q3", "type": "text", "text": "Escribe el nombre de la persona que amas:"},
    {
        "id": "q4", "type": "select", "text": "¿Cuál de estas cosas te gusta más de mí?",
        "options": ["mi forma de ser", "mi pene", "mi cara", "otro"]
    },
    {"id": "q5", "type": "final", "text": "Listo: entrega virtual de flores amarillas para michelle"}
]

# Respuestas personalizadas para la pregunta select
PERSONALIZED_RESPONSES = {
    "mi forma de ser": "te amo mucho michelle, ya sabia que me amabas por como soy",
    "mi pene": "ay mi cochinita, ya sabia que te gustaba esta, es toda tuya.",
    "mi cara": "te gusto nomas por mi cara entonces?, ok.",
    "otro": "no pues, otro que esperabas."
}

# --- Helpers ---
def init_state():
    if "idx" not in st.session_state:
        st.session_state.idx = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "error_name" not in st.session_state:
        st.session_state.error_name = False
    if "select_response" not in st.session_state:
        st.session_state.select_response = ""

def change_idx(delta: int):
    st.session_state.idx = max(0, min(st.session_state.idx + delta, len(QUESTIONS)-1))
    st.session_state.error_name = False
    st.session_state.select_response = ""

def reset_all():
    st.session_state.clear()
    init_state()

def render_progress():
    pct = int((st.session_state.idx / (len(QUESTIONS)-1)) * 100)
    st.progress(pct)
    st.caption(f"Progreso: {pct}%")

# --- App ---
init_state()
render_progress()

q = QUESTIONS[st.session_state.idx]

st.title("Flores Amarillas 💛")

if q["type"] == "info":
    st.info(q["text"])
    if st.button("Siguiente"):
        change_idx(1)

elif q["type"] == "radio":
    answer = st.radio(q["text"], q["options"], key=q["id"])
    if st.button("Siguiente"):
        st.session_state.answers[q["id"]] = answer
        change_idx(1)

elif q["type"] == "text":
    answer = st.text_input(q["text"], key=q["id"])
    # El botón "Siguiente" registra el nombre sin necesidad de presionar enter.
    if st.button("Siguiente"):
        if answer.strip().lower() == REQUIRED_NAME:
            st.session_state.answers[q["id"]] = answer.strip()
            change_idx(1)
        else:
            st.session_state.error_name = True
    if st.session_state.error_name:
        st.error("¡Debes escribir el nombre correcto (hojin)!")

elif q["type"] == "select":
    answer = st.selectbox(q["text"], q["options"], key=q["id"])
    # Al dar click en "Siguiente", muestra la respuesta personalizada abajo
    if st.button("Siguiente"):
        st.session_state.answers[q["id"]] = answer
        st.session_state.select_response = PERSONALIZED_RESPONSES.get(answer, "")
        change_idx(1)
    # Si ya hay una respuesta personalizada, la mostramos
    if st.session_state.select_response:
        st.success(st.session_state.select_response)

elif q["type"] == "final":
    st.success(q["text"])
    # Mostrar imagen si existe en la raíz
    try:
        with open("0990ee99212269f82854ed4a978ece63.jpg", "rb") as f:
            img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode()
        st.markdown(f"""
            <div style="text-align:center; margin-top:20px;">
                <img src="data:image/jpeg;base64,{img_b64}" 
                alt="Flores amarillas" 
                style="width:300px; border-radius:15px; box-shadow:0 4px 8px rgba(0,0,0,0.2);">
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.warning("No se pudo cargar la imagen de flores amarillas.")

    if st.button("Reiniciar"):
        reset_all()
