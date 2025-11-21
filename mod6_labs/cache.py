# cache.py
"""Weather data caching functionality for offline support."""

import time
import json
from pathlib import Path


class WeatherCache:
    """Cache manager for weather data with expiration logic."""
    
    def __init__(self, cache_dir="cache", expiry_minutes=30):
        """
        Initialize the cache manager.
        
        Args:
            cache_dir: Directory to store cache files
            expiry_minutes: Cache expiration time in minutes
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.expiry_seconds = expiry_minutes * 60
    
    def get(self, city: str):
        """
        Get cached weather data for a city.
        
        Args:
            city: Name of the city
            
        Returns:
            Cached weather data if available and not expired, None otherwise
        """
        cache_file = self.cache_dir / f"{city.lower()}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                    if time.time() - cached['timestamp'] < self.expiry_seconds:
                        return cached['data']
            except (json.JSONDecodeError, KeyError):
                # If cache file is corrupted, remove it
                cache_file.unlink(missing_ok=True)
        return None
    
    def set(self, city: str, data: dict):
        """
        Cache weather data for a city.
        
        Args:
            city: Name of the city
            data: Weather data to cache
        """
        cache_file = self.cache_dir / f"{city.lower()}.json"
        cached = {
            'timestamp': time.time(),
            'data': data
        }
        try:
            with open(cache_file, 'w') as f:
                json.dump(cached, f)
        except Exception as e:
            # Silently fail if we can't write cache
            pass
    
    def get_timestamp(self, city: str):
        """
        Get the timestamp of cached data.
        
        Args:
            city: Name of the city
            
        Returns:
            Timestamp when data was cached, or None if not cached
        """
        cache_file = self.cache_dir / f"{city.lower()}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                    return cached.get('timestamp')
            except (json.JSONDecodeError, KeyError):
                return None
        return None
    
    def get_forecast(self, city: str):
        """
        Get cached forecast data for a city.
        
        Args:
            city: Name of the city
            
        Returns:
            Cached forecast data if available and not expired, None otherwise
        """
        cache_file = self.cache_dir / f"{city.lower()}_forecast.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                    if time.time() - cached['timestamp'] < self.expiry_seconds:
                        return cached['data']
            except (json.JSONDecodeError, KeyError):
                cache_file.unlink(missing_ok=True)
        return None
    
    def set_forecast(self, city: str, data: dict):
        """
        Cache forecast data for a city.
        
        Args:
            city: Name of the city
            data: Forecast data to cache
        """
        cache_file = self.cache_dir / f"{city.lower()}_forecast.json"
        cached = {
            'timestamp': time.time(),
            'data': data
        }
        try:
            with open(cache_file, 'w') as f:
                json.dump(cached, f)
        except Exception:
            pass
    
    def get_forecast_timestamp(self, city: str):
        """
        Get the timestamp of cached forecast data.
        
        Args:
            city: Name of the city
            
        Returns:
            Timestamp when forecast was cached, or None if not cached
        """
        cache_file = self.cache_dir / f"{city.lower()}_forecast.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                    return cached.get('timestamp')
            except (json.JSONDecodeError, KeyError):
                return None
        return None
