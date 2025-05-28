import streamlit as st
import cv2
from PIL import Image
import numpy as np
import time
import base64
import os

# Set Streamlit page config
st.set_page_config(page_title="GhostCam", layout="wide", initial_sidebar_state="collapsed")

# Load and encode scary background image
def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

if os.path.exists("scary.jpg"):
    bg_image_base64 = get_base64_of_image("scary.jpg")
else:
    st.error("Missing 'scary.jpg' in the same directory as this script.")
    st.stop()

# Creepy CSS with local scary background
st.markdown(f"""
    <style>
    body {{
        background-color: black;
        color: red;
        font-family: 'Courier New', monospace;
    }}
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    .title {{
        font-size: 50px;
        text-align: center;
        color: crimson;
        animation: flicker 1s infinite;
        margin-top: 20px;
    }}
    @keyframes flicker {{
        0% {{opacity: 1;}}
        50% {{opacity: 0.4;}}
        100% {{opacity: 1;}}
    }}
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>👁️ GhostCam is Watching...</div>", unsafe_allow_html=True)

# Delay for creepy effect
with st.spinner("Capturing your soul..."):
    time.sleep(2)

# Capture image using OpenCV (silently)
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

if ret:
    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display captured image
    st.image(img_rgb, caption="👻 GhostCam has captured your image...", use_container_width=True)
    st.warning("You're being watched. Run... if you still can.", icon="😨")
else:
    st.error("💀 GhostCam failed to capture your image. You're safe... for now.")
