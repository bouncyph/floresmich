import streamlit as st
import base64

# --- CONFIG ---
REQUIRED_NAME = "michelle"
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

# --- Helpers ---
def init_state():
    if "idx" not in st.session_state:
        st.session_state.idx = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "error_name" not in st.session_state:
        st.session_state.error_name = False

def change_idx(delta: int):
    st.session_state.idx = max(0, min(st.session_state.idx + delta, len(QUESTIONS)-1))
    st.session_state.error_name = False

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
    if st.button("Siguiente"):
        if answer.strip().lower() == REQUIRED_NAME:
            st.session_state.answers[q["id"]] = answer.strip()
            change_idx(1)
        else:
            st.session_state.error_name = True
    if st.session_state.error_name:
        st.error("¡Debes escribir el nombre correcto (michelle)!")

elif q["type"] == "select":
    answer = st.selectbox(q["text"], q["options"], key=q["id"])
    if st.button("Siguiente"):
        st.session_state.answers[q["id"]] = answer
        change_idx(1)
        # Mostramos mensaje personalizado según opción
        if answer == "mi forma de ser":
            st.success("¡Aww, tu forma de ser es especial para mí también!")
        elif answer == "mi pene":
            st.success("😏 Jajaja, eres traviesa, pero me gusta tu sinceridad.")
        elif answer == "mi cara":
            st.success("¡Me alegra que te guste mi cara! 😊")
        elif answer == "otro":
            st.success("¡Me gustaría saber qué es ese 'otro' que te gusta de mí!")

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
