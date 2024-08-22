import requests


def get_room_availability(checkin_date, checkout_date, location):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = 'YOUR_API_KEY'
    url = 'https://api.booking.com/v1/hotels/availability'  # Example URL

    params = {
        'checkin_date': checkin_date,
        'checkout_date': checkout_date,
        'location': location,
        'api_key': api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        return data
    else:
        # Handle errors or API limit issues
        return {'error': 'Unable to fetch availability data'}