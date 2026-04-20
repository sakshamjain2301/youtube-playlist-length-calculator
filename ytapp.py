import streamlit as st
import yt_dlp
from datetime import timedelta

st.title("YouTube Playlist Duration Calculator")

# Create web input fields
url = st.text_input("Enter the YouTube playlist or video URL:")
col1, col2 = st.columns(2)
with col1:
    start_num = st.number_input("Start video number", min_value=1, value=1)
with col2:
    end_num = st.number_input("End video number (Enter 0 to include all remaining)", min_value=0, value=0)

# Create a button to trigger the calculation
if st.button("Calculate"):
    if not url:
        st.warning("Please enter a URL first.")
    else:
        with st.spinner("Calculating..."):
            ydl_opts = {'extract_flat': True, 'quiet': True}
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    if 'entries' not in info:
                        st.info("This is a single video.")
                        st.success(f"Duration: {timedelta(seconds=info.get('duration', 0))}")
                    else:
                        entries = list(info['entries'])
                        total_videos = len(entries)
                        
                        actual_end = total_videos if end_num == 0 else min(total_videos, end_num)
                        start_idx = max(0, start_num - 1)
                        
                        if start_idx >= actual_end:
                            st.error("Invalid range.")
                        else:
                            selected_videos = entries[start_idx:actual_end]
                            total_seconds = sum(v['duration'] for v in selected_videos if v and v.get('duration'))
                            
                            st.success(f"**Total time:** {timedelta(seconds=total_seconds)}")
                            st.write(f"Counted {len(selected_videos)} videos (from index {start_num} to {actual_end}).")
            except Exception as e:
                st.error(f"An error occurred: {e}")