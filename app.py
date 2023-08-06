import re
from io import BytesIO

import pytube
import requests
import streamlit as st
from PIL import Image
from streamlit_chat import message
from youtube_transcript_api import YouTubeTranscriptApi

st.cache_data()


def extract_video_id(url):
    video_id = None
    # Extract video ID from URL
    regex = r"(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.findall(regex, url)
    if match:
        video_id = match[0]
    return video_id


st.cache_data()


def extract_subtitles(video_id, language):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return transcript
    except:
        return None


def extract_text(subs):
    text = " ".join([sub["text"] for sub in subs])
    return text


st.cache_data()


def extract_thumbnail(vid_id):
    thumbnail_url = f"https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg"
    try:
        response = requests.get(thumbnail_url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        st.write("Error displaying thumbnail.")


st.cache_data()


def extract_video_info(video_url):
    try:
        yt = pytube.YouTube(video_url)
        video_info = {
            "title": yt.title,
            "channel": yt.author,
            "date": yt.publish_date.date(),
            "views": yt.views,
            # 'comments': yt.embed_html
        }
        # # Get number of subscribers
        # channel_url = f"https://www.youtube.com/channel/{yt.channel_id}"
        # channel = pytube.Channel(channel_url)
        # video_info['subscribers'] = channel.subscriber_count
        return video_info
    except Exception as e:
        print(e)
        return None


def main():
    st.title("GPTube")
    st.write("Enter a YouTube video URL and select the language to extract subtitles:")

    url = st.text_input("YouTube URL:")
    language = st.selectbox(
        "Select Language:", ["en", "fr"]
    )  # Add more options if needed

    if st.button("Extract"):
        if url:
            video_id = extract_video_id(url)
            video_info = extract_video_info(url)
            if video_id:
                subtitles = extract_subtitles(video_id, language.lower())
                if subtitles:
                    text = extract_text(subtitles)
                    if text:
                        st.success("Subtitles extracted successfully!")
                        col1, col2 = st.columns(2)
                        with col1:
                            img_thumbnail = extract_thumbnail(video_id)
                            st.subheader(video_info["title"])
                            st.image(img_thumbnail)
                            st.text(
                                video_info["channel"] + " " + str(video_info["date"])
                            )
                            st.text(f"Words count : {len(text.split())}")
                            with st.expander("See full text"):
                                st.write(text)
                        with col2:
                            message("My message")
                            message("Hello bot!", is_user=True)
                else:
                    st.warning(
                        f"No {language} subtitles found for the given video URL."
                    )
            else:
                st.warning("Invalid YouTube video URL. Please try again.")
        else:
            st.warning("Please enter a valid YouTube video URL.")


if __name__ == "__main__":
    # url = "https://www.youtube.com/watch?v=g-SC1VxwpEw"
    # vid_id = extract_video_id(url)
    # subs = extract_subtitles(vid_id, language="en")
    # txt = extract_text(subs)
    # print(txt)

    main()
