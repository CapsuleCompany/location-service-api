"""
Address Validation Module

This module provides functions to validate addresses using the Google Maps Geocoding API.
It extracts structured address components such as street, city, state, postal code, and country,
and also retrieves geographic coordinates (latitude and longitude).

Functions:
- extract_address_components(address_components): Parses the Google Maps API response to extract 
  structured address fields like address line 1, address line 2, city, state, postal code, and country.

- validate_address(address): Sends a request to the Google Maps Geocoding API to validate an address 
  and returns structured address details along with latitude, longitude, and validation status.

Dependencies:
- requests (for making API calls)
- Django settings (expects `GOOGLE_MAPS_API_KEY` to be configured)

Usage Example:
    validated_address = validate_address("1600 Amphitheatre Parkway, Mountain View, CA")
    if validated_address["valid"]:
        print("Address is valid:", validated_address)
    else:
        print("Invalid address:", validated_address["error"])

Author: Camryn Crowder
Date: 01/29/2025
"""

import requests
from django.conf import settings


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
    status = data.get("status")

    if status == "OK":
        result = data["results"][0]
        address_components = result["address_components"]
        location = result["geometry"]["location"]

        structured_address = extract_address_components(address_components)
        structured_address["latitude"] = location["lat"]
        structured_address["longitude"] = location["lng"]
        structured_address["valid"] = True

        return structured_address
    elif status == "ZERO_RESULTS":
        return {"valid": False, "error": "No results found"}
    elif status == "REQUEST_DENIED":
        return {"valid": False, "error": "Request denied"}
    elif status == "INVALID_REQUEST":
        return {"valid": False, "error": "Invalid request"}
    elif status == "UNKNOWN_ERROR":
        return {"valid": False, "error": "Unknown error"}
    return {"valid": False, "error": "Invalid Address"}
