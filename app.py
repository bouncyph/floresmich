import streamlit as st
import base64

streamlit run app.py --server.headless true --browser.gatherUsageStats false --server.enableCORS false


REQUIRED_NAME = "hojin"
QUESTIONS = [
    {"id": "q1", "type": "info", "text": "Hola, gracias por quererme tanto michelle, no tengo plata para poder comprarte un ramo de flores amarillas tangibles, pero no significa que no te ame. Pulsa siguiente para continuar."},
    {
        "id": "q2",
        "type": "radio",
        "text": "¿Me quieres?",
        "options": ["Sí", "No"],
        "responses": {
            "Sí": "yo te quiero mas mi amor preciosa.",
            "No": "fuck you nigga bitch nigga nigga nigga nigga"
        }
    },
    {"id": "q3", "type": "text", "text": "Escribe el nombre de la persona que amas:"},
    {
        "id": "q4",
        "type": "select",
        "text": "¿Qué te gusta más de mí?",
        "options": ["mi forma de ser", "mi pene", "mi cara", "otro"],
        "responses": {
            "mi forma de ser": "te amo mucho michelle, ya sabia que me amabas por como soy",
            "mi pene": "ay mi cochinita, ya sabia que te gustaba esta, es toda tuya.",
            "mi cara": "te gusto nomas por mi cara entonces?, ok.",
            "otro": "no pues, otro que esperabas."
        }
    },
    {"id": "q5", "type": "final", "text": "Listo: entrega virtual de flores amarillas para michelle"}
]

# --- Inicializar session_state ---
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

init_state()
render_progress()
q = QUESTIONS[st.session_state.idx]

st.title("Flores Amarillas 💛")

# --- Preguntas ---
if q["type"] == "info":
    st.info(q["text"])
    if st.button("Siguiente"):
        change_idx(1)

elif q["type"] == "radio":
    temp_key = f"temp_{q['id']}"
    confirm_key = f"confirm_{q['id']}"
    if temp_key not in st.session_state:
        st.session_state[temp_key] = None
    if confirm_key not in st.session_state:
        st.session_state[confirm_key] = False
    selected = st.radio(
        q["text"],
        q["options"],
        index=0 if st.session_state[temp_key] is None else q["options"].index(st.session_state[temp_key])
    )
    st.session_state[temp_key] = selected
    if not st.session_state[confirm_key]:
        if st.button("Confirmar") and selected is not None:
            st.session_state[q["id"]] = selected
            st.session_state.answers[q["id"]] = selected
            st.session_state[confirm_key] = True
    if st.session_state[confirm_key]:
        response = q["responses"].get(selected, "")
        if response:
            st.success(response)
        if st.button("Siguiente"):
            st.session_state[confirm_key] = False
            change_idx(1)

elif q["type"] == "text":
    if q["id"] not in st.session_state:
        st.session_state[q["id"]] = ""

    st.session_state[q["id"]] = st.text_input(q["text"], value=st.session_state[q["id"]])
    
    if st.button("Siguiente"):
        if st.session_state[q["id"]].strip().lower() == REQUIRED_NAME:
            st.session_state.answers[q["id"]] = st.session_state[q["id"]].strip()
            change_idx(1)
        else:
            st.session_state.error_name = True
    
    if st.session_state.error_name:
        st.error(f"¡Debes escribir el nombre correcto ({REQUIRED_NAME})!")

elif q["type"] == "select":
    temp_key = f"temp_{q['id']}"
    confirm_key = f"confirm_{q['id']}"
    if temp_key not in st.session_state:
        st.session_state[temp_key] = None
    if confirm_key not in st.session_state:
        st.session_state[confirm_key] = False
    selected = st.selectbox(
        q["text"],
        q["options"],
        index=0 if st.session_state[temp_key] is None else q["options"].index(st.session_state[temp_key])
    )
    st.session_state[temp_key] = selected
    if not st.session_state[confirm_key]:
        if st.button("Confirmar") and selected is not None:
            st.session_state[q["id"]] = selected
            st.session_state.answers[q["id"]] = selected
            st.session_state[confirm_key] = True
    if st.session_state[confirm_key]:
        response = q["responses"].get(selected, "")
        if response:
            st.success(response)
        if st.button("Siguiente"):
            st.session_state[confirm_key] = False
            change_idx(1)

elif q["type"] == "final":
    st.success(q["text"])
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
