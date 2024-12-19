from flask import Flask, request, jsonify, send_from_directory
import json
from flask_cors import CORS
import os
import re

app = Flask(__name__, static_folder="dist", static_url_path="")
CORS(app)


# Book-to-category mapping
# Book-to-category mapping
book_categories = {
    # Book of Mormon
    "1 Nephi": "Book of Mormon",
    "2 Nephi": "Book of Mormon",
    "Jacob": "Book of Mormon",
    "Enos": "Book of Mormon",
    "Jarom": "Book of Mormon",
    "Omni": "Book of Mormon",
    "Words of Mormon": "Book of Mormon",
    "Mosiah": "Book of Mormon",
    "Alma": "Book of Mormon",
    "Helaman": "Book of Mormon",
    "3 Nephi": "Book of Mormon",
    "4 Nephi": "Book of Mormon",
    "Mormon": "Book of Mormon",
    "Ether": "Book of Mormon",
    "Moroni": "Book of Mormon",
    
    # Old Testament
    "Genesis": "Old Testament",
    "Exodus": "Old Testament",
    "Leviticus": "Old Testament",
    "Numbers": "Old Testament",
    "Deuteronomy": "Old Testament",
    "Joshua": "Old Testament",
    "Judges": "Old Testament",
    "Ruth": "Old Testament",
    "1 Samuel": "Old Testament",
    "2 Samuel": "Old Testament",
    "1 Kings": "Old Testament",
    "2 Kings": "Old Testament",
    "1 Chronicles": "Old Testament",
    "2 Chronicles": "Old Testament",
    "Ezra": "Old Testament",
    "Nehemiah": "Old Testament",
    "Esther": "Old Testament",
    "Job": "Old Testament",
    "Psalms": "Old Testament",
    "Proverbs": "Old Testament",
    "Ecclesiastes": "Old Testament",
    "Song of Solomon": "Old Testament",
    "Isaiah": "Old Testament",
    "Jeremiah": "Old Testament",
    "Lamentations": "Old Testament",
    "Ezekiel": "Old Testament",
    "Daniel": "Old Testament",
    "Hosea": "Old Testament",
    "Joel": "Old Testament",
    "Amos": "Old Testament",
    "Obadiah": "Old Testament",
    "Jonah": "Old Testament",
    "Micah": "Old Testament",
    "Nahum": "Old Testament",
    "Habakkuk": "Old Testament",
    "Zephaniah": "Old Testament",
    "Haggai": "Old Testament",
    "Zechariah": "Old Testament",
    "Malachi": "Old Testament",
    
    # New Testament
    "Matthew": "New Testament",
    "Mark": "New Testament",
    "Luke": "New Testament",
    "John": "New Testament",
    "Acts": "New Testament",
    "Romans": "New Testament",
    "1 Corinthians": "New Testament",
    "2 Corinthians": "New Testament",
    "Galatians": "New Testament",
    "Ephesians": "New Testament",
    "Philippians": "New Testament",
    "Colossians": "New Testament",
    "1 Thessalonians": "New Testament",
    "2 Thessalonians": "New Testament",
    "1 Timothy": "New Testament",
    "2 Timothy": "New Testament",
    "Titus": "New Testament",
    "Philemon": "New Testament",
    "Hebrews": "New Testament",
    "James": "New Testament",
    "1 Peter": "New Testament",
    "2 Peter": "New Testament",
    "1 John": "New Testament",
    "2 John": "New Testament",
    "3 John": "New Testament",
    "Jude": "New Testament",
    "Revelation": "New Testament",
    
    # Doctrine and Covenants
    "Doctrine and Covenants": "Doctrine and Covenants",
    
    # Pearl of Great Price
    "Moses": "Pearl of Great Price",
    "Abraham": "Pearl of Great Price",
    "Joseph Smith-Matthew": "Pearl of Great Price",
    "Joseph Smith-History": "Pearl of Great Price",
    "Articles of Faith": "Pearl of Great Price"
}


abbreviation_map = {
    "dc": "Doctrine and Covenants",
    "jsh": "Joseph Smith-History",
    "jsm": "Joseph Smith-Matthew",
    "aof": "Articles of Faith",
    "wom": "Words of Mormon",
    "sos": "Song of Solomon",
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



@app.route("/filter-options", methods=["POST"])
def filter_options_endpoint():
    data = request.json
    query = data.get("query", "")
    
    # Call the filter_options function to filter books based on the query
    filtered_books = filter_options(query, books)
    
    # Now add the category for each filtered book from book_categories
    filtered_books_with_categories = [
        {"book": book, "category": book_categories.get(book, "Unknown Category")}
        for book in filtered_books
    ]
    
    return jsonify(filtered_books_with_categories)



# Serve React frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")
if __name__ == "__main__":
    app.run(debug=True)