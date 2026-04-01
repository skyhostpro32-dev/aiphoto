import streamlit as st
import numpy as np
from PIL import Image
import torch
import cv2

# SAM
from segment_anything import sam_model_registry, SamPredictor

# Stable Diffusion Inpainting
from diffusers import StableDiffusionInpaintPipeline

st.title("🧠 Ultra AI Object Remover (SAM + SD)")

# Load models (cache for speed)
@st.cache_resource
def load_models():
    # SAM model
    sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b.pth")
    predictor = SamPredictor(sam)

    # Stable Diffusion Inpainting
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting",
        torch_dtype=torch.float32
    )

    return predictor, pipe

predictor, pipe = load_models()

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    st.image(image, caption="Original Image")

    st.write("👉 Click approximate center of object to remove")

    x = st.number_input("X coordinate", 0, img_np.shape[1], 100)
    y = st.number_input("Y coordinate", 0, img_np.shape[0], 100)

    if st.button("Remove Object"):
        with st.spinner("AI working..."):

            # --- SAM Mask ---
            predictor.set_image(img_np)
            input_point = np.array([[x, y]])
            input_label = np.array([1])

            masks, _, _ = predictor.predict(
                point_coords=input_point,
                point_labels=input_label,
                multimask_output=False,
            )

            mask = masks[0].astype(np.uint8) * 255

            # --- Stable Diffusion Inpainting ---
            mask_pil = Image.fromarray(mask).convert("L")

            result = pipe(
                prompt="clean background",
                image=image,
                mask_image=mask_pil
            ).images[0]

        st.image(result, caption="Removed + AI Filled")

        # Download
        import io
        buf = io.BytesIO()
        result.save(buf, format="PNG")

        st.download_button(
            "Download",
            data=buf.getvalue(),
            file_name="ai_removed.png",
            mime="image/png"
        )
