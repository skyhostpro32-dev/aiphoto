import streamlit as st
from PIL import Image
import numpy as np
import cv2
from rembg import remove
import io

st.set_page_config(page_title="AI Object Remover", layout="centered")

st.title("🧠 AI Person / Object Remover (Stable)")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    st.image(image, caption="Original Image", use_column_width=True)

    if st.button("Remove Person / Object"):
        with st.spinner("Processing... Please wait"):

            # Step 1: Remove background → get mask
            output = remove(image)
            output_np = np.array(output)

            if output_np.shape[2] == 4:
                alpha = output_np[:, :, 3]
            else:
                alpha = cv2.cvtColor(output_np, cv2.COLOR_RGB2GRAY)

            # Step 2: Create mask
            _, mask = cv2.threshold(alpha, 10, 255, cv2.THRESH_BINARY)

            # Step 3: Improve mask (smooth edges)
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.dilate(mask, kernel, iterations=1)

            # Step 4: Inpaint (fill removed area)
            result = cv2.inpaint(img_np, mask, 3, cv2.INPAINT_TELEA)

            result_img = Image.fromarray(result)

        st.image(result_img, caption="Result (Person/Object Removed)", use_column_width=True)

        # Download
        buf = io.BytesIO()
        result_img.save(buf, format="PNG")

        st.download_button(
            "Download Image",
            data=buf.getvalue(),
            file_name="result.png",
            mime="image/png"
        )
