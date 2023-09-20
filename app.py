from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the database and tables
def init_db():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')  # Enable foreign key support
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES authors (id)
        )
    ''')
    cursor.execute("INSERT INTO authors (name) VALUES ('Author 1')")
    cursor.execute("INSERT INTO authors (name) VALUES ('Author 2')")
    cursor.execute("INSERT INTO books (title, author_id) VALUES ('Book 1', 1)")
    cursor.execute("INSERT INTO books (title, author_id) VALUES ('Book 2', 2)")
    conn.commit()
    conn.close()

# Create a route to list all authors
@app.route('/authors', methods=['GET'])
def get_authors():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()
    conn.close()
    return jsonify(authors)

# Create a route to add a new author
@app.route('/authors', methods=['POST'])
def add_author():
    name = request.json.get('name')
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Author added successfully"})

# Create a route to update an author
@app.route('/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    name = request.json.get('name')
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE authors SET name=? WHERE id=?", (name, author_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Author updated successfully"})

# Create a route to delete an author
@app.route('/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM authors WHERE id=?", (author_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Author deleted successfully"})

# Create a route to list all books
@app.route('/books', methods=['GET'])
def get_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT books.id, books.title, authors.name FROM books JOIN authors ON books.author_id = authors.id')
    books = cursor.fetchall()
    conn.close()
    return jsonify(books)

# Create a route to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    title = request.json.get('title')
    author_id = request.json.get('author_id')
    
    # Ensure author_id is an integer
    try:
        author_id = int(author_id)
    except ValueError:
        return jsonify({"message": "Invalid author_id. It should be an integer."}), 400
    
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", (title, author_id))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Book added successfully"})

# Create a route to update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    title = request.json.get('title')
    author_id = request.json.get('author_id')
    
    # Ensure author_id is an integer
    try:
        author_id = int(author_id)
    except ValueError:
        return jsonify({"message": "Invalid author_id. It should be an integer."}), 400
    
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=?, author_id=? WHERE id=?", (title, author_id, book_id))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Book updated successfully"})
# Create a route to delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Book deleted successfully"})

if __name__ == '__main__':
    # init_db()
    app.run(debug=True)
