from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for players
players = {}

@app.route('/join', methods=['POST'])
def join_game():
    data = request.json
    player_id = data['id']
    players[player_id] = {'x': 400, 'y': 300}  # Starting position
    return jsonify(players)

@app.route('/update', methods=['POST'])
def update_player():
    data = request.json
    player_id = data['id']
    players[player_id]['x'] += data['dx']
    players[player_id]['y'] += data['dy']
    return jsonify(players)

@app.route('/players', methods=['GET'])
def get_players():
    return jsonify(players)

if __name__ == "__main__":
    app.run(debug=True)
