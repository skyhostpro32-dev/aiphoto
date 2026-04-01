import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io

st.set_page_config(page_title="Mask Tool", layout="centered")

st.title("🖌️ Image Mask Tool")

uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load image safely
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    st.image(image, caption="Original Image", use_column_width=True)

    st.write("Draw over the area you want to mask 👇")

    brush_size = st.slider("Brush Size", 5, 50, 20)

    # ✅ SAFE canvas (fix applied)
    canvas = st_canvas(
        fill_color="rgba(255, 0, 0, 0.4)",
        stroke_width=brush_size,
        stroke_color="red",
        background_image=Image.fromarray(img_array),  # FIX
        update_streamlit=True,
        height=img_array.shape[0],
        width=img_array.shape[1],
        drawing_mode="freedraw",
        key="canvas",
    )

    if canvas.image_data is not None:

        if st.button("Apply Mask"):
            mask_data = canvas.image_data

            # Extract alpha channel as mask
            mask = mask_data[:, :, 3]
            mask = (mask > 0).astype(np.uint8) * 255

            # Convert original image to RGBA
            img_rgba = Image.fromarray(img_array).convert("RGBA")
            img_rgba = np.array(img_rgba)

            # Apply transparency where mask exists
            img_rgba[mask == 255] = [255, 0, 0, 0]

            result = Image.fromarray(img_rgba)

            st.image(result, caption="Masked Result", use_column_width=True)

            # Download
            buf = io.BytesIO()
            result.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Download Image",
                data=byte_im,
                file_name="masked_image.png",
                mime="image/png"
            )
