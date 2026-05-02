from flask import Flask, jsonify, request
from recommender import recommend, df, features_enrichies

app = Flask(__name__)

@app.route("/recommend")
def recommend_endpoint():
    track_name = request.args.get("track")
    if track_name is None:
        return jsonify({"error": "Paramètre track manquant"}), 400
    
    result = recommend(track_name)
    
    if result is None:
        return jsonify({"error": "Chanson non trouvée"}), 404
    
    results, scores = result
    return jsonify({"tracks": results.to_dict(orient="records")})

if __name__ == "__main__":
    app.run(port=5001, debug=True)