import streamlit as st

from utils import generate_video_script

st.title("Video script generator")

with st.sidebar:
    api_key = st.text_input("Enter your OpenAI API key to get started:", type="password")

subject = st.text_input("Enter the main topic of your video:")
video_duration = st.number_input("Enter the duration of the video (in minutes):", min_value=0.1, step=0.1)
creativity = st.slider("Adjust the creativity for your video script (larger number means higher creativity):",
                       min_value=0.0, step=0.1, max_value=1.0, value=0.7)
st.divider()
submitted = st.button("Generate your script!")

if submitted and not api_key:
    st.info("API key is missing!")
    st.stop()
if submitted and not subject:
    st.info("Video subject is missing!")
    st.stop()
if submitted:
    with st.spinner("Generating something amazing for you..."):
        try:
            title, script, search_result = generate_video_script(subject, video_duration, creativity, api_key)
        except:
            st.error("Some error occurred. Please check your api key and/or your billing plan.")
            st.stop()
    st.success("Generated successfully!")
    st.subheader("Title:")
    st.write(title)
    st.subheader("Script:")
    st.write(script)
