from flask import Flask, request, jsonify, send_from_directory
import json
from flask_cors import CORS
import os
import re

app = Flask(__name__, static_folder="dist", static_url_path="")
CORS(app)




# Function to filter options based on query
def filter_options(query, options):
    # Clean the query by removing spaces and dashes
    query_cleaned = query.replace(" ", "").replace("-", "").lower()
    
    # Check if the query is an abbreviation like "doc" or "dc" and map to the full title
    if query_cleaned in abbreviation_map:
        return [abbreviation_map[query_cleaned]]
    
    # Filter options by removing spaces and dashes and comparing
    return [
        option for option in options
        if query_cleaned in option.replace(" ", "").replace("-", "").lower()
    ]



abbreviation_map = {
    "dc": "Doctrine and Covenants",
    "jsh": "Joseph Smith-History",
    "jsm": "Joseph Smith-Matthew",
    "aof": "Articles of Faith",
}

books = [
    #book of mormon
    "1 Nephi", "2 Nephi", "Jacob", "Enos", "Jarom", "Omni", "Words of Mormon", "Mosiah",
    "Alma", "Helaman", "3 Nephi", "4 Nephi", "Mormon", "Ether", "Moroni",
    # Old Testament
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", "1 Samuel",
    "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", 
    "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", 
    "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", 
    "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
    #new testament
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", 
    "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", 
    "1 John", "2 John", "3 John", "Jude", "Revelation",
    #Doctrine and Covenants
    "Doctrine and Covenants",
    #pearl of great price
    "Moses", "Abraham", "Joseph Smith-Matthew", "Joseph Smith-History", "Articles of Faith"
]
@app.route("/filter-options", methods=["POST"])
def filter_options_endpoint():
    data = request.json
    query = data.get("query", "")
    
    # Call your Python function
    filtered_options = filter_options(query, books)
    
    return jsonify(filtered_options)



# Serve React frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")
if __name__ == "__main__":
    app.run(debug=True)