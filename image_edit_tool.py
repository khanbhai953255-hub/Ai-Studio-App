import io
from PIL import Image, ImageOps, ImageFilter
import streamlit as st

def run_image_edit_tool():
    st.title("✍️ Image Editor")
    up = st.file_uploader("Image upload", type=["png","jpg","jpeg"])
    if not up:
        st.info("कोई image अपलोड करें.")
        return

    img = Image.open(up).convert("RGB")
    col1, col2 = st.columns(2)
    with col1:
        w = st.number_input("Width", 64, 4096, img.width, step=16)
        h = st.number_input("Height", 64, 4096, img.height, step=16)
        rotate = st.slider("Rotate", -180, 180, 0)
        do_gray = st.checkbox("Grayscale")
        blur = st.slider("Blur", 0, 10, 0)
        flip_h = st.checkbox("Flip Horizontal")
        flip_v = st.checkbox("Flip Vertical")
    with col2:
        # apply
        out = img.resize((int(w), int(h)))
        if rotate:
            out = out.rotate(rotate, expand=True, fillcolor=(0,0,0))
        if do_gray:
            out = ImageOps.grayscale(out).convert("RGB")
        if blur:
            out = out.filter(ImageFilter.GaussianBlur(blur))
        if flip_h:
            out = ImageOps.mirror(out)
        if flip_v:
            out = ImageOps.flip(out)

        st.image(out, caption="Preview", use_container_width=True)
        buf = io.BytesIO()
        out.save(buf, format="PNG")
        st.download_button("⬇️ Download PNG", buf.getvalue(), file_name="edited.png", mime="image/png")
