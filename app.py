import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io

st.title("🖌️ Mask Creator Tool")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGBA")

    st.write("Draw mask on image:")

    brush_size = st.slider("Brush Size", 5, 50, 20)

    canvas = st_canvas(
        fill_color="rgba(255, 0, 0, 0.4)",
        stroke_width=brush_size,
        stroke_color="red",
        background_image=image,
        update_streamlit=True,
        height=image.size[1],
        width=image.size[0],
        drawing_mode="freedraw",
        key="canvas",
    )

    if canvas.image_data is not None:

        if st.button("Apply Mask"):

            mask_data = canvas.image_data

            # Extract mask (where user drew)
            mask = mask_data[:, :, 3]  # alpha channel

            mask = (mask > 0).astype(np.uint8) * 255

            # Create transparent masked output
            img_array = np.array(image)

            # Apply mask (make masked area transparent)
            img_array[mask == 255] = [255, 0, 0, 0]

            result = Image.fromarray(img_array)

            st.image(result, caption="Masked Preview", use_column_width=True)

            # Convert to downloadable file
            buf = io.BytesIO()
            result.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="Download Image",
                data=byte_im,
                file_name="masked_image.png",
                mime="image/png"
            )
