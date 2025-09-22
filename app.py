import streamlit as st
import base64

# --- CONFIG ---
REQUIRED_NAME = "hojin"
QUESTIONS = [
    {"id": "q1", "type": "info", "text": "Hola, gracias por quererme tanto. Pulsa siguiente para continuar."},
    {"id": "q2", "type": "radio", "text": "¿Me quieres?", "options": ["Sí", "No"]},
    {"id": "q3", "type": "text", "text": "Escribe el nombre de la persona que amas:"},
    {"id": "q4", "type": "select", "text": "¿Cuál de estas cosas te gusta más de mí?", "options": ["Mi risa", "Mi forma de ser", "Mi apoyo", "Otra"]},
    {"id": "q5", "type": "final", "text": "Listo: entrega virtual de flores amarillas"}
]

# --- Helpers ---
def init_state():
    if "idx" not in st.session_state: st.session_state.idx = 0
    if "answers" not in st.session_state: st.session_state.answers = {}
    if "error_name" not in st.session_state: st.session_state.error_name = False

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

# --- App UI ---
st.set_page_config(page_title="Flores Amarillas para Michelle", layout="centered")
init_state()

st.title("🌼 Flores Amarillas — Interactivo")
st.write("Mini-test interactivo para dedicar flores virtuales a Michelle. ¡Hazlo con cariño!")
render_progress()

q = QUESTIONS[st.session_state.idx]
st.markdown(f"### {q['text']}")

# --- Inputs dinámicos ---
response = None
if q["type"] == "info":
    st.write("Solo sigue las preguntas hasta el final.")
elif q["type"] == "radio":
    response = st.radio("Elige una opción:", q["options"], index=0)
elif q["type"] == "select":
    response = st.selectbox("Selecciona:", q["options"], index=0)
elif q["type"] == "text":
    response = st.text_input("Escribe aquí:")

# --- Botones de navegación ---
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("Atrás"): change_idx(-1)
with col2:
    if st.button("Siguiente"):
        if response is not None: st.session_state.answers[q["id"]] = response
        change_idx(1)
with col3:
    if st.button("Reiniciar"): reset_all()

# --- Página final ---
if q["type"] == "final":
    st.markdown("---")
    given_name = st.session_state.answers.get("q3", "").strip().lower()
    
    if not given_name:
        st.warning("Aún no has escrito el nombre de la persona que amas. Ve atrás e ingrésalo.")
    elif given_name != REQUIRED_NAME:
        st.session_state.error_name = True
        st.error("El nombre que escribiste NO coincide con el nombre requerido. Intenta de nuevo.")
        if st.button("Volver y corregir"): st.session_state.idx = 2
    else:
        st.success(f"El nombre '{st.session_state.answers.get('q3')}' fue verificado ✅")
        st.balloons()

        # Cargar imagen en base64 para incrustarla en HTML
        with open("0990ee99212269f82854ed4a978ece63.jpg", "rb") as f:
            img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode()

        # Mostrar la imagen en lugar de las flores CSS
        st.markdown(f"""
        <div style="text-align:center; margin-top:20px;">
            <h3>🌼 Flores amarillas para {st.session_state.answers.get('q3')} 🌼</h3>
            <img src="data:image/jpeg;base64,{img_b64}" 
                 alt="Flores amarillas" 
                 style="width:300px; border-radius:15px; box-shadow:0 4px 8px rgba(0,0,0,0.2);">
        </div>
        """, unsafe_allow_html=True)

        if st.button("Volver a empezar ❤️"): reset_all()

# --- Footer ---
st.markdown("---")
st.caption("Hecho con Streamlit. Personaliza las preguntas en QUESTIONS.")
