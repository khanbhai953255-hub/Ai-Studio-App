import streamlit as st

def run():
    st.header("🎬 Video Tool")
    st.write("यहाँ आप अपने वीडियो से जुड़े काम कर सकते हैं।")

    # Example: यूज़र वीडियो अपलोड करे
    video_file = st.file_uploader("वीडियो अपलोड करें", type=["mp4", "mov", "avi"])
    if video_file:
        st.video(video_file)
        st.success("✅ वीडियो सफलतापूर्वक अपलोड हो गया!")

    # Example: टेक्स्ट इनपुट
    text = st.text_input("वीडियो का टाइटल लिखिए:")
    if text:
        st.info(f"आपने टाइटल लिखा: {text}")import streamlit as st
from PIL import Image
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import numpy as np
import os, tempfile

def pad_to_aspect(im: Image.Image, target_w: int, target_h: int, bg=(0, 0, 0)):
    src_w, src_h = im.size
    target_aspect = target_w / target_h
    src_aspect = src_w / src_h
    if abs(src_aspect - target_aspect) < 1e-3:
        return im.resize((target_w, target_h), Image.LANCZOS)
    if src_aspect > target_aspect:
        new_w = target_w
        new_h = int(round(target_w / src_aspect))
    else:
        new_h = target_h
        new_w = int(round(target_h * src_aspect))
    im_resized = im.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (target_w, target_h), bg)
    x = (target_w - new_w) // 2
    y = (target_h - new_h) // 2
    canvas.paste(im_resized, (x, y))
    return canvas

def make_video_from_images(images, out_path, width, height, fps, sec_per_image, bg_color=(0,0,0), audio_file=None):
    clips = []
    for file in images:
        im = Image.open(file).convert("RGB")
        im = pad_to_aspect(im, width, height, bg=bg_color)
        frame = np.array(im)
        clip = ImageClip(frame).set_duration(sec_per_image)
        clips.append(clip)
    final = concatenate_videoclips(clips, method="compose").set_fps(fps)
    if audio_file:
        try:
            audio = AudioFileClip(audio_file)
            if audio.duration < final.duration:
                loops = int(final.duration // audio.duration) + 1
                audio = concatenate_videoclips([audio] * loops).subclip(0, final.duration)
            else:
                audio = audio.subclip(0, final.duration)
            final = final.set_audio(audio)
        except Exception as e:
            st.warning(f"Audio add failed: {e}")
    final.write_videofile(out_path, fps=fps, codec="libx264", audio_codec="aac")

def run_video_tool():
    st.title("🎬 Video Maker — 9:16 / 16:9")
    col1, col2 = st.columns(2)
    with col1:
        aspect = st.radio("Aspect Ratio", ["9:16 (Vertical)", "16:9 (Horizontal)"], index=0)
        width, height = (1080, 1920) if aspect.startswith("9:16") else (1920, 1080)
        fps = st.slider("FPS", 15, 60, 30)
        sec_per_image = st.slider("Seconds per image", 1, 10, 3)
        bg_hex = st.color_picker("Background (for padding)", "#000000")
        bg_rgb = tuple(int(bg_hex[i:i+2], 16) for i in (1, 3, 5))
    with col2:
        audio = st.file_uploader("Optional background music (mp3/m4a/wav)", type=["mp3","m4a","wav"])
        images = st.file_uploader("Upload images (order by filename)", type=["png","jpg","jpeg"], accept_multiple_files=True)
        st.caption("Tip: फाइल नाम 01, 02, 03… रखें ताकि order सही रहे।")
    if images:
        st.write(f"✅ {len(images)} images selected • Target: **{width}×{height}** • FPS: **{fps}**")
    if st.button("📽️ Create Video", disabled=not images):
        if not images:
            st.warning("पहले images अपलोड करें.")
            return
        with st.spinner("Processing…"):
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    out_path = os.path.join(tmpdir, "output.mp4")
                    audio_path = None
                    if audio:
                        audio_path = os.path.join(tmpdir, audio.name)
                        with open(audio_path, "wb") as f:
                            f.write(audio.read())
                    make_video_from_images(
                        images=sorted(images, key=lambda f: f.name),
                        out_path=out_path, width=width, height=height,
                        fps=fps, sec_per_image=sec_per_image,
                        bg_color=bg_rgb, audio_file=audio_path
                    )
                    with open(out_path, "rb") as f:
                        st.success("✅ Video created!")
                        st.download_button("⬇️ Download MP4", f, file_name="video.mp4", mime="video/mp4")
            except Exception as e:
                st.error(f"Error: {e}")
