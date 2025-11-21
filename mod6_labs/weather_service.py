# weather_service.py
"""Weather API service layer."""

import httpx
from typing import Dict, Optional
from config import Config
from datetime import datetime
from cache import WeatherCache


class WeatherServiceError(Exception):
    """Custom exception for weather service errors."""
    pass


class WeatherService:
    """Service for fetching weather data from OpenWeatherMap API."""
    
    def __init__(self):
        self.api_key = Config.API_KEY
        self.base_url = Config.BASE_URL
        self.timeout = Config.TIMEOUT
        self.cache = WeatherCache(cache_dir="cache", expiry_minutes=30)
        self.is_offline = False  # Track offline status
    
    async def get_weather(self, city: str) -> Dict:
        """
        Fetch weather data for a given city.
        
        Args:
            city: Name of the city
            
        Returns:
            Dictionary containing weather data
            
        Raises:
            WeatherServiceError: If the request fails
        """
        if not city:
            raise WeatherServiceError("City name cannot be empty")
        
        # Check cache first
        cached_data = self.cache.get(city)
        
        # Build request parameters
        params = {
            "q": city,
            "appid": self.api_key,
            "units": Config.UNITS,
        }
        
        try:
            # Make async HTTP request
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.base_url, params=params)
                
                # Check for HTTP errors
                if response.status_code == 404:
                    raise WeatherServiceError(
                        f"City '{city}' not found. Please check the spelling."
                    )
                elif response.status_code == 401:
                    raise WeatherServiceError(
                        "Invalid API key. Please check your configuration."
                    )
                elif response.status_code >= 500:
                    raise WeatherServiceError(
                        "Weather service is currently unavailable. "
                        "Please try again later."
                    )
                elif response.status_code != 200:
                    raise WeatherServiceError(
                        f"Error fetching weather data: {response.status_code}"
                    )
                
                # Parse JSON response
                data = response.json()
                
                # Cache the successful response
                self.cache.set(city, data)
                self.is_offline = False
                
                return data
                
        except httpx.TimeoutException:
            # Try to use cached data if available
            if cached_data:
                self.is_offline = True
                return cached_data
            raise WeatherServiceError(
                "Request timed out. Please check your internet connection."
            )
        except httpx.NetworkError:
            # Try to use cached data if available
            if cached_data:
                self.is_offline = True
                return cached_data
            raise WeatherServiceError(
                "Network error. Please check your internet connection."
            )
        except httpx.HTTPError as e:
            # Try to use cached data if available
            if cached_data:
                self.is_offline = True
                return cached_data
            raise WeatherServiceError(f"HTTP error occurred: {str(e)}")
        except Exception as e:
            # Try to use cached data if available
            if cached_data:
                self.is_offline = True
                return cached_data
            raise WeatherServiceError(f"An unexpected error occurred: {str(e)}")
    
    async def get_weather_by_coordinates(
        self, 
        lat: float, 
        lon: float
    ) -> Dict:
        """
        Fetch weather data by coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary containing weather data
        """
        # Create a cache key from coordinates
        cache_key = f"coords_{lat}_{lon}"
        cached_data = self.cache.get(cache_key)
        
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": Config.UNITS,
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Cache the successful response
                self.cache.set(cache_key, data)
                self.is_offline = False
                
                return data
                
        except Exception as e:
            # Try to use cached data if available
            if cached_data:
                self.is_offline = True
                return cached_data
            raise WeatherServiceError(f"Error fetching weather data: {str(e)}")
    
    async def get_forecast(self, city: str) -> Dict: # for the forecast feature I added
        """Get 5-day forecast."""
        # Check cache first
        cached_data = self.cache.get_forecast(city)
        
        forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": Config.UNITS,
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(forecast_url, params=params)
                
                if response.status_code == 404:
                    raise WeatherServiceError(
                        f"City '{city}' not found. Please check the spelling."
                    )
                elif response.status_code == 401:
                    raise WeatherServiceError(
                        "Invalid API key. Please check your configuration."
                    )
                elif response.status_code >= 500:
                    raise WeatherServiceError(
                        "Weather service is currently unavailable. "
                        "Please try again later."
                    )
                elif response.status_code != 200:
                    raise WeatherServiceError(
                        f"Error fetching forecast data: {response.status_code}"
                    )
                
                data = response.json()
                
                # Cache the successful response
                self.cache.set_forecast(city, data)
                self.is_offline = False
                
                return data
                
        except httpx.TimeoutException:
            # Try to use cached data if available
            if cached_data:
                self.is_offline = True
                return cached_data
            raise WeatherServiceError(
                "Request timed out. Please check your internet connection."
            )
        except httpx.NetworkError:
            # Try to use cached data if available
            if cached_data:
                self.is_offline = True
                return cached_data
            raise WeatherServiceError(
                "Network error. Please check your internet connection."
            )
        except httpx.HTTPError as e:
            # Try to use cached data if available
            if cached_data:
                self.is_offline = True
                return cached_data
            raise WeatherServiceError(f"HTTP error occurred: {str(e)}")
        except Exception as e:
            # Try to use cached data if available
            if cached_data:
                self.is_offline = True
                return cached_data
            raise WeatherServiceError(f"An unexpected error occurred: {str(e)}")