from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
from scripture_data import verse_counts, abbreviation_map, book_categories, book_chapters, books

app = Flask(__name__, static_folder="dist", static_url_path="")
CORS(app)


def filter_options(query, options):
    query_cleaned = query.replace(" ", "").replace("-", "").lower()
    
    if query_cleaned in abbreviation_map:
        book = abbreviation_map[query_cleaned]
        return [{"book": book, "category": book_categories.get(book, "Unknown Category"), "chapter": None, "verse": None}]
    
    match = re.match(r'((?:\d+\s*)?[a-z]+)(\d+)?(?::(\d+))?', query_cleaned)
    chapter = None
    verse = None
    if match:
        book_part = match.group(1)
        chapter = int(match.group(2)) if match.group(2) else None
        verse = int(match.group(3)) if match.group(3) else None
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
            if verse is None or (chapter and 1 <= verse <= verse_counts.get(book, {}).get(chapter, 0)):
                results.append({"book": book, "category": book_categories.get(book, "Unknown Category"), "chapter": chapter, "verse": verse})
            if verse is None and chapter:
                # Add options for all valid verses in this chapter
                max_verses = verse_counts.get(book, {}).get(chapter, 0)
                results.extend([
                    {"book": book, "category": book_categories.get(book, "Unknown Category"), "chapter": chapter, "verse": v}
                    for v in range(1, max_verses + 1)
                ])
        if chapter is None:
            # Add options for all valid chapters
            results.extend([
                {"book": book, "category": book_categories.get(book, "Unknown Category"), "chapter": i, "verse": None}
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