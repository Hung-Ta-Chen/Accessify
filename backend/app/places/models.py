from flask_sqlalchemy import SQLAlchemy
from app import db


class Place(db.Model):
    '''Model for Place'''
    # __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    lat = db.Column(db.Numeric(25, 15), nullable=False)
    lng = db.Column(db.Numeric(25, 15), nullable=False)
    place_id = db.Column(db.String(300), unique=True, nullable=False)
    place_type = db.Column(db.String(255), nullable=False)

    reviews = db.relationship('Review', backref='place', lazy='dynamic')

    def __repr__(self):
        return f'<Place: {self.name}, (Lat, Lng): ({self.lat}, {self.lng})>'

    def to_dict(self):
        '''For serialization'''
        return {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,
            'place_id': self.place_id,
            'place_type': self.place_type
        }


class Review(db.Model):
    '''Model for Review'''
    # __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey(
        'place.id'), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    wheelchair_rating = db.Column(db.Integer, nullable=False)
    restroom_rating = db.Column(db.Integer, nullable=False)
    overall_rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Review {self.id} by {self.username}>'

    def to_dict(self):
        '''For serialization'''
        return {
            'id': self.id,
            'username': self.username,
            'wheelchair_rating': self.wheelchair_rating,
            'restroom_rating': self.restroom_rating,
            'overall_rating': self.overall_rating,
            'comment': self.comment,
            'place_id': self.place.place_id if self.place else None,
            'created_at': self.created_at,
        }
