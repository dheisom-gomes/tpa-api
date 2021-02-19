from os import environ
from re import findall
from flask import Flask, jsonify, request
import scrapping

app: Flask = Flask(__name__)
consoles: list = scrapping.getConsoles()
games: dict = {}
consolesRequests: int = 0
gamesRequests: dict = {}


@app.route("/api/v1/consoles", methods=["GET"])
def getConsoles():
    global consoles, consolesRequests
    if consolesRequests in (0, 10):
        consoles = scrapping.getConsoles()
        consolesRequests = 1
    else:
        consolesRequests += 1
    return jsonify({'ok': True, 'result': consoles}), 200


@app.route("/api/v1/consoles/<int:id>", methods=["GET"])
def getGames(id):
    global games, gamesRequests, consoles
    if len(consoles) < (id+1):
        return jsonify({'ok': False, 'message': 'Console not found'}), 404
    try:
        offset: int = int(request.args.get("offset", 0))
        limit: int = int(request.args.get("limit", 200)) + offset
    except Exception:
        return jsonify({'ok': False, 'message': 'Invalid "offset" or "limit"'}), 400
    if gamesRequests.get(id, 0) in (0, 10):
        games[id] = scrapping.getGames(consoles[id]["url"])
        gamesRequests[id] = 1
    else:
        gamesRequests[id] += 1
    return jsonify({'ok': True, 'result': games[id][offset:limit]}), 200


@app.route("/api/v1/search/<int:id>", methods=["GET"])
def searchGame(id):
    global games, consoles, gamesRequests
    if len(consoles) < (id+1):
        return jsonify({'ok': False, 'message': 'Console not found'}), 400
    try:
        query = request.args.get("query").strip().lower()
    except Exception:
        return jsonify({'ok': False, 'message': '"query" parameter not informed'}), 400
    if not query:
        return jsonify({'ok': False, 'message': '"query" parameter cont\'t be blank'}), 400
    if not id in games or gamesRequests in (0, 10):
        games[id] = scrapping.getGames(consoles[id]["url"])
        gamesRequests[id] = 1
    else:
        gamesRequests[id] += 1
    result = []
    for game in games[id]:
        if findall(query, game["name"].lower()):
            result.append(game)
    if not result:
        return jsonify({'ok': False, 'message': 'This search did not return a result'}), 400
    return jsonify({'ok': True, 'result': result}), 200


@app.errorhandler(500)
def internalError(err):
    return jsonify({'ok': False, 'message': 'Internal server error'}), 500


def main() -> None:
    host: str = '0.0.0.0'
    port: int = int(environ.get("PORT", 5000))
    app.run(host, port)
