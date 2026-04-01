import streamlit as st
from PIL import Image
from simple_lama_inpainting import SimpleLama
import numpy as np

# Initialize the model
@st.cache_resource
def load_model():
    return SimpleLama()

lama = load_model()

st.title("AI Spot Eraser")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Original Image", use_container_width=True)
    
    # In a real app, you'd use a canvas component here. 
    # For a quick test, we can use a placeholder or logic to apply a mask.
    if st.button("Apply Mask & Erase"):
        # Note: For a true "draw-on-image" experience in Streamlit, 
        # you would need the 'streamlit-drawable-canvas' library.
        st.write("Processing...")
        
        # Dummy mask for demonstration (usually you'd get this from a canvas)
        mask = Image.new("L", img.size, 0) 
        
        # Run Inpainting
        result = lama(img, mask)
        st.image(result, caption="Natural Image", use_container_width=True)
