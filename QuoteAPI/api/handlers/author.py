from http import HTTPStatus

from marshmallow import ValidationError
from api import app, db
from api.models.author import AuthorModel
from flask import abort, jsonify, request
from api.schemas.author import author_schema, authors_schema


@app.route("/authors", methods=['GET'])
def get_authors():
    authors_db = db.session.scalars(db.select(AuthorModel)).all()
    return jsonify(authors_schema.dump(authors_db)), 200



@app.route("/authors", methods=['POST'])
def create_author():
    # author_data = request.json 
    try:
        author_data = author_schema.loads(request.data) # get_data
        author = AuthorModel(**author_data)
        db.session.add(author)
        db.session.commit()
    except ValidationError as ve:
        abort(400, f'Validation error: {str(ve)}')
    except Exception as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")
    return jsonify(author_schema.dump(author)), 201
                   

@app.route("/authors/<int:author_id>", methods=['GET'])
def create_author_by_id(author_id: int):
    author = db.get_or_404(AuthorModel, author_id, description=f'Author with id={author_id} not found')
    # instance -> dict -> json
    return jsonify(author_schema.dump(author)), 200


@app.route("/authors/<int:author_id>", methods=['PUT'])
def edit_author(author_id: int):
    author: AuthorModel = db.get_or_404(AuthorModel, author_id, description=f'Author with id={author_id} not found')
    try:
        data = author_schema.loads(request.data)
    except ValidationError as ve:
        abort(400, f'Validation error: {str(ve)}')

    for key, value in data.items():
        setattr(author, key, value)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(503, f'Database error: {str(e)}')
    return jsonify(author_schema.dump(author)), 200


@app.route("/authors/<int:author_id>", methods=["DELETE"])
def delete_author(author_id:int):
    author = db.get_or_404(AuthorModel, author_id, description=f'Author with id={author_id} not found')
    db.session.delete(author)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")
    return jsonify(message=f"Author with id {author_id} deleted"), 200