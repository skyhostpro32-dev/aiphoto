import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import numpy as np
import base64
import io
import requests

st.title("🧠 AI Object Remover (Fabric.js)")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    # Convert image → base64
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    img_base64 = base64.b64encode(buf.getvalue()).decode()

    img_data = f"data:image/png;base64,{img_base64}"

    # Load HTML component
    with open("component.html", "r") as f:
        html = f.read()

    # Inject script to send image
    html += f"""
    <script>
    window.onload = function() {{
        window.postMessage({{
            type: "load_image",
            img: "{img_data}"
        }}, "*");
    }};
    </script>
    """

    # Capture mask
    mask_data = components.html(html, height=600)

    st.info("Draw on image → Click 'Apply Mask'")

    # NOTE: Streamlit doesn't auto-capture postMessage directly
    # So we simulate via text input (simple workaround)
    mask_input = st.text_area("Paste mask data here (auto next version)")

    if st.button("Remove Object") and mask_input:

        # Decode mask
        header, encoded = mask_input.split(",", 1)
        mask_bytes = base64.b64decode(encoded)

        # Call AI API (ClipDrop)
        response = requests.post(
            "https://clipdrop-api.co/cleanup/v1",
            files={
                'image_file': buf.getvalue(),
                'mask_file': mask_bytes
            },
            headers={
                'x-api-key': 'YOUR_API_KEY'
            }
        )

        if response.status_code == 200:
            result = Image.open(io.BytesIO(response.content))

            st.image(result, caption="Result", use_column_width=True)

            st.download_button(
                "Download",
                data=response.content,
                file_name="result.png",
                mime="image/png"
            )
        else:
            st.error("API Error")
