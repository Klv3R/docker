from flask import Flask, render_template, request, jsonify
import redis

# 1. Initialize the app FIRST
app = Flask(__name__)

# 2. Connect to the database
db = redis.Redis(host='redis', port=6379, decode_responses=True)

# 3. NOW you can define your routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/score', methods=['POST'])
def save_score():
    data = request.json
    db.zadd("leaderboard", {data['name']: data['score']})
    return jsonify(status="success")

@app.route('/leaderboard', methods=['GET'])
def get_scores():
    scores = db.zrevrange("leaderboard", 0, 9, withscores=True)
    # This flattens the list for the frontend
    flattened = [item for sublist in scores for item in sublist]
    return jsonify(flattened)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)