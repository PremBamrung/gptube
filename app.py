import re

import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    video_id = None
    # Extract video ID from URL
    regex = r"(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.findall(regex, url)
    if match:
        video_id = match[0]
    return video_id


def extract_subtitles(video_id, language):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return transcript
    except:
        return None


def extract_text(subs):
    text = " ".join([sub["text"] for sub in subs])
    return text


def main():
    st.title("Subtitle Extractor")
    st.write("Enter a YouTube video URL and select the language to extract subtitles:")

    url = st.text_input("YouTube URL:")
    language = st.selectbox(
        "Select Language:", ["English", "Spanish", "French"]
    )  # Add more options if needed

    if st.button("Extract"):
        if url:
            video_id = extract_video_id(url)
            if video_id:
                subtitles = extract_subtitles(video_id, language.lower())
                if subtitles:
                    st.success("Subtitles extracted successfully!")
                    for sub in subtitles:
                        st.write(sub["text"])
                else:
                    st.warning(
                        f"No {language} subtitles found for the given video URL."
                    )
            else:
                st.warning("Invalid YouTube video URL. Please try again.")
        else:
            st.warning("Please enter a valid YouTube video URL.")


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=g-SC1VxwpEw"
    vid_id = extract_video_id(url)
    subs = extract_subtitles(vid_id, language="en")
    txt = extract_text(subs)
    print(txt)
