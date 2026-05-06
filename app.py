from flask import Flask, request, jsonify, render_template_string
import easyocr
import requests

app = Flask(__name__)

# Load model once at startup
reader = easyocr.Reader(['en'], gpu=False)

SERVER_URL = 'https://ocr-vh1p.onrender.com/api/text'

@app.route('/api/image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image'}), 400
            
        file = request.files['image']
        img_bytes = file.read()
        
        results = reader.readtext(img_bytes)
        text = ' '.join([result[1] for result in results]).strip()
        
        if not text:
            return jsonify({'status': 'empty'}), 200
            
        payload = {'filename': 'capture.jpg', 'text': text}
        response = requests.post(SERVER_URL, json=payload, timeout=10)
        
        return jsonify({'status': 'success', 'ocr': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def camera():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
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
            }, 'image/jpeg', 0.8);
        }
    </script>
</body>
</html>
''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
    