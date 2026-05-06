from flask import Flask, request, jsonify, render_template_string
import os
import easyocr
import requests

app = Flask(__name__)
reader = easyocr.Reader(['en'])

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
            return jsonify({'status': 'no text detected'}), 200
            
        json_data = {
            'filename': 'capture.jpg',
            'text': text
        }
        
        response = requests.post(SERVER_URL, json=json_data, timeout=10)
        response.raise_for_status()
        
        return jsonify({'status': 'success', 'text': text})
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
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body, html { width: 100%; height: 100%; overflow: hidden; background: #000; }
        video { width: 100vw; height: 100vh; object-fit: cover; }
        .shutter {
            position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%);
            width: 70px; height: 70px; background: white; border-radius: 50%; border: none;
        }
    </style>
</head>
<body>
    <video id="video" autoplay playsinline></video>
    <button class="shutter" onclick="takePhoto()"></button>
    <canvas id="canvas" style="display:none;"></canvas>
    <script>
        const video = document.getElementById('video');
        async function start() {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { 
                    facingMode: 'environment',
                    width: { ideal: window.innerWidth },
                    height: { ideal: window.innerHeight }
                }
            });
            video.srcObject = stream;
        }
        async function takePhoto() {
            const canvas = document.getElementById('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            
            canvas.toBlob(async (blob) => {
                const formData = new FormData();
                formData.append('image', blob, 'photo.jpg');
                await fetch('/api/image', { method: 'POST', body: formData });
            }, 'image/jpeg', 0.9);
        }
        start();
    </script>
</body>
</html>
''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
    
 