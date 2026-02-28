import streamlit as st
import google.generativeai as genai
import uuid
import re

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Celestials CodeRefine Ultra",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= REDIRECT CHECK =================
if "user" not in st.session_state:
    st.switch_page("login.py")   # change if needed

# ================= PREMIUM CSS =================
st.markdown("""
<style>

html, body {
    background-color:#020617;
    color:#e5e7eb;
    font-family: Inter, system-ui;
}

/* App background */
.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(99,102,241,0.25), transparent 40%),
        radial-gradient(circle at 85% 75%, rgba(20,184,166,0.25), transparent 40%),
        linear-gradient(135deg,#020617,#020617);
}

/* ================= PREMIUM SIDEBAR ================= */

section[data-testid="stSidebar"]{
    background:
        linear-gradient(180deg, rgba(255,255,255,0.10), rgba(255,255,255,0.03));
    backdrop-filter: blur(40px);
    border-right:1px solid rgba(255,255,255,0.18);
    padding-top:16px;
    box-shadow:
        inset -1px 0 0 rgba(255,255,255,0.08),
        8px 0 30px rgba(0,0,0,0.35);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    letter-spacing:-0.3px;
}

section[data-testid="stSidebar"] .stMarkdown h3{
    margin-top:10px;
    font-size:15px;
    opacity:0.9;
    font-weight:600;
}

section[data-testid="stSidebar"] label{
    padding:6px 8px;
    border-radius:10px;
    transition:0.25s;
}

section[data-testid="stSidebar"] label:hover{
    background:rgba(99,102,241,0.18);
    box-shadow:0 0 12px rgba(99,102,241,0.35);
    transform:translateX(2px);
}

section[data-testid="stSidebar"] .stSelectbox{
    margin-bottom:10px;
}

section[data-testid="stSidebar"] button{
    border-radius:12px !important;
    border:1px solid rgba(255,255,255,0.15) !important;
    background:rgba(255,255,255,0.05) !important;
    transition:0.25s !important;
}

section[data-testid="stSidebar"] button:hover{
    transform:translateX(3px);
    box-shadow:0 0 14px rgba(99,102,241,0.45);
}

hr{
    border:0;
    height:1px;
    background:linear-gradient(90deg,transparent,rgba(255,255,255,0.2),transparent);
}

.top-glass{
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(24px);
    border-radius: 26px;
    padding: 1.6rem 2rem;
    border: 1px solid rgba(255,255,255,0.14);
    margin-bottom: 22px;
}

.card{
    padding:18px;
    border-radius:16px;
    background: rgba(255,255,255,0.06);
    border:1px solid rgba(255,255,255,0.12);
    text-align:center;
}

.output-glass{
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(22px);
    border-radius: 20px;
    padding: 1.2rem;
    border: 1px solid rgba(255,255,255,0.16);
    margin-top:10px;
}

</style>
""", unsafe_allow_html=True)

# ================= GEMINI =================
genai.configure(api_key="GET")
model = genai.GenerativeModel("gemini-2.5-flash")

# ================= SESSION =================
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    cid = str(uuid.uuid4())
    st.session_state.chats[cid] = []
    st.session_state.current_chat = cid

# ================= SIDEBAR =================
with st.sidebar:
    st.title("⚙ Control Panel")

    language = st.selectbox("Language", ["Python","C++","Java","JavaScript","C","Go","Rust"])

    st.divider()

    detect_bugs = st.checkbox("🐞 Bug Detection", True)
    explain = st.checkbox("📘 Explanation", True)
    score_mode = st.checkbox("📊 Performance Score", True)
    time_complex = st.checkbox("⏱ Time Complexity", True)
    space_complex = st.checkbox("💾 Space Complexity", True)
    improvement_meter = st.checkbox("🚀 Improvement Meter", True)

    st.divider()
    st.subheader("💬 Chats")

    for index, cid in enumerate(list(st.session_state.chats.keys())):
        col1, col2 = st.columns([4,1])

        if col1.button(f"Chat {index+1}", key=f"chat_{cid}"):
            st.session_state.current_chat = cid

        if col2.button("🗑", key=f"delete_{cid}"):
            del st.session_state.chats[cid]
            if st.session_state.chats:
                st.session_state.current_chat = list(st.session_state.chats.keys())[0]
            else:
                new_id = str(uuid.uuid4())
                st.session_state.chats[new_id] = []
                st.session_state.current_chat = new_id
            st.rerun()

    if st.button("➕ New Chat"):
        cid = str(uuid.uuid4())
        st.session_state.chats[cid] = []
        st.session_state.current_chat = cid
        st.rerun()

# ================= HERO =================
st.markdown("<div class='top-glass'>", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center;font-size:40px;
background: linear-gradient(90deg,#ff6b6b,#ffd93d,#6bcBef);
-webkit-background-clip:text;color:transparent;'>
🚀 Celestials CodeRefine Ultra
</h1>
<p style='text-align:center;opacity:0.8'>
Next-gen AI Code Review & Optimization Engine
</p>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
c1.markdown("<div class='card'>⚡ Instant Optimization</div>", unsafe_allow_html=True)
c2.markdown("<div class='card'>🧠 AI Intelligence</div>", unsafe_allow_html=True)
c3.markdown("<div class='card'>🔒 Secure Review</div>", unsafe_allow_html=True)
c4.markdown("<div class='card'>📊 Performance Insights</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ================= CHAT =================
current_chat = st.session_state.current_chat
messages = st.session_state.chats[current_chat]

if not messages:
    st.info("👋 Paste your code below to start AI optimization.")

for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

code_input = st.chat_input("Paste code for AI review...")

# ================= PROCESS =================
if code_input:
    messages.append({"role":"user","content":code_input})

    prompt = f"""
You are CodeRefine Ultra.

Analyze this {language} code:

{code_input}

STRICT FORMAT:

### Optimized Code
(code only inside triple backticks, no comments)

### Time Complexity
### Space Complexity
### Bugs
### Performance Score
### Improvement Meter
### Explanation
"""

    with st.chat_message("assistant"):
        with st.spinner("AI optimizing code..."):
            response = model.generate_content(prompt)
            result = response.text if hasattr(response,"text") else str(response)

            def extract(title):
                m = re.search(rf"### {title}\s*(.*?)(?=\n### |\Z)", result, re.S)
                return m.group(1).strip() if m else ""

            optimized_match = re.search(r"### Optimized Code.*?```.*?\n(.*?)```", result, re.S)
            optimized_code = optimized_match.group(1).strip() if optimized_match else ""

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("<div class='output-glass'>", unsafe_allow_html=True)
                st.markdown("### 📄 Original Code")
                st.code(code_input, language=language.lower())
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='output-glass'>", unsafe_allow_html=True)
                st.markdown("### ⚡ Optimized Code")
                st.code(optimized_code, language=language.lower())
                st.markdown("</div>", unsafe_allow_html=True)

            if time_complex:
                st.markdown("<div class='output-glass'>", unsafe_allow_html=True)
                st.markdown("### ⏱ Time Complexity")
                st.markdown(extract("Time Complexity"))
                st.markdown("</div>", unsafe_allow_html=True)

            if space_complex:
                st.markdown("<div class='output-glass'>", unsafe_allow_html=True)
                st.markdown("### 💾 Space Complexity")
                st.markdown(extract("Space Complexity"))
                st.markdown("</div>", unsafe_allow_html=True)

            if detect_bugs:
                st.markdown("<div class='output-glass'>", unsafe_allow_html=True)
                st.markdown("### 🐞 Bugs")
                st.markdown(extract("Bugs"))
                st.markdown("</div>", unsafe_allow_html=True)

            if score_mode:
                st.markdown("<div class='output-glass'>", unsafe_allow_html=True)
                st.markdown("### 📊 Performance Score")
                st.markdown(extract("Performance Score"))
                st.markdown("</div>", unsafe_allow_html=True)

            if improvement_meter:
                st.markdown("<div class='output-glass'>", unsafe_allow_html=True)
                st.markdown("### 🚀 Improvement Meter")
                st.markdown(extract("Improvement Meter"))
                st.markdown("</div>", unsafe_allow_html=True)

            if explain:
                st.markdown("<div class='output-glass'>", unsafe_allow_html=True)
                st.markdown("### 📘 Explanation")
                st.markdown(extract("Explanation"))
                st.markdown("</div>", unsafe_allow_html=True)

    messages.append({"role":"assistant","content":result})

# ================= CLEAR =================
if st.button("🧹 Clear Current Chat"):
    st.session_state.chats[current_chat] = []
    st.rerun()
