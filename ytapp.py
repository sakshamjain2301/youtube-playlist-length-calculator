import streamlit as st
import yt_dlp
import re

st.title("YouTube Playlist Duration Calculator")

# Create web input fields
url = st.text_input("Enter the YouTube playlist or video URL:")
col1, col2 = st.columns(2)
with col1:
    start_num = st.number_input("Start video number", min_value=1, value=1)
with col2:
    end_num = st.number_input("End video number (Enter 0 to include all remaining)", min_value=0, value=0)

# Helper function to format seconds into exact hours, minutes, and seconds
def format_time(total_seconds):
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    return f"{h} hours, {m} minutes, {s} seconds"

# Create a button to trigger the calculation
if st.button("Calculate"):
    if not url:
        st.warning("Please enter a URL first.")
    else:
        with st.spinner("Calculating..."):
            
            # THE FIX: If the URL contains a playlist ID, extract just the playlist URL
            match = re.search(r'list=([a-zA-Z0-9_-]+)', url)
            if match:
                target_url = f"https://www.youtube.com/playlist?list={match.group(1)}"
            else:
                target_url = url

            ydl_opts = {'extract_flat': True, 'quiet': True}
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(target_url, download=False)
                    
                    if 'entries' not in info:
                        st.info("This is a single video.")
                        st.success(f"Duration: {format_time(info.get('duration', 0))}")
                    else:
                        entries = list(info['entries'])
                        total_videos = len(entries)
                        
                        actual_end = total_videos if end_num == 0 else min(total_videos, end_num)
                        start_idx = max(0, start_num - 1)
                        
                        if start_idx >= actual_end:
                            st.error("Invalid range. Start number must be less than end number.")
                        else:
                            selected_videos = entries[start_idx:actual_end]
                            
                            # Sum the durations, ensuring we handle missing data gracefully
                            total_seconds = sum(v.get('duration', 0) for v in selected_videos if v and v.get('duration'))
                            
                            # Display Normal Speed Result
                            st.success(f"**Total time (1x speed):** {format_time(total_seconds)}")
                            st.write(f"Counted {len(selected_videos)} videos (from index {start_num} to {actual_end}).")
                            
                            # Display Accelerated Speeds
                            st.markdown("### Time at Faster Speeds:")
                            st.info(f"**1.5x speed:** {format_time(total_seconds / 1.5)}")
                            st.info(f"**2.0x speed:** {format_time(total_seconds / 2.0)}")
                            st.info(f"**2.5x speed:** {format_time(total_seconds / 2.5)}")
                            st.info(f"**3.0x speed:** {format_time(total_seconds / 3.0)}")
                            
            except Exception as e:
                st.error(f"An error occurred: {e}")