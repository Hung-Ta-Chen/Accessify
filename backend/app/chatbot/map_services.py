from dotenv import load_dotenv
import os
import googlemaps
from datetime import datetime
from flask import current_app
from .db_services import save_place_details

load_dotenv()

MAPS_API_KEY = os.environ.get('MAPS_API_KEY')

# Initialize Google Maps client
gmaps = googlemaps.Client(key=MAPS_API_KEY)


def fetch_place_details(place_name):
    geocode_result = gmaps.geocode(place_name)
    if not geocode_result:
        return None

    place_id = geocode_result[0]['place_id']
    place_details = gmaps.place(place_id=place_id)['result']

    details = {
        "name": place_details.get("name"),
        "address": place_details.get("formatted_address"),
        "phone_number": place_details.get("formatted_phone_number", None),
        "status": place_details.get("business_status"),
        "rating": place_details.get("rating", -1),
        "reviews": [{"author_name": review.get("author_name"),
                     "rating": review.get("rating"),
                     "time": review.get("time"),
                     "text": review.get("text", "")
                     } for review in place_details.get("reviews", [])],
        "latitude": place_details.get("geometry", {}).get("location", {}).get("lat"),
        "longitude": place_details.get("geometry", {}).get("location", {}).get("lng"),
        "geometry_type": place_details.get("geometry", {}).get("location_type"),
        "place_id": place_id,
        "types": place_details.get("types", []),
        "price_level": place_details.get("price_level", "No price level available"),
        "opening_hours": place_details.get("opening_hours", {}).get("weekday_text", []),
        "vicinity": place_details.get("vicinity", ""),
        "price_level": place_details.get("price_level", ""),
        "wheelchair_accessible_entrance": place_details.get("wheelchair_accessible_entrance", False),
        "user_ratings_total": place_details.get("user_ratings_total", 0),
        "reservable": place_details.get("reservable", False),
        "delivery": place_details.get("delivery", False),
        "dine_in": place_details.get("dine_in", False),
        "takeout": place_details.get("takeout", False),
        "serves_breakfast": place_details.get("serves_breakfast", False),
        "serves_lunch": place_details.get("serves_lunch", False),
        "serves_dinner": place_details.get("serves_dinner", False),
        "serves_vegetarian_food": place_details.get("serves_vegetarian_food", False),
        "serve_alcohol": place_details.get("serves_beer", False) or place_details.get("serves_wine", False),
        "summary": place_details.get("editorial_summary", {}).get("overview", "")
    }
    save_place_details(details)
    return details


def fetch_vicinity_details(location, radius=10000, service_type='', k=20):
    current_app.logger.info(
        f'location: {location}, service_type={service_type}')
    # Perform a nearby search for each type of service
    places_result = gmaps.places_nearby(
        location=location, radius=10000, type=service_type)

    places = []
    for place_details in places_result.get('results', []):
        # Try save the place details in db
        details = {
            "name": place_details.get("name"),
            "address": place_details.get("formatted_address"),
            "phone_number": place_details.get("formatted_phone_number", None),
            "status": place_details.get("business_status"),
            "rating": place_details.get("rating", -1),
            "reviews": [{"author_name": review.get("author_name"),
                        "rating": review.get("rating"),
                         "time": review.get("time"),
                         "text": review.get("text", "")
                         } for review in place_details.get("reviews", [])],
            "latitude": place_details.get("geometry", {}).get("location", {}).get("lat"),
            "longitude": place_details.get("geometry", {}).get("location", {}).get("lng"),
            "geometry_type": place_details.get("geometry", {}).get("location_type"),
            "place_id": place_details.get("place_id"),
            "types": place_details.get("types", []),
            "price_level": place_details.get("price_level", "No price level available"),
            "opening_hours": place_details.get("opening_hours", {}).get("weekday_text", []),
            "vicinity": place_details.get("vicinity", ""),
            "price_level": place_details.get("price_level", ""),
            "wheelchair_accessible_entrance": place_details.get("wheelchair_accessible_entrance", False),
            "user_ratings_total": place_details.get("user_ratings_total", 0),
            "reservable": place_details.get("reservable", False),
            "delivery": place_details.get("delivery", False),
            "dine_in": place_details.get("dine_in", False),
            "takeout": place_details.get("takeout", False),
            "serves_breakfast": place_details.get("serves_breakfast", False),
            "serves_lunch": place_details.get("serves_lunch", False),
            "serves_dinner": place_details.get("serves_dinner", False),
            "serves_vegetarian_food": place_details.get("serves_vegetarian_food", False),
            "serve_alcohol": place_details.get("serves_beer", False) or place_details.get("serves_wine", False),
            "summary": place_details.get("editorial_summary", {}).get("overview", "")
        }
        save_place_details(details)

        # Append some general details to the result list
        places.append({
            "name": place_details.get('name'),
            "address": place_details.get('vicinity'),
            "rating": place_details.get('rating', -1),
            "place_id": place_details.get('place_id'),
            "open_now": place_details.get('opening_hours', {}).get('open_now', False),
            "status": place_details.get("business_status"),
            "wheelchair_accessible_entrance": place_details.get("wheelchair_accessible_entrance", False),
        })

        if len(places) >= k:
            break

    return places


def geocode(place_name):
    geocode_result = gmaps.geocode(place_name)

    if not geocode_result:
        return None  # No geocode results
    location = geocode_result[0]['geometry']['location']
    return (location['lat'], location['lng'])
