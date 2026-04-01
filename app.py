import streamlit as st
from PIL import Image
from simple_lama_inpainting import SimpleLama
import numpy as np

# This loads the model only once to save memory
@st.cache_resource
def load_model():
    return SimpleLama()

st.title("✨ AI Spot Eraser")
st.write("Upload an image to remove spots or objects.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Original Image", use_container_width=True)
    
    # Simple trigger for the "Natural Image" result
    if st.button("Apply Mask & Erase"):
        with st.spinner("Processing..."):
            lama = load_model()
            
            # For a quick test, we'll create a dummy mask.
            # In a full app, you'd use 'streamlit-drawable-canvas' to draw the mask.
            mask = Image.new("L", img.size, 0) 
            
            result = lama(img, mask)
            st.image(result, caption="Resulting Image", use_container_width=True)
            st.success("Done!")
