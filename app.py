import streamlit as st
import numpy as np
from PIL import Image
import io
import requests

st.title("🧠 AI Object Remover")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)

    st.write("Upload mask (white = remove area)")

    mask_file = st.file_uploader("Upload Mask Image", type=["png"])

    if mask_file:
        mask = Image.open(mask_file).convert("L")
        st.image(mask, caption="Mask", use_column_width=True)

        if st.button("Remove Object"):

            # Convert images to bytes
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")

            mask_bytes = io.BytesIO()
            mask.save(mask_bytes, format="PNG")

            # Call LaMa API (example public endpoint)
            response = requests.post(
                "https://clipdrop-api.co/cleanup/v1",
                files={
                    'image_file': img_bytes.getvalue(),
                    'mask_file': mask_bytes.getvalue()
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
                st.error("Error processing image")
