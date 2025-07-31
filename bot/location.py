from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pytz
from datetime import datetime
import os
import logging

tf = TimezoneFinder()

class LocationService:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="greety_bot")
        self.default_tz = pytz.timezone(os.getenv('DEFAULT_TZ', 'UTC'))

    async def generate_welcome(self, user, location):
        try:
            # Get timezone
            tz_name = tf.timezone_at(lat=location.latitude, lng=location.longitude)
            tz = pytz.timezone(tz_name) if tz_name else self.default_tz
            
            # Get address
            geo = self.geolocator.reverse(f"{location.latitude}, {location.longitude}")
            address = geo.raw.get('address', {})
            
            # Build message
            return f"""
🌍 Welcome {user.first_name} from {self._format_location(address)}!
🕒 Local time: {datetime.now(tz).strftime('%H:%M %Z')}
{self._get_weather(location) if os.getenv('WEATHER_ENABLED') == '1' else ''}
            """
        except Exception as e:
            logging.error(f"Location error: {e}")
            return f"Welcome {user.first_name}! 🎉"

    def _format_location(self, address):
        """Extract city/country from address"""
        return (
            address.get('city', '') or 
            address.get('town', '') or 
            address.get('country', 'Unknown')
        )

    def _get_weather(self, location):
        """Placeholder for weather integration"""
        return "☀️ Current weather: 24°C Sunny"
