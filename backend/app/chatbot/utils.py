def format_document_text(place):
    descriptions = [place.get("summary", "")]
    for review in place.get("reviews", []):
        descriptions.append(review.get("text", ""))

    attributes = []
    if place.get("wheelchain_accessible_entrance", False):
        attributes.append("This place is wheelchair accessible.")
    if place.get("price_level"):
        attributes.append(f"Price level: {place['price_level']}")
    if place.get("rating", -1) > 0:
        attributes.append(f"Rating: {place['rating']} stars")
    if place.get("reservable", False):
        attributes.append("Reservations are available.")
    if place.get("delivery", False):
        attributes.append("Delivery services are available.")
    if place.get("dine_in", False):
        attributes.append("Dine-in is available.")
    if place.get("takeout", False):
        attributes.append("Takeout is available.")
    if place.get("serves_breakfast", False):
        attributes.append("Breakfast is served.")
    if place.get("serves_lunch", False):
        attributes.append("Lunch is served.")
    if place.get("serves_dinner", False):
        attributes.append("Dinner is served.")
    if place.get("serves_vegetarian_food", False):
        attributes.append("Vegetarian options are available.")
    if place.get("serve_alcohol", False):
        attributes.append("Alcoholic beverages are served.")

    # Combine all parts into a single string
    full_description = " ".join(descriptions + attributes).strip()
    return full_description
