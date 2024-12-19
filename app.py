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


book_chapters = {
    # Book of Mormon
    "1 Nephi": 22, "2 Nephi": 33, "Jacob": 7, "Enos": 1, "Jarom": 1, "Omni": 1,
    "Words of Mormon": 1, "Mosiah": 29, "Alma": 63, "Helaman": 16, "3 Nephi": 30,
    "4 Nephi": 1, "Mormon": 9, "Ether": 15, "Moroni": 10,

    # Old Testament
    "Genesis": 50, "Exodus": 40, "Leviticus": 27, "Numbers": 36, "Deuteronomy": 34,
    "Joshua": 24, "Judges": 21, "Ruth": 4, "1 Samuel": 31, "2 Samuel": 24,
    "1 Kings": 22, "2 Kings": 25, "1 Chronicles": 29, "2 Chronicles": 36,
    "Ezra": 10, "Nehemiah": 13, "Esther": 10, "Job": 42, "Psalms": 150,
    "Proverbs": 31, "Ecclesiastes": 12, "Song of Solomon": 8, "Isaiah": 66,
    "Jeremiah": 52, "Lamentations": 5, "Ezekiel": 48, "Daniel": 12, "Hosea": 14,
    "Joel": 3, "Amos": 9, "Obadiah": 1, "Jonah": 4, "Micah": 7, "Nahum": 3,
    "Habakkuk": 3, "Zephaniah": 3, "Haggai": 2, "Zechariah": 14, "Malachi": 4,

    # New Testament
    "Matthew": 28, "Mark": 16, "Luke": 24, "John": 21, "Acts": 28,
    "Romans": 16, "1 Corinthians": 16, "2 Corinthians": 13, "Galatians": 6,
    "Ephesians": 6, "Philippians": 4, "Colossians": 4, "1 Thessalonians": 5,
    "2 Thessalonians": 3, "1 Timothy": 6, "2 Timothy": 4, "Titus": 3,
    "Philemon": 1, "Hebrews": 13, "James": 5, "1 Peter": 5, "2 Peter": 3,
    "1 John": 5, "2 John": 1, "3 John": 1, "Jude": 1, "Revelation": 22,

    # Doctrine and Covenants
    "Doctrine and Covenants": 138,

    # Pearl of Great Price
    "Moses": 8, "Abraham": 5, "Joseph Smith-Matthew": 1, "Joseph Smith-History": 1,
    "Articles of Faith": 1
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

def filter_options(query, options):
    query_cleaned = query.replace(" ", "").replace("-", "").lower()
    
    if query_cleaned in abbreviation_map:
        book = abbreviation_map[query_cleaned]
        return [{"book": book, "category": book_categories.get(book, "Unknown Category"), "chapter": None}]
    
    match = re.match(r'((?:\d+\s*)?[a-z]+)(\d+)?', query_cleaned)
    chapter = None
    if match:
        book_part = match.group(1)
        chapter = int(match.group(2)) if match.group(2) else None
    else:
        book_part = query_cleaned
    
    filtered_books = [
        option for option in options
        if book_part in option.replace(" ", "").replace("-", "").lower()
    ]
    
    results = []
    for book in filtered_books:
        max_chapters = book_chapters.get(book, 0)
        if chapter is None or (1 <= chapter <= max_chapters):
            results.append({"book": book, "category": book_categories.get(book, "Unknown Category"), "chapter": chapter})
        if chapter is None:
            # Add options for all valid chapters
            results.extend([
                {"book": book, "category": book_categories.get(book, "Unknown Category"), "chapter": i}
                for i in range(1, max_chapters + 1)
            ])
    
    return results


@app.route("/filter-options", methods=["POST"])
def filter_options_endpoint():
    data = request.json
    query = data.get("query", "")
    
    filtered_books = filter_options(query, books)
    
    return jsonify(filtered_books)



# Serve React frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")
if __name__ == "__main__":
    app.run(debug=True)