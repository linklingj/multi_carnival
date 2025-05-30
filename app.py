from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
clients = {}

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def do_login():
    username = request.form.get('username', 'anonymous')
    role = request.form.get('role')
    return redirect(url_for('index', username=username, role=role))

@app.route("/index")
def index():
    username = request.args.get('username', 'NoName')
    role = request.args.get('role', 'all')
    return render_template('index.html', username=username, role=role)

@socketio.on('connect')
def handle_connect():
    user_name = request.args.get('user_name', 'anonymous')
    role = request.args.get('role', 'unity')
    if user_name == "UNITY":
        return
    sid = request.sid
    clients[sid] = {'user_name': user_name, 'role': role}

    print(f"Client Connected: {user_name}")

    socketio.emit('users_info', clients, room = 'game_room')

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    user = clients.pop(sid, None)

    print(f"Client Disconnected: {user['user_name']}")

@socketio.on('join_room')
def handle_join_room(data):
    room = data.get('room')
    user = data.get('user_name')

    join_room(room)
    print(user + ' Joined Room')

@socketio.on('move_input')
def handle_move_input(data):
    """
    data 예시: {'user_name':'xxx', 'user_id':'xxx', 'input_btn':'up', 'btn_type':'down'}
    """
    user_name = data.get('user_name')
    user_id = data.get('user_id')
    input_btn = data.get('input_btn', '')
    btn_type = data.get('btn_type', 'click')

    print(f"[Server] input from {user_name}: {input_btn} type: {btn_type}")

    socketio.emit('unity_input', data, room = 'game_room')



if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, allow_unsafe_werkzeug=True)
