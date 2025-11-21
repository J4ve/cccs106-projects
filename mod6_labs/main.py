# main.py
"""Weather Application using Flet v0.28.3"""

# Standard library imports
import flet as ft
from weather_service import WeatherService
from config import Config

# for animations
import asyncio

# for search history feature
import json
from pathlib import Path

# for geolocation support feature
import httpx

# for forecast date handling
from datetime import datetime

class WeatherApp:
    """Main Weather Application class."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()
        self.setup_page()

        # For search history feature
        self.history_file = Path("search_history.json")
        self.search_history = self.load_history()
        
        # Track view mode
        self.show_forecast = False
        self.current_city = None

        self.build_ui()


    # search history feature functions
    def load_history(self):
        """Load search history from file."""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    def save_history(self):
        """Save search history to file."""
        with open(self.history_file, 'w') as f:
            json.dump(self.search_history, f)

    def add_to_history(self, city: str):
        """Add city to history."""
        if city not in self.search_history:
            self.search_history.insert(0, city)
            self.search_history = self.search_history[:10]  # Keep last 10
            self.save_history()

    def build_history_dropdown(self) -> ft.Dropdown:
        """Build dropdown with search history."""
        return ft.Dropdown(
            label="Recent Searches",
            border_color=ft.Colors.BLUE_400,
            expand=True,
            options=[ft.dropdown.Option(city) for city in self.search_history],
            on_change=lambda e: self.on_history_select(e),
        )
    
    def on_history_select(self, e):
        """Handle selection from history dropdown."""
        selected_city = e.control.value
        if selected_city:
            self.city_input.value = selected_city
            self.page.update()
            self.on_search(None)
    # End of search history feature functions

    # Geolocation feature
    async def get_location_weather(self):
        """Get weather for current location."""
        # Fade out existing content
        if self.weather_container.visible:
            self.weather_container.opacity = 0
            self.page.update()
            await asyncio.sleep(0.2)
        if self.forecast_container.visible:
            self.forecast_container.opacity = 0
            self.page.update()
            await asyncio.sleep(0.2)
        
        self.loading.visible = True
        self.error_message.visible = False
        self.weather_container.visible = False
        self.forecast_container.visible = False
        self.page.update()
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "apiKey": Config.GEOLOCATION_API_KEY
                }
                print(f"API Key being used: {Config.GEOLOCATION_API_KEY}") #check if ginagamit talaga api
                response = await client.get(Config.GEOLOCATION_BASE_URL, params=params) # i used ipgeolocation.io since nakita ko na accurate sya
                print(f"Status code: {response.status_code}")  # test status code for what i got para sa documentation
                print(f"Response text: {response.text}")  # test return
                data = response.json()
                lat, lon = data['latitude'], data['longitude']
                weather = await self.weather_service.get_weather_by_coordinates(
                    lat, lon
                )
                # Store city name from weather data
                self.current_city = weather.get('name', '')
                await self.display_weather(weather)
                
                # Show forecast toggle button
                self.forecast_toggle.visible = True
                self.show_forecast = False
                self.forecast_toggle.text = "Show 5-Day Forecast"
                self.forecast_toggle.icon = ft.Icons.CALENDAR_MONTH
        except Exception as e:
            self.show_error("Could not get your location. Please try again.")
        finally:
            self.loading.visible = False
            self.page.update()

    def build_geolocation_button(self) -> ft.Button:
        """Build button that uses the user's location"""
        return ft.ElevatedButton(
            "Check My Weather",
            icon=ft.Icons.LOCATION_ON,
            on_click=lambda e: self.page.run_task(self.get_location_weather),
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_700,
            )
        )
    
    def setup_page(self):
        """Configure page settings."""
        self.page.title = Config.APP_TITLE
        
        # Add theme switcher
        self.page.theme_mode = ft.ThemeMode.LIGHT  # Use light theme (Pinalitan ko kasi may bug po sa icon)
        
        # Custom theme Colors
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.Colors.BLUE,
        )
        
        self.page.padding = 20
        self.page.scroll = ft.ScrollMode.AUTO  # Make page scrollable
        
        # Window properties are accessed via page.window object in Flet 0.28.3
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = Config.APP_HEIGHT
        self.page.window.resizable = False
        self.page.window.center()

    def toggle_theme(self, e):
        """Toggle between light and dark theme."""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_button.icon = ft.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_button.icon = ft.Icons.DARK_MODE
        self.page.update()
    
    def build_ui(self):
        """Build the user interface."""
        # Title
        self.title = ft.Text(
            "Weather App",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700,
        )

        # Search history dropdown
        self.history_dropdown = self.build_history_dropdown()
        
        # City input field
        self.city_input = ft.TextField(
            label="Enter city name",
            hint_text="e.g., London, Tokyo, New York",
            border_color=ft.Colors.BLUE_400,
            prefix_icon=ft.Icons.LOCATION_CITY,
            autofocus=True,
            on_submit=self.on_search,
        )
        
        # Search button
        self.search_button = ft.ElevatedButton(
            "Get Weather",
            icon=ft.Icons.SEARCH,
            on_click=self.on_search,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_700,
            ),
        )

        # Geolocation button
        self.geolocation_button = self.build_geolocation_button()
        if not self.history_dropdown.options:
            self.history_dropdown.visible = False
        else:
            self.history_dropdown.visible = True #appear lang if may laman na

        # Theme toggle button
        self.theme_button = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            tooltip="Toggle theme",
            on_click=self.toggle_theme,
        )
        
        # Weather display container (initially hidden)
        self.weather_container = ft.Container(
            visible=False,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            padding=20,
        )
        
        # Forecast display container (initially hidden)
        self.forecast_container = ft.Container(
            visible=False,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            padding=20,
        )
        
        # Toggle button for forecast
        self.forecast_toggle = ft.ElevatedButton(
            "Show 5-Day Forecast",
            icon=ft.Icons.CALENDAR_MONTH,
            visible=False,
            on_click=self.toggle_forecast_view,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.GREEN_700,
            ),
        )
        
        # Error message
        self.error_message = ft.Text(
            "",
            color=ft.Colors.RED_700,
            visible=False,
        )
        
        # Loading indicator
        self.loading = ft.ProgressRing(visible=False)
        
        # Add all components to page
        self.page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            self.title,
                            self.theme_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.history_dropdown,
                    self.city_input,
                    self.search_button,
                    self.geolocation_button,
                    self.forecast_toggle,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.loading,
                    self.error_message,
                    self.weather_container,
                    self.forecast_container,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )
    
    def on_search(self, e):
        """Handle search button click or enter key press."""
        self.page.run_task(self.get_weather)
    
    def toggle_forecast_view(self, e):
        """Toggle between current weather and forecast view."""
        if self.show_forecast:
            # Fade out forecast, show current weather
            self.show_forecast = False
            if self.forecast_container.visible:
                self.page.run_task(self._fade_out_and_show_weather)
            else:
                self.weather_container.visible = True
                self.forecast_toggle.text = "Show 5-Day Forecast"
                self.forecast_toggle.icon = ft.Icons.CALENDAR_MONTH
                self.page.update()
        else:
            # Fade out weather, show forecast
            self.show_forecast = True
            if self.weather_container.visible:
                self.page.run_task(self._fade_out_and_show_forecast)
            else:
                self.forecast_toggle.text = "Show Current Weather"
                self.forecast_toggle.icon = ft.Icons.THERMOSTAT
                self.page.run_task(self.get_and_display_forecast)
                self.page.update()
    
    async def _fade_out_and_show_weather(self):
        """Helper to fade out forecast and show weather."""
        self.forecast_container.opacity = 0
        self.page.update()
        await asyncio.sleep(0.2)
        self.forecast_container.visible = False
        
        # Show weather with fade in animation
        self.weather_container.animate_opacity = 300
        self.weather_container.opacity = 0
        self.weather_container.visible = True
        self.page.update()
        
        await asyncio.sleep(0.1)
        self.weather_container.opacity = 1
        self.forecast_toggle.text = "Show 5-Day Forecast"
        self.forecast_toggle.icon = ft.Icons.CALENDAR_MONTH
        self.page.update()
    
    async def _fade_out_and_show_forecast(self):
        """Helper to fade out weather and show forecast."""
        self.weather_container.opacity = 0
        self.page.update()
        await asyncio.sleep(0.2)
        self.weather_container.visible = False
        self.forecast_toggle.text = "Show Current Weather"
        self.forecast_toggle.icon = ft.Icons.THERMOSTAT
        await self.get_and_display_forecast()
    
    async def get_weather(self):
        """Fetch and display weather data."""
        city = self.city_input.value.strip()
        
        # Validate input
        if not city:
            self.show_error("Please enter a city name")
            return
        
        # Store current city
        self.current_city = city
        
        # Fade out existing content
        if self.weather_container.visible:
            self.weather_container.opacity = 0
            self.page.update()
            await asyncio.sleep(0.2)
        if self.forecast_container.visible:
            self.forecast_container.opacity = 0
            self.page.update()
            await asyncio.sleep(0.2)
        
        # Show loading, hide previous results
        self.loading.visible = True
        self.error_message.visible = False
        self.weather_container.visible = False
        self.forecast_container.visible = False
        self.page.update()
        
        try:
            # Fetch weather data
            weather_data = await self.weather_service.get_weather(city)
            
            # Display weather
            await self.display_weather(weather_data)
            
            # Show forecast toggle button
            self.forecast_toggle.visible = True
            self.show_forecast = False
            self.forecast_toggle.text = "Show 5-Day Forecast"
            self.forecast_toggle.icon = ft.Icons.CALENDAR_MONTH
            
        except Exception as e:
            self.show_error(str(e))
        
        finally:
            self.loading.visible = False
            self.page.update()
    
    async def display_weather(self, data: dict):
        """Display weather information."""
        # Extract data
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp = data.get("main", {}).get("temp", 0)
        feels_like = data.get("main", {}).get("feels_like", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", 0)
        
        # Animate weather container
        self.weather_container.animate_opacity = 300
        self.weather_container.opacity = 0
        self.weather_container.visible = True
        self.page.update()

        # Fade in
        await asyncio.sleep(0.1)
        self.weather_container.opacity = 1
        self.page.update()

        # Build weather display
        self.weather_container.content = ft.Column(
            [
                # Location
                ft.Text(
                    f"{city_name}, {country}",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                
                # Weather icon and description
                ft.Row(
                    [
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                            width=100,
                            height=100,
                        ),
                        ft.Text(
                            description,
                            size=20,
                            italic=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                
                # Temperature
                ft.Text(
                    f"{temp:.1f}°C",
                    size=48,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                ),
                
                ft.Text(
                    f"Feels like {feels_like:.1f}°C",
                    size=16,
                    color=ft.Colors.GREY_700,
                ),
                
                ft.Divider(),
                
                # Additional info
                ft.Row(
                    [
                        self.create_info_card(
                            ft.Icons.WATER_DROP,
                            "Humidity",
                            f"{humidity}%"
                        ),
                        self.create_info_card(
                            ft.Icons.AIR,
                            "Wind Speed",
                            f"{wind_speed} m/s"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        # Update search history
        self.add_to_history(city_name)
        self.save_history()
        self.history_dropdown.options = [ft.dropdown.Option(city) for city in self.search_history]

        # Animate search history
        if not self.history_dropdown.options:
            self.history_dropdown.visible = False
        else:
            if not self.history_dropdown.visible:
                self.history_dropdown.animate_opacity = 300
                self.history_dropdown.opacity = 0
                self.history_dropdown.visible = True
                self.page.update()

                # Fade in
                await asyncio.sleep(0.1)
                self.history_dropdown.opacity = 1
                self.page.update()
            
        self.weather_container.visible = True
        self.forecast_container.visible = False
        self.error_message.visible = False
        self.page.update()
    
    def create_info_card(self, icon, label, value):
        """Create an info card for weather details."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=30, color=ft.Colors.BLUE_700),
                    ft.Text(label, size=12, color=ft.Colors.GREY_600),
                    ft.Text(
                        value,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
            width=150,
        )
    
    def show_error(self, message: str):
        """Display error message."""
        self.error_message.value = f"❌ {message}"
        self.error_message.visible = True
        self.weather_container.visible = False
        self.page.update()
    
    async def get_and_display_forecast(self):
        """Fetch and display forecast data."""
        if not self.current_city:
            return
        
        self.loading.visible = True
        self.error_message.visible = False
        self.forecast_container.visible = False
        self.page.update()
        
        try:
            forecast_data = await self.weather_service.get_forecast(self.current_city)
            await self.display_forecast(forecast_data)
        except Exception as e:
            self.show_error(f"Error fetching forecast: {str(e)}")
        finally:
            self.loading.visible = False
            self.page.update()
    
    def process_forecast_data(self, data: dict):
        """Process forecast data and group by days."""
        forecast_list = data.get('list', [])
        daily_forecasts = {}
        
        for item in forecast_list:
            # Extract date from timestamp
            dt_txt = item.get('dt_txt', '')
            date_obj = datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')
            date_key = date_obj.strftime('%Y-%m-%d')
            day_name = date_obj.strftime('%A')
            
            if date_key not in daily_forecasts:
                daily_forecasts[date_key] = {
                    'date': date_key,
                    'day_name': day_name,
                    'temps': [],
                    'conditions': [],
                    'icons': [],
                    'humidity': [],
                    'wind_speed': []
                }
            
            # Collect data points
            daily_forecasts[date_key]['temps'].append(item['main']['temp'])
            daily_forecasts[date_key]['conditions'].append(
                item['weather'][0]['description']
            )
            daily_forecasts[date_key]['icons'].append(
                item['weather'][0]['icon']
            )
            daily_forecasts[date_key]['humidity'].append(item['main']['humidity'])
            daily_forecasts[date_key]['wind_speed'].append(item['wind']['speed'])
        
        # Calculate daily summaries
        processed = []
        for date_key in sorted(daily_forecasts.keys())[:5]:  # Only take 5 days
            day_data = daily_forecasts[date_key]
            
            # Find most common condition and icon
            conditions = day_data['conditions']
            most_common_condition = max(set(conditions), key=conditions.count)
            
            # Get icon from midday (or most common)
            icons = day_data['icons']
            most_common_icon = max(set(icons), key=icons.count)
            
            processed.append({
                'date': day_data['date'],
                'day_name': day_data['day_name'],
                'temp_min': min(day_data['temps']),
                'temp_max': max(day_data['temps']),
                'condition': most_common_condition.title(),
                'icon': most_common_icon,
                'avg_humidity': sum(day_data['humidity']) / len(day_data['humidity']),
                'avg_wind': sum(day_data['wind_speed']) / len(day_data['wind_speed'])
            })
        
        return processed
    
    async def display_forecast(self, data: dict):
        """Display 5-day forecast."""
        city_name = data.get('city', {}).get('name', 'Unknown')
        country = data.get('city', {}).get('country', '')
        
        # Process forecast data
        daily_data = self.process_forecast_data(data)
        
        # Animate forecast container
        self.forecast_container.animate_opacity = 300
        self.forecast_container.opacity = 0
        self.forecast_container.visible = True
        self.page.update()
        
        # Create tabs for each day
        tabs = []
        for day in daily_data:
            tab_content = ft.Container(
                content=ft.Column(
                    [
                        # Date
                        ft.Text(
                            day['date'],
                            size=14,
                            color=ft.Colors.GREY_700,
                        ),
                        
                        # Weather icon
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{day['icon']}@2x.png",
                            width=80,
                            height=80,
                        ),
                        
                        # Condition
                        ft.Text(
                            day['condition'],
                            size=16,
                            italic=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        
                        # Temperature range
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.ARROW_UPWARD, size=20, color=ft.Colors.RED_400),
                                ft.Text(
                                    f"{day['temp_max']:.1f}°C",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED_700,
                                ),
                                ft.VerticalDivider(width=20),
                                ft.Icon(ft.Icons.ARROW_DOWNWARD, size=20, color=ft.Colors.BLUE_400),
                                ft.Text(
                                    f"{day['temp_min']:.1f}°C",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_700,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        
                        ft.Divider(),
                        
                        # Additional details
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Icon(ft.Icons.WATER_DROP, size=24, color=ft.Colors.BLUE_700),
                                        ft.Text("Humidity", size=12, color=ft.Colors.GREY_600),
                                        ft.Text(
                                            f"{day['avg_humidity']:.0f}%",
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.VerticalDivider(width=40),
                                ft.Column(
                                    [
                                        ft.Icon(ft.Icons.AIR, size=24, color=ft.Colors.BLUE_700),
                                        ft.Text("Wind", size=12, color=ft.Colors.GREY_600),
                                        ft.Text(
                                            f"{day['avg_wind']:.1f} m/s",
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=15,
            )
            
            tabs.append(
                ft.Tab(
                    text=day['day_name'],
                    content=tab_content,
                )
            )
        
        # Build forecast display with tabs
        self.forecast_container.content = ft.Column(
            [
                # Title
                ft.Text(
                    f"5-Day Forecast: {city_name}, {country}",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                
                ft.Divider(),
                
                # Tabs
                ft.Tabs(
                    selected_index=0,
                    animation_duration=300,
                    tabs=tabs,
                    height=400,  # Fixed height for tabs
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
        
        # Fade in
        await asyncio.sleep(0.1)
        self.forecast_container.opacity = 1
        self.forecast_container.visible = True
        self.page.update()


def main(page: ft.Page):
    """Main entry point."""
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)