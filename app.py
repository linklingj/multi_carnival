from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def do_login():
    username = request.form.get('username', 'anonymous')
    return redirect(url_for('index', username=username))

@app.route("/index")
def index():
    username = request.args.get('username', 'NoName')
    return render_template('index.html', username=username)

@socketio.on('connect')
def handle_connect():
    print('Client Connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client Disconnected')

@socketio.on('join_room')
def handle_join_room(data):
    room = data.get('room')
    user = data.get('user_name')

    print(user + ' Joined Room')
    join_room(room)

@socketio.on('move_input')
def handle_move_input(data):
    """
    data 예시: {'user_name':'xxx', 'user_id':'xxx', 'input_btn':'up'}
    """
    user_name = data.get('user_name')
    user_id = data.get('user_id')
    input_btn = data.get('input_btn', '')

    print(f"[Server] input from {user_name}: {input_btn}")

    socketio.emit('unity_input', data, room = 'game_room')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)