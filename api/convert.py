from flask import request, jsonify
from PIL import Image
from flask_cors import CORS
import io

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def image_to_ascii(image_bytes, width=100, invert=False):
    chars = ASCII_CHARS[::-1] if invert else ASCII_CHARS
    img = Image.open(io.BytesIO(image_bytes)).convert("L")
    img.thumbnail((1200, 1200))
    original_width, original_height = img.size
    height = int(original_height * width / original_width * 0.45)
    img = img.resize((width, height))
    pixels = list(img.getdata())
    ascii_str = ""
    for i, pixel in enumerate(pixels):
        ascii_str += chars[pixel * len(chars) // 256]
        if (i + 1) % width == 0:
            ascii_str += "\n"
    return ascii_str

def handler(request):
    if request.method == "POST":
        file = request.files.get("image")
        if not file:
            return jsonify({"error": "No image uploaded"}), 400
        width = int(request.form.get("width", 100))
        invert = request.form.get("invert") == "true"
        result = image_to_ascii(file.read(), width, invert)
        return jsonify({"ascii_art": result})