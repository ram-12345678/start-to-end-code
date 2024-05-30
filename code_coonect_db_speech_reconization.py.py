import streamlit as st
from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization")

# Streamlit UI
st.title("Text Summarization App")

# Text input
text = st.text_area("Enter text to summarize:")

# Summarize text
if st.button("Summarize"):
    if text:
        summary = summarizer(text)[0]['summary_text']
        st.success("Summary:")
        st.write(summary)
    else:
        st.warning("Please enter some text to summarize.")
