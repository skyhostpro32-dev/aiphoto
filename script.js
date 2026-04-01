const canvas = new fabric.Canvas('canvas', {
    isDrawingMode: true
});

canvas.freeDrawingBrush.color = "white";
canvas.freeDrawingBrush.width = 20;

// Receive image from Streamlit
window.addEventListener("message", (event) => {
    if (event.data.type === "load_image") {
        fabric.Image.fromURL(event.data.img, function(img) {
            canvas.setWidth(img.width);
            canvas.setHeight(img.height);
            canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
        });
    }
});

function sendMask() {
    const mask = canvas.toDataURL("image/png");

    // Send to Streamlit
    window.parent.postMessage({
        isStreamlitMessage: true,
        type: "streamlit:setComponentValue",
        value: mask
    }, "*");
}