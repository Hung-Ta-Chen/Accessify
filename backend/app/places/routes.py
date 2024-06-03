from flask import Blueprint, jsonify, request, abort
from .models import Place, Review
from .services import *

place_blueprint = Blueprint('place_blueprint', __name__)
review_blueprint = Blueprint('review_blueprint', __name__)


@place_blueprint.route('/places', methods=['GET'])
def get_places():
    places = get_all_places()
    return jsonify([place.to_dict() for place in places]), 200


@place_blueprint.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = get_place_by_placeid(place_id)
    if not place:
        abort(404, description=f"No place matches place_id={place_id}.")
    return jsonify(place.to_dict()), 200


@place_blueprint.route('/places', methods=['POST'])
def add_place():
    place_data = request.get_json()
    new_place = create_place(place_data)
    return jsonify(new_place.to_dict()), 201


@place_blueprint.route('/places/<place_id>', methods=['PUT'])
def modify_place(place_id):
    data = request.get_json()
    updated_place = update_place(place_id, data)
    if not updated_place:
        abort(404, description=f"No place matches place_id={place_id}.")
    return jsonify(updated_place.to_dict()), 200


@place_blueprint.route('/places/<place_id>', methods=['DELETE'])
def remove_place(place_id):
    result = delete_place(place_id)
    if not result:
        abort(404, description=f"No place matches place_id={place_id}.")
    return jsonify({'message': 'Place deleted'}), 200


@review_blueprint.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    reviews = get_reviews_of_place(place_id)
    if len(reviews) > 0:
        return jsonify([review.to_dict() for review in reviews]), 200
    else:
        abort(
            404, description=f"No reviews found for the specified place_id: {place_id}.")


@review_blueprint.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    review_data = request.get_json()
    new_review = add_review_to_place(place_id, review_data)
    if new_review:
        return jsonify(new_review.to_dict()), 201
    else:
        abort(404, description=f"No place matches place_id={place_id}.")


@review_blueprint.route('/places/<place_id>/stats', methods=['GET'])
def get_place_stats(place_id):
    stats = calculate_stats(place_id)
    if stats is None:
        abort(404, description=f"No place found with place_id {place_id}.")
    return jsonify(stats), 200
