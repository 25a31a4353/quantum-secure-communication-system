import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Quantum Secure Communication System",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Clean up default Streamlit chrome to give a full-screen native feel
st.markdown(
    """
    <style>
        header[data-testid="stHeader"] {
            display: none !important;
        }
        footer {
            display: none !important;
        }
        #MainMenu {
            visibility: hidden !important;
        }
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            margin: 0 !important;
        }
        [data-testid="stAppViewContainer"] {
            background-color: #020205 !important;
            padding: 0 !important;
        }
        iframe {
            width: 100% !important;
            border: none !important;
            display: block !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

template_path = os.path.join(BASE_DIR, "templates", "index.html")
css_path = os.path.join(BASE_DIR, "static", "style.css")
js_path = os.path.join(BASE_DIR, "static", "script.js")

with open(template_path, "r", encoding="utf-8") as f:
    html_content = f.read()

with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Inline CSS and JS into the template so Streamlit serves the exact localhost experience
html_content = html_content.replace(
    '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'style.css\') }}">',
    f"<style>\n{css_content}\n</style>",
)
html_content = html_content.replace(
    '<script src="{{ url_for(\'static\', filename=\'script.js\') }}"></script>',
    f"<script>\n{js_content}\n</script>",
)

components.html(html_content, height=1050, scrolling=True)
