import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io

st.set_page_config(page_title="Mask Tool", layout="centered")

st.title("🖌️ Image Mask Tool (Stable Version)")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    st.image(image, caption="Original Image", use_column_width=True)

    st.write("Draw mask below (same area approx) 👇")

    brush_size = st.slider("Brush Size", 5, 50, 20)

    canvas_size = 400  # fixed safe canvas size

    canvas = st_canvas(
        fill_color="rgba(255, 0, 0, 0.4)",
        stroke_width=brush_size,
        stroke_color="red",
        background_color="white",  # ✅ no background_image → no crash
        height=canvas_size,
        width=canvas_size,
        drawing_mode="freedraw",
        key="canvas",
    )

    if canvas.image_data is not None:

        if st.button("Apply Mask"):

            # Get mask from canvas
            mask = canvas.image_data[:, :, 3]
            mask = (mask > 0).astype(np.uint8) * 255

            # Resize mask to match image
            mask_img = Image.fromarray(mask).resize((image.width, image.height))
            mask = np.array(mask_img)

            # Convert image to RGBA
            img_rgba = image.convert("RGBA")
            img_rgba = np.array(img_rgba)

            # Apply transparency
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
                file_name="masked.png",
                mime="image/png"
            )
