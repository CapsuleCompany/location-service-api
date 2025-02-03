import requests
from datetime import datetime
from django.conf import settings


def get_zip_codes_within_radius(zip_code, distance, units="miles"):
    """
    Fetches ZIP codes within a given radius of a specified ZIP code using ZipcodeAPI.

    :param zip_code: (str) The base ZIP code to search around.
    :param distance: (int) The search radius (max 500 miles unless unlimited plan).
    :param units: (str) "miles" or "km" (default is "miles").
    :return: (list) A list of ZIP codes within the specified radius.
    """

    API_KEY = getattr(settings, "ZIPCODE_API_KEY", None)

    if not API_KEY:
        raise ValueError("ZIPCODE_API_KEY is not set in Django settings.")

    url = f"https://www.zipcodeapi.com/rest/{API_KEY}/radius.json/{zip_code}/{distance}/{units}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "zip_codes" in data:
            return [zip_info["zip_code"] for zip_info in data["zip_codes"]]
        else:
            print("No ZIP codes found in the specified radius.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching ZIP codes: {e}")
        return []


zip_codes = get_zip_codes_within_radius("45440", 5)
print(zip_codes)


def update_zip_codes(zip_code, distance):
    """
    Periodically fetch updated ZIP codes to ensure service areas remain accurate.
    """
    API_KEY = getattr(settings, "ZIPCODE_API_KEY", None)
    base_zip = zip_code
    distance = distance
    url = f"https://www.zipcodeapi.com/rest/{API_KEY}/radius.json/{base_zip}/{distance}/miles"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "zip_codes" in data:
            zip_codes = [zip_info["zip_code"] for zip_info in data["zip_codes"]]
            print(f"Updated ZIP codes as of {datetime.now()}: {zip_codes}")
            return zip_codes
    except requests.exceptions.RequestException as e:
        print(f"Error updating ZIP codes: {e}")
        return []


update_zip_codes()
