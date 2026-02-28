import streamlit as st
import base64

st.set_page_config(page_title="Celestials", layout="wide")

# -------------------------
# HIDE STREAMLIT UI
# -------------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# -------------------------
# BACKGROUND FUNCTION
# -------------------------
def set_background(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(
            rgba(0,0,0,0.65),
            rgba(0,0,0,0.65)
        ),
        url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    /* Center container */
    .center-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }}

    /* Glass login card */
    .login-card {{
        backdrop-filter: blur(15px);
        background: rgba(255,255,255,0.08);
        padding: 50px;
        border-radius: 16px;
        width: 380px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        text-align: center;
    }}

    .title {{
        color: white;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }}

    .subtitle {{
        color: rgba(255,255,255,0.8);
        margin-bottom: 30px;
        font-size: 14px;
    }}
    </style>
    """, unsafe_allow_html=True)


set_background("images.jpg")


# -------------------------
# AUTH STATE
# -------------------------
if not st.session_state.get("authenticated", False):
    st.switch_page("login.py")

USERNAME = "arpit"
PASSWORD = "1234"


# -------------------------
# LOGIN UI
# -------------------------
if not st.session_state.authenticated:

    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    st.markdown('<div class="title">Celestials</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Sign in to continue</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if username == USERNAME and password == PASSWORD:
            st.session_state.authenticated = True
            st.switch_page("pages/dashboard.py")
        else:
            st.error("Invalid credentials")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.switch_page("pages/dashboard.py")
