from flask import Flask, jsonify, abort, make_response, request
from models import books

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/api/v1/books/", methods=["GET"])
def books_list_api_v1():
    return jsonify(books.all())

@app.route("/api/v1/books/", methods=["POST"])
def create_book():
    print(request.json)
    if not request.json or 'title' not in request.json:
        abort(400)
    book = {
        'id': books.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'authors': request.json['authors'],
        'description': request.json.get('description', ""),
        'pages_num': request.json.get('pages_num'),
        'how_many': request.json.get('how_many'),
        'done': False
    }
    books.create(book)
    return jsonify({'book': book}), 201

@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})

@app.route("/api/v1/books/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'authors' in data and not isinstance(data.get('authors'), str),
        'pages_num' in data and not isinstance(data.get('pages_num'), int),
        'how_many' in data and not isinstance(data.get('how_many'), int),
        'description' in data and not isinstance(data.get('description'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    book = {
        'title': data.get('title', book['title']),
        'authors': data.get('authors', book['authors']),
        'pages_num': data.get('pages_num', book['pages_num']),
        'how_many': data.get('how_many', book['how_many']),
        'description': data.get('description', book['description']),
        'done': data.get('done', book['done'])
    }
    books.update(book_id, book)
    return jsonify({'book': book})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)