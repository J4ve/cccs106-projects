# watchlist.py
"""Watchlist management for multiple city weather comparison."""

import json
from pathlib import Path
from typing import List


class Watchlist:
    """Manage a list of cities for weather comparison."""
    
    def __init__(self, filename="watchlist.json"):
        """
        Initialize the watchlist manager.
        
        Args:
            filename: Name of the file to store watchlist data
        """
        self.watchlist_file = Path(filename)
        self.cities = self.load()
    
    def load(self) -> List[str]:
        """
        Load watchlist from file.
        
        Returns:
            List of city names in the watchlist
        """
        if self.watchlist_file.exists():
            try:
                with open(self.watchlist_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save(self):
        """Save current watchlist to file."""
        try:
            with open(self.watchlist_file, 'w') as f:
                json.dump(self.cities, f)
        except IOError:
            pass  # Fail silently if we can't save
    
    def add(self, city: str) -> bool:
        """
        Add a city to the watchlist.
        
        Args:
            city: Name of the city to add
            
        Returns:
            True if city was added, False if it already exists
        """
        if city not in self.cities:
            self.cities.append(city)
            self.save()
            return True
        return False
    
    def remove(self, city: str) -> bool:
        """
        Remove a city from the watchlist.
        
        Args:
            city: Name of the city to remove
            
        Returns:
            True if city was removed, False if it wasn't in the list
        """
        if city in self.cities:
            self.cities.remove(city)
            self.save()
            return True
        return False
    
    def get_all(self) -> List[str]:
        """
        Get all cities in the watchlist.
        
        Returns:
            List of city names
        """
        return self.cities.copy()
    
    def clear(self):
        """Remove all cities from the watchlist."""
        self.cities = []
        self.save()
    
    def count(self) -> int:
        """
        Get the number of cities in the watchlist.
        
        Returns:
            Number of cities
        """
        return len(self.cities)
