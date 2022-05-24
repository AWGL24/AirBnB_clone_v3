#!/usr/bin/python3
""" Module handles all default RESTful API actions """
from flask import abort, jsonify
from requests import request
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews(place_id):
    """ Retrieves the list of all Review objects of Place """
    place = storage.get('Place', place_id)
    reviewList = []
    if place is None:
        abort(404)
    for review in place.reviews:
        reviewList.append(review.to_dict())
    return jsonify(reviewList)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def getreview(review_id):
    """ Retrieves a Review objects """
    r = storage.get('Review', review_id)
    if r is None:
        abort(404)
    return jsonify(r.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def reviewdel(review_id):
    """ Deletes a Review object """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    dictionary = {}
    review.delete()
    storage.save()
    return jsonify(dictionary), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def reviewCreate(place_id):
    """ Creates a review object """
    places = storage.get('Place', place_id)
    if places is None:
        abort(404)
    json_req = request.get_json()
    if json_req is None:
        abort(400, "Not a JSON")
    if "user_id" not in json_req:
        abort(400, "Missing user_id")
    user = storage.get('User', json_req["user_id"])
    if user is None:
        abort(404)
    if "text" not in json_req:
        abort(400, "Missing text")
    json_req["place_id"] = place_id
    newReview = Review(**json_req)
    newReview.save()
    return jsonify(newReview.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def reviewUpdate(review_id):
    """ Update a Review object """
    json_req = request.get_json()
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if json_req is None:
        abort(400, "Not a JSON")
    for key, value in json_req.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "place_id"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict(), 200)
