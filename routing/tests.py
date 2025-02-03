from django.conf import settings
import requests


def extract_address_components(address_components):
    """Extract structured address fields from Google Maps API response."""
    address_data = {
        "address_line_1": "",
        "address_line_2": "",
        "city": "",
        "state": "",
        "postal_code": "",
        "country": "",
        "latitude": None,
        "longitude": None,
        "valid": False,
    }

    for component in address_components:
        types = component["types"]
        if "street_number" in types:
            address_data["address_line_1"] = component["long_name"] + " "
        if "route" in types:
            address_data["address_line_1"] += component["long_name"]
        if "subpremise" in types:
            address_data["address_line_2"] = component["long_name"]
        if "locality" in types:
            address_data["city"] = component["long_name"]
        if "administrative_area_level_1" in types:
            address_data["state"] = component["short_name"]
        if "postal_code" in types:
            address_data["postal_code"] = component["long_name"]
        if "country" in types:
            address_data["country"] = component["long_name"]

    return address_data


def validate_address(address):
    """Validate an address using Google Maps API and return structured data."""
    api_key = settings.GOOGLE_MAPS_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}

    response = requests.get(base_url, params=params)
    data = response.json()

    if data.get("status") == "OK":
        result = data["results"][0]
        address_components = result["address_components"]
        location = result["geometry"]["location"]

        structured_address = extract_address_components(address_components)
        structured_address["latitude"] = location["lat"]
        structured_address["longitude"] = location["lng"]
        structured_address["valid"] = True

        return structured_address

    return {"valid": False, "error": "Invalid Address"}
