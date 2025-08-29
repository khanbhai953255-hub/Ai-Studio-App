import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip
import tempfile, os

def run_video_tool():
    st.title("🎬 Video Maker — Text + Image")

    # Image Upload
    image_file = st.file_uploader("📸 Upload Image", type=["jpg", "jpeg", "png"])
    
    # Text Prompt
    text_prompt = st.text_input("✍️ Enter your video text prompt:")
    
    # Button
    if st.button("🚀 Generate 8 sec Video"):
        if not image_file or not text_prompt:
            st.warning("⚠️ Please upload an image and enter text.")
            return
        
        with st.spinner("⏳ Generating video..."):
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    # Save uploaded image
                    img_path = os.path.join(tmpdir, image_file.name)
                    with open(img_path, "wb") as f:
                        f.write(image_file.read())

                    # Create background image clip
                    img_clip = ImageClip(img_path).set_duration(8).resize(height=720)

                    # Create text overlay
                    txt_clip = (TextClip(text_prompt, fontsize=70, color="white", font="Arial-Bold")
                                .set_duration(8)
                                .set_position(("center", "bottom")))

                    # Final video
                    final = CompositeVideoClip([img_clip, txt_clip])
                    out_path = os.path.join(tmpdir, "output.mp4")
                    final.write_videofile(out_path, fps=24)

                    # Show & Download
                    st.video(out_path)
                    with open(out_path, "rb") as f:
                        st.download_button("⬇️ Download Video", f, file_name="video.mp4", mime="video/mp4")

            except Exception as e:
                st.error(f"❌ Error: {e}")
