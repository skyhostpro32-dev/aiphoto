import io
import base64
from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
from simple_lama_inpainting import SimpleLama

app = Flask(__name__)
model = SimpleLama()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/erase', methods=['POST'])
def erase():
    data = request.json
    # Decode the base64 image and mask
    image_data = base64.b64decode(data['image'].split(',')[1])
    mask_data = base64.b64decode(data['mask'].split(',')[1])

    img = Image.open(io.BytesIO(image_data)).convert("RGB")
    mask = Image.open(io.BytesIO(mask_data)).convert("L")

    # The AI magic happens here
    result = model(img, mask)

    # Convert back to base64 to send to frontend
    buffered = io.BytesIO()
    result.save(buffered, format="PNG")
    encoded_res = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return jsonify({'result': 'data:image/png;base64,' + encoded_res})

if __name__ == '__main__':
    app.run(port=5000)
