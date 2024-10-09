from flask import Flask, jsonify, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Serial Communication Interface</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f7f7f7; }
        .container { text-align: center; padding: 20px; background-color: white; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); border-radius: 8px; }
        h1 { color: #333; }
        input, button { margin: 10px 0; padding: 5px; width: 100%; max-width: 300px; }
        #result { margin-top: 20px; padding: 10px; background-color: #f0f0f0; width: 100%; max-width: 300px; word-wrap: break-word; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Serial Communication Interface</h1>
        <input type="text" id="comPort" placeholder="COM Port (e.g., COM7)">
        <input type="number" id="baudRate" value="115200" placeholder="Baud Rate">
        <input type="number" id="brightness" min="0" max="255" placeholder="Brightness (0-255)">
        <button onclick="setBrightness()">Set Brightness</button>
        <div id="result"></div>
    </div>

    <script>
        function setBrightness() {
            const comPort = document.getElementById('comPort').value;
            const baudRate = document.getElementById('baudRate').value;
            const brightness = document.getElementById('brightness').value;

            fetch('/set_brightness', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ com_port: comPort, baud_rate: baudRate, brightness: brightness }),
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/set_brightness', methods=['POST'])
def set_brightness():
    data = request.json
    com_port = data.get('com_port')
    baud_rate = data.get('baud_rate')
    brightness = data.get('brightness')

    try:
        # Forward request to local server running serial communication
        local_server_url = 'http://<local_server_ip>:5001/serial/write'
        response = requests.post(local_server_url, json={
            'com_port': com_port,
            'baud_rate': baud_rate,
            'address': 0xd0,  # Assuming brightness is controlled at address 0xd0
            'value': brightness
        })

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
