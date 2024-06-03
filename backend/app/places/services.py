from .models import Place, Review
from app import db
from sqlalchemy import func


def get_all_places():
    """Service for getting all places"""
    return Place.query.all()


def get_place_by_placeid(place_id):
    """Service for getting place by place_id"""
    return Place.query.filter_by(place_id=place_id).first()


def create_place(data):
    """Servie for creating a new place"""
    new_place = Place(name=data['name'],
                      lat=data['lat'],
                      lng=data['lng'],
                      place_id=data['place_id'],
                      place_type=data['place_type'],
                      )
    db.session.add(new_place)
    db.session.commit()
    return new_place


def update_place(place_id, data):
    """Service for updating a place by place_id"""
    place = get_place_by_placeid(place_id)
    if place:
        place.name = data.get('name', place.name)
        place.lat = data.get('lat', place.lat)
        place.lng = data.get('lng', place.lng)
        place.place_type = data.get('place_type', place.place_type)
        db.session.commit()
    return place


def delete_place(place_id):
    """Service for deleting place by place_id"""
    place = get_place_by_placeid(place_id)
    if place:
        db.session.delete(place)
        db.session.commit()
        return True
    return False


def get_reviews_of_place(place_id):
    """Service for getting reviews to place by place_id"""
    place = get_place_by_placeid(place_id)
    if place:
        return place.reviews.all()
    return []


def add_review_to_place(place_id, data):
    """Service for adding a review to place by place_id"""
    place = get_place_by_placeid(place_id)
    if place:
        new_review = Review(place=place,
                            username=data['username'],
                            wheelchair_rating=data['wheelchair_rating'],
                            restroom_rating=data['restroom_rating'],
                            overall_rating=data['overall_rating'],
                            comment=data['comment'])
        db.session.add(new_review)
        db.session.commit()
        return new_review
    return None


def calculate_stats(place_id):
    place = Place.query.filter_by(place_id=place_id).first()
    if not place:
        return None

    reviews = Review.query.filter_by(place_id=place.id)
    # Calculate stats of reviews
    stats = {
        'average_wheelchair_access_rating': reviews.with_entities(func.avg(Review.wheelchair_rating)).scalar(),
        'average_restroom_rating': reviews.with_entities(func.avg(Review.restroom_rating)).scalar(),
        'average_overall_rating': reviews.with_entities(func.avg(Review.overall_rating)).scalar(),
        'user_review_count': reviews.count(),
    }
    return stats
