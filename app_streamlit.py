import streamlit as st
from ultralytics import YOLO
import numpy as np
import cv2
import base64
from PIL import Image
import json

st.set_page_config(layout="wide")

model = YOLO("best.pt")

# === UI ===
st.title("🪑 Real-time Posture Detector (Streamlit Compatible)")

transparency = st.slider("Overlay Transparency", 0.0, 1.0, 0.4)

placeholder = st.empty()
alert_box = st.empty()

# === Javascript Webcam Streamlit Hook ===
JS = """
<script>
var video = document.createElement('video');
video.width = 640;
video.height = 480;
video.autoplay = true;

navigator.mediaDevices.getUserMedia({video:true}).then(stream=>{
    video.srcObject = stream;
});

var canvas = document.createElement('canvas');
canvas.width = 640;
canvas.height = 480;
var ctx = canvas.getContext('2d');

function capture() {
    ctx.drawImage(video, 0, 0, 640, 480);
    var data = canvas.toDataURL('image/jpeg');
    window.parent.postMessage({type:'capture', data:data}, '*');
}

setInterval(capture, 300);

document.addEventListener("visibilitychange", function() {
    if (document.hidden) {
        window.parent.postMessage({type:'hidden'}, '*');
    }
});

</script>
"""

st.components.v1.html(JS, height=0)

# Temporary storage for JS → Streamlit messages
if "frame" not in st.session_state:
    st.session_state.frame = None
if "tab_hidden" not in st.session_state:
    st.session_state.tab_hidden = False

# Streamlit listener for browser messages
message = st.experimental_get_query_params()

def handle_js_event():
    import streamlit_javascript as st_js # optional

# === MAIN LOOP ===
import streamlit.components.v1 as components

receiver = components.html("""
<script>
window.addEventListener('message', (e)=>{
    if(e.data.type === 'capture'){
        fetch('/_stcore/send?data='+encodeURIComponent(e.data.data));
    }
    if(e.data.type === 'hidden'){
        fetch('/_stcore/hidden');
    }
