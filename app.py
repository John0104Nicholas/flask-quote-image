from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import textwrap
import uuid
import os

app = Flask(__name__)

# Ensure output folder exists
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()

    # Safely read values with defaults
    text = data.get("text", "No quote provided")
    font_size = int(data.get("font_size", 48))
    bgcolor = data.get("bgcolor", "#1E1E1E")
    text_color = data.get("text_color", "#FFFFFF")

    # Create a blank 1080x1080 image
    img = Image.new("RGB", (1080, 1080), color=bgcolor)
    draw = ImageDraw.Draw(img)

    # Use system font (make sure this path exists)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)

    # Wrap and draw the quote
    wrapped_text = textwrap.fill(text, width=30)
    draw.text((50, 400), wrapped_text, font=font, fill=text_color)

    # Save the image to output folder
    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath)

    # Return image file as binary
    return send_file(filepath, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
