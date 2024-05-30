import streamlit as st
import cv2
import requests
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.paused = False

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        if not self.paused:
            return img
        else:
            return self.last_frame

    def set_paused(self, paused):
        self.paused = paused
        if paused:
            self.last_frame = self.frame

st.title("Live Video Streaming with Streamlit and Flask")
st.write("Control the video stream and recording options below.")

start_button = st.button("Start Recording")
stop_button = st.button("Stop Recording")
pause_button = st.button("Pause Recording")
resume_button = st.button("Resume")

if start_button:
    requests.get("http://127.0.0.1:5000/start_recording")
    st.success("Started recording")

if stop_button:
    requests.get("http://127.0.0.1:5000/stop_recording")
    st.success("Stopped recording")

if pause_button:
    webrtc_ctx.video_transformer.set_paused(True)
    st.success("Paused recording")

if resume_button:
    webrtc_ctx.video_transformer.set_paused(False)
    st.success("Resumed recording")

webrtc_ctx = webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)
