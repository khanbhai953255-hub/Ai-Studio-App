import io
import requests
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

def _placeholder_image(prompt: str, w=768, h=768):
    img = Image.new("RGB", (w, h), (30, 30, 30))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 24)
    except:
        font = ImageFont.load_default()
    text = f"Prompt:\n{prompt}"
    d.multiline_text((20, 20), text, fill=(240, 240, 240), font=font, spacing=6)
    return img

def run_image_tool():
    st.title("🖼️ Text → Image")
    st.info("फ्री मोड: Placeholder image बनती है. अगर OPENAI_API_KEY हो तो असली जेनरेशन ट्राय होगा (gpt-image-1).")

    prompt = st.text_area("Describe the image you want", height=120, placeholder="e.g. sunset over mountains, cinematic, 4k")
    w = st.slider("Width", 256, 1024, 768, step=64)
    h = st.slider("Height", 256, 1024, 768, step=64)

    if st.button("Generate"):
        api_key = st.secrets.get("OPENAI_API_KEY", None)
        if api_key:
            try:
                # OpenAI Images API (best-effort). If API changes, fallback will trigger.
                headers = {"Authorization": f"Bearer {api_key}"}
                data = {
                    "model": "gpt-image-1",
                    "prompt": prompt or "abstract colorful wallpaper",
                    "size": f"{w}x{h}",
                }
                r = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data, timeout=60)
                if r.ok:
                    b64 = r.json()["data"][0]["b64_json"]
                    import base64
                    img_bytes = base64.b64decode(b64)
                    st.image(img_bytes, caption="Generated")
                    st.download_button("⬇️ Download PNG", img_bytes, file_name="image.png", mime="image/png")
                    return
                else:
                    st.warning(f"Image API error {r.status_code}. Using placeholder.")
            except Exception as e:
                st.warning(f"Image API failed ({e}). Using placeholder.")

        # Fallback: free placeholder
        img = _placeholder_image(prompt or "No prompt", w=w, h=h)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Placeholder")
        st.download_button("⬇️ Download PNG", buf.getvalue(), file_name="image.png", mime="image/png")
