from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Messenger Interface</title>
<style>
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f1f1f1;
}

.container {
    max-width: 600px;
    margin: 20px auto;
    border: 1px solid #ccc;
    border-radius: 8px;
    overflow: hidden;
}

.chat-box {
    height: 400px;
    overflow-y: scroll;
    padding: 10px;
}

.input-box {
    display: flex;
    padding: 10px;
}

.input-box input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 20px;
    margin-right: 10px;
}

.input-box button {
    padding: 10px 20px;
    border: none;
    background-color: #4CAF50;
    color: white;
    border-radius: 20px;
    cursor: pointer;
}

.input-box button:hover {
    background-color: #45a049;
}
</style>
</head>
<body>
<div class="container">
    <div id="chat-box" class="chat-box">
        <!-- Chat messages will be dynamically added here -->
    </div>
    <div class="input-box">
        <input id="data" type="text" placeholder="Type your message...">
        <button onclick="sendMessage()">Send</button>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.3.2/socket.io.js"></script>
<script>
var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('message', function(data) {
    var message = data['message'];
    var chatBox = document.getElementById('chat-box');
    var messageDiv = document.createElement('div');
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
});

function sendMessage() {
    var data = document.getElementById("data").value;
    socket.emit('message', {message: data});
    document.getElementById("data").value = '';
}
</script>
</body>
</html>
"""

@app.route('/')
def render_html():
    return html_code

@socketio.on('message')
def handle_message(data):
    message = data['message']
    emit('message', {'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)
    