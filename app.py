from flask import Flask, request, jsonify, send_from_directory
import json
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="dist", static_url_path="")
CORS(app)

# Load the JSON file once when the server starts
with open("data/bom.json", "r", encoding="utf-8") as f:
    bom_data = json.load(f)

@app.route("/search", methods=["POST"])
def search_bom():
    data = request.json
    search_term = data.get("search", "")
    case_sensitive = data.get("case_sensitive", False)
    results = []

    for book, chapters in bom_data.items():
        for chapter, verses in chapters.items():
            for verse_number, verse_text in enumerate(verses, start=1):
                if (case_sensitive and search_term in verse_text) or \
                   (not case_sensitive and search_term.lower() in verse_text.lower()):
                    results.append({
                        "book": book,
                        "chapter": chapter,
                        "verse": verse_number,
                        "text": verse_text
                    })

    return jsonify(results)

# Serve React frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")
if __name__ == "__main__":
    app.run(debug=True)