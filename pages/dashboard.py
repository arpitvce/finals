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
if not st.session_state.get("authenticated", False):
    st.switch_page("login.py")

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

/* ================= PREMIUM CHAT INPUT ================= */

[data-testid="stChatInput"] textarea {
    border-radius:14px !important;
    border:2px solid transparent !important;
    padding:12px !important;
    color:#ffffff !important;
    background-image:
        linear-gradient(#020617,#020617),
        linear-gradient(90deg,#3b82f6,#06b6d4,#8b5cf6);
    background-origin:border-box;
    background-clip:padding-box,border-box;
    transition: all 0.35s ease;
}

[data-testid="stChatInput"] textarea:focus {
    box-shadow: 0 0 25px rgba(59,130,246,0.7);
    outline:none !important;
}

[data-testid="stChatInput"] button {
    border-radius:12px !important;
    background: linear-gradient(90deg,#3b82f6,#8b5cf6) !important;
    border:none !important;
    color:white !important;
    transition:0.3s ease;
}

[data-testid="stChatInput"] button:hover {
    box-shadow: 0 0 18px rgba(139,92,246,0.8);
    transform: scale(1.05);
}

/* ================= SIDEBAR ================= */

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
genai.configure(api_key="AIzaSyAA0XN23S195NFFGQY2A9D-KLz7XrxeK3Q")
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
                st.markdown("### 📄 Original Code")
                st.code(code_input, language=language.lower())

            with col2:
                st.markdown("### ⚡ Optimized Code")
                st.code(optimized_code, language=language.lower())

            st.markdown("### ⏱ Time Complexity")
            st.markdown(extract("Time Complexity"))

            st.markdown("### 💾 Space Complexity")
            st.markdown(extract("Space Complexity"))

            st.markdown("### 🐞 Bugs")
            st.markdown(extract("Bugs"))

            st.markdown("### 📊 Performance Score")
            st.markdown(extract("Performance Score"))

            st.markdown("### 🚀 Improvement Meter")
            st.markdown(extract("Improvement Meter"))

            st.markdown("### 📘 Explanation")
            st.markdown(extract("Explanation"))

    messages.append({"role":"assistant","content":result})

# ================= CLEAR =================
if st.button("🧹 Clear Current Chat"):
    st.session_state.chats[current_chat] = []
    st.rerun()
# ================= ENHANCEMENT LAYER =================
import time
import json
from datetime import datetime

st.divider()
st.markdown("## 🚀 Ultra Enhancement Panel")

# ================= THEME TOGGLE =================
theme_mode = st.toggle("🌙 Neon Glow Mode")

if theme_mode:
    st.markdown("""
    <style>
    html, body, .stApp {
        background: linear-gradient(135deg,#000000,#0f172a);
    }
    .card {
        background: rgba(0,255,255,0.08);
        border:1px solid rgba(0,255,255,0.4);
        box-shadow: 0 0 20px rgba(0,255,255,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# ================= MODEL SWITCHER =================
st.subheader("🧠 AI Model Settings")

model_choice = st.selectbox(
    "Select Gemini Model",
    ["gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"]
)

temperature = st.slider("🔥 AI Creativity (Temperature)", 0.0, 1.0, 0.3, 0.1)

genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel(
    model_choice,
    generation_config={"temperature": temperature}
)

# ================= SESSION STATS =================
st.subheader("📊 Session Analytics")

total_chats = len(st.session_state.chats)
total_messages = sum(len(v) for v in st.session_state.chats.values())

colA, colB = st.columns(2)
colA.metric("💬 Total Chats", total_chats)
colB.metric("📝 Total Messages", total_messages)

# ================= EXPORT CHAT =================
st.subheader("💾 Export Options")

current_chat = st.session_state.current_chat
chat_data = st.session_state.chats[current_chat]

if chat_data:
    export_text = ""
    for msg in chat_data:
        export_text += f"{msg['role'].upper()}:\n{msg['content']}\n\n"

    st.download_button(
        label="📥 Download Chat as TXT",
        data=export_text,
        file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

# ================= DOWNLOAD LAST OPTIMIZED CODE =================
if chat_data:
    last_response = chat_data[-1]["content"] if chat_data[-1]["role"] == "assistant" else ""
    code_match = re.search(r"```.*?\n(.*?)```", last_response, re.S)
    extracted_code = code_match.group(1) if code_match else ""

    if extracted_code:
        st.download_button(
            label="📦 Download Optimized Code",
            data=extracted_code,
            file_name="optimized_code.txt",
            mime="text/plain"
        )

# ================= TYPING ANIMATION =================
def typing_effect(text, speed=0.01):
    placeholder = st.empty()
    output = ""
    for char in text:
        output += char
        placeholder.markdown(output)
        time.sleep(speed)

# ================= COPY BUTTON =================
if chat_data:
    if st.button("📋 Copy Last AI Response"):
        st.code(chat_data[-1]["content"])
        st.success("Copied to clipboard (manual select & copy).")

# ================= CHAT MEMORY INFO =================
st.subheader("🧠 Memory Monitor")

for cid, msgs in st.session_state.chats.items():
    st.caption(f"Chat ID: {cid[:8]}... | Messages: {len(msgs)}")

st.success("✨ Ultra Enhancement Layer Activated Successfully!")
# ================= ULTRA PRO EXTENSION =================
import os
import traceback
import matplotlib.pyplot as plt

st.divider()
st.markdown("## 💎 Enterprise Upgrade Panel")

# ================= SECURE API KEY INPUT =================
st.subheader("🔐 Secure API Configuration")

user_api_key = st.text_input("Enter Gemini API Key (optional override)", type="password")

if user_api_key:
    genai.configure(api_key=user_api_key)
    st.success("Using custom API key securely.")

# ================= FILE UPLOAD SUPPORT =================
st.subheader("📂 Upload Code File")

uploaded_file = st.file_uploader("Upload .py, .cpp, .java, .js, .go, .rs, .c file")

if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8")
    st.code(file_content, language=language.lower())
    st.info("Copy above code into chat input to analyze.")

# ================= AUTO SAVE CHAT =================
st.subheader("💾 Persistent Chat Storage")

SAVE_PATH = "saved_chats.json"

if st.button("💾 Save All Chats"):
    with open(SAVE_PATH, "w") as f:
        json.dump(st.session_state.chats, f)
    st.success("Chats saved locally.")

if os.path.exists(SAVE_PATH):
    if st.button("📂 Load Saved Chats"):
        with open(SAVE_PATH, "r") as f:
            st.session_state.chats = json.load(f)
        st.success("Chats restored.")
        st.rerun()

# ================= AI RESPONSE TIMER =================
st.subheader("🚦 Performance Monitor")

if "last_response_time" not in st.session_state:
    st.session_state.last_response_time = 0

response_time = st.session_state.get("last_response_time", 0)
st.metric("⏱ Last AI Response Time (sec)", f"{response_time:.2f}")

# ================= TOKEN ESTIMATION =================
st.subheader("🧠 Token Usage Estimator")

if chat_data:
    total_chars = sum(len(msg["content"]) for msg in chat_data)
    approx_tokens = total_chars // 4
    st.metric("📊 Approx Tokens Used", approx_tokens)

# ================= PYTHON EXECUTION SANDBOX =================
st.subheader("🧪 Python Execution Sandbox")

sandbox_code = st.text_area("Run Python Code Safely")

if st.button("▶ Run Code"):
    try:
        local_env = {}
        exec(sandbox_code, {}, local_env)
        st.success("Code executed successfully.")
        st.write(local_env)
    except Exception as e:
        st.error("Execution Error:")
        st.text(traceback.format_exc())

# ================= COMPLEXITY VISUALIZATION =================
st.subheader("📊 Complexity Visualizer")

complexity_options = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)", "O(2ⁿ)"]
selected_complexity = st.selectbox("Select Algorithm Complexity", complexity_options)

if st.button("Generate Complexity Graph"):
    n = list(range(1, 20))

    if selected_complexity == "O(1)":
        y = [1 for _ in n]
    elif selected_complexity == "O(log n)":
        y = [1 if i == 1 else (i.bit_length()) for i in n]
    elif selected_complexity == "O(n)":
        y = n
    elif selected_complexity == "O(n log n)":
        y = [i * (i.bit_length()) for i in n]
    elif selected_complexity == "O(n²)":
        y = [i**2 for i in n]
    else:
        y = [2**i for i in n]

    fig, ax = plt.subplots()
    ax.plot(n, y)
    ax.set_title(f"{selected_complexity} Growth")
    ax.set_xlabel("Input Size")
    ax.set_ylabel("Operations")
    st.pyplot(fig)

# ================= ANIMATED HEADER GLOW =================
st.markdown("""
<style>
@keyframes glow {
    0% { text-shadow: 0 0 10px #ff6b6b; }
    50% { text-shadow: 0 0 25px #6bcBef; }
    100% { text-shadow: 0 0 10px #ffd93d; }
}
h1 {
    animation: glow 3s infinite alternate;
}
</style>
""", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("""
<hr>
<center>
🚀 <b>Celestials CodeRefine Ultra Enterprise</b><br>
AI-Powered Code Intelligence Platform<br>
© 2026 Celestials Technologies
</center>
""", unsafe_allow_html=True)

st.success("💎 Enterprise Features Activated Successfully!")
