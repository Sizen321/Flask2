from http import HTTPStatus
from api import db, app
from api.models.quote import QuoteModel
from api.models.author import AuthorModel
from typing import Any
from flask import jsonify, abort, request
from . import validate
from sqlalchemy.exc import InvalidRequestError

# URL: /quotes
@app.route("/quotes")
def get_quotes() -> list[dict[str, Any]]:
    """ Функция неявно преобразовывает список словарей в JSON."""
    quotes_db = db.session.scalars(db.select(QuoteModel)).all()
    quotes = []
    for quote in quotes_db:
        quotes.append(quote.to_dict())
    return jsonify(quotes), 200


# URL: /authors/1/quotes
@app.route("/authors/<int:author_id>/quotes")
def get_author_quotes(author_id):
    """ Функция неявно преобразовывает список словарей в JSON."""
    author = db.session.get(AuthorModel, author_id)
    quotes = []
    for quote in author.quotes:
        quotes.append(quote.to_dict())
    
    return jsonify(author=author.to_dict() | {"quotes": quotes}), 200


@app.route("/authors/<int:author_id>/quotes", methods=['POST'])
def create_quote(author_id):
    raw_data = request.json
    data = validate(raw_data)
    author = db.get_or_404(AuthorModel, author_id)
    try:
        quote = QuoteModel(**data)
        db.session.add(quote)
        db.session.commit()
    except Exception as e:
        abort(503, f"error: {str(e)}")
    except TypeError:
        return (
            (
                "Invalid data. Required: author, text, rating (optional). "
                f"Recevived: {', '.join(data.keys())}"
            ),
            HTTPStatus.BAD_REQUEST,
        )
    return quote.to_dict(), HTTPStatus.CREATED


@app.route("/quotes/filter")
def filter_quotes():
    """DONE: change to work with database."""
    try:
        if (result := db.session.execute(db.select(QuoteModel)).one_or_none()):
            print(f'{request.args =}')
            quotes = result.filter_by(**request.args).all()
        else:
            return jsonify([]), 200
    except InvalidRequestError:
        return (
            (
                "Invalid data. Required: author, text, rating (optional). "
                f"Recevived: {', '.join(request.args.keys())}"
            ),
            HTTPStatus.BAD_REQUEST,
        )
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    return jsonify([quote.to_dict() for quote in quotes]), 200