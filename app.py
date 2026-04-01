import streamlit as st
from PIL import Image
import base64
import io

st.title("🧠 AI Object Remover (Fabric.js)")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    img_base64 = base64.b64encode(buf.getvalue()).decode()

    img_data = f"data:image/png;base64,{img_base64}"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.2.4/fabric.min.js"></script>
    </head>
    <body style="margin:0;">

    <canvas id="canvas"></canvas>

    <script>
    const canvas = new fabric.Canvas('canvas', {{
        isDrawingMode: true
    }});

    canvas.freeDrawingBrush.color = "white";
    canvas.freeDrawingBrush.width = 20;

    fabric.Image.fromURL("{img_data}", function(img) {{
        canvas.setWidth(img.width);
        canvas.setHeight(img.height);
        canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
    }});

    function sendMask() {{
        const dataURL = canvas.toDataURL("image/png");
        navigator.clipboard.writeText(dataURL);
        alert("Mask copied! Paste below.");
    }}

    const btn = document.createElement("button");
    btn.innerText = "Apply Mask";
    btn.style.position = "fixed";
    btn.style.bottom = "10px";
    btn.style.left = "10px";
    btn.onclick = sendMask;
    document.body.appendChild(btn);

    </script>

    </body>
    </html>
    """

    st.components.v1.html(html, height=600)

    mask_data = st.text_area("Paste Mask Here")

    if st.button("Preview Mask") and mask_data:
        st.success("Mask received ✅")
