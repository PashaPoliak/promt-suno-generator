from flask import Flask, request, jsonify, render_template_string
import requests
import base64
import os

app = Flask(__name__)

OCR_SPACE_API_KEY = os.environ.get('OCR_API_KEY')
GALLERY_URL = 'https://ocr-vh1p.onrender.com/api/text'

@app.route('/api/image', methods=['POST'])
def process_image():
    try:
        if not OCR_SPACE_API_KEY:
            return jsonify({'error': 'Server configuration error: Missing API Key'}), 500

        if 'image' not in request.files:
            return jsonify({'error': 'No image'}), 400

        file = request.files['image']
        img_data = file.read()
        base64_image = base64.b64encode(img_data).decode('utf-8')

        payload = {
            'base64Image': f"data:image/jpeg;base64,{base64_image}",
            'apikey': OCR_SPACE_API_KEY,
            'language': 'eng',
        }

        api_resp = requests.post('https://api.ocr.space/parse/image', data=payload, timeout=15).json()

        if not api_resp.get('ParsedResults'):
            return jsonify({'status': 'ocr_failed', 'details': api_resp}), 400

        text = api_resp['ParsedResults'][0]['ParsedText'].strip()

        if text:
            requests.post(GALLERY_URL, json={'filename': 'capture.jpg', 'text': text}, timeout=10)

        return jsonify({'status': 'success', 'ocr': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def camera():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: #000; }
        video { width: 100vw; height: 100vh; object-fit: cover; }
        .shutter {
            position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%);
            width: 70px; height: 70px; background: #fff; border-radius: 50%; border: none;
        }
    </style>
</head>
<body>
    <video id="v" autoplay playsinline></video>
    <button class="shutter" onclick="snap()"></button>
    <canvas id="c" style="display:none;"></canvas>
    <script>
        const v = document.getElementById('v');
        navigator.mediaDevices.getUserMedia({video: {facingMode: 'environment'}})
            .then(s => v.srcObject = s);
        function snap() {
            const c = document.getElementById('c');
            c.width = v.videoWidth;
            c.height = v.videoHeight;
            c.getContext('2d').drawImage(v, 0, 0);
            c.toBlob(b => {
                const f = new FormData();
                f.append('image', b, 'p.jpg');
                fetch('/api/image', {method: 'POST', body: f});
            }, 'image/jpeg', 0.6);
        }
    </script>
</body>
</html>
''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)