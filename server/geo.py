from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

def get_timezone_for_location(location_name):
    # Initialize the geocoder
    geolocator = Nominatim(user_agent="timezone_finder")

    # Get the location information (latitude, longitude) using the location name
    location = geolocator.geocode(location_name)

    if location:
        latitude, longitude = location.latitude, location.longitude

        # Initialize the TimezoneFinder
        tz_finder = TimezoneFinder()

        # Get the timezone for the given latitude and longitude
        timezone_str = tz_finder.timezone_at(lng=longitude, lat=latitude)

        return timezone_str

    else:
        print("Location not found.")
        return None

# Example usage:
def main(): 
    location_name = input("Enter location: ")
    timezone = get_timezone_for_location(location_name)

    if timezone:
        print(f"The timezone for {location_name} is {timezone}.")


if __name__ =='__main__':
    main()
