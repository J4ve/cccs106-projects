# Weather Application - Module 6 Lab

## Student Information
- **Name**: Jave Atanacio Bacsain
- **Student ID**: 231003016
- **Course**: CCCS 106
- **Section**: BSCS-3A

## Project Overview
This is a weather application I built using Python and the Flet framework. It pulls real-time weather data from cities around the world through the OpenWeatherMap API. The interface follows Material Design principles. It's clean, intuitive, and easy to navigate. Users can check current weather conditions like temperature, humidity, wind speed, and get a description of what's happening outside.

Building this taught me more than I expected. I got hands-on experience with asynchronous programming, learning how `async/await` works with `page.run_task()` to keep the UI responsive while fetching data. I integrated a real API for the first time, dealing with error handling and making sure the app doesn't break when things go wrong. I implemented persistent storage using JSON files, so user data sticks around between sessions. The UI work involved animations and real-time updates, which was challenging but rewarding. And throughout all of this, I got a much better grasp of object-oriented design. I learned how to structure classes properly and keep concerns separated.

The development process wasn't smooth. I struggled with Python's OOP fundamentals, especially understanding when and why to use `self`. Managing the initialization order of class attributes was confusing at first. Getting components to update in real-time took several attempts. And figuring out how to handle events between user interactions and asynchronous operations required patience and a lot of trial and error. But each challenge taught me something new, and I'm happy with how it turned out.

## Features Implemented

### Base Features
- [x] City search functionality
- [x] Current weather display
- [x] Temperature, humidity, wind speed
- [x] Weather icons
- [x] Error handling
- [x] Modern UI with Material Design

### Enhanced Features
1. **Search History with Persistent Storage**
   - **Description**: The app automatically saves the last 10 cities you've searched in a JSON file called `search_history.json`. These show up in a dropdown menu, so you can click on any city you've searched before and get its weather instantly without needing to type it again. The history sticks around even after you close the app, and it updates in real-time as you search for new places.
   
   - **Why I chose this feature**: I wanted to make the app feel more practical for everyday use. If you're the kind of person who checks weather for the same few cities regularly, typing them over and over gets old fast. This feature just made sense. It reduces repetition and makes the whole experience smoother. Plus, it gave me a chance to work with file I/O and state management, which I knew I needed more practice with.
   
   - **Implementation Details**:
     - Used JSON for storage with Python's `pathlib` library to keep things cross-platform
     - Built a dropdown menu that populates automatically from the saved history
     - Added a function so the same city doesn't show up twice
     - Most recent searches appear at the top (last-in, first-out)
     - Limited history to 10 entries to keep things fast and manageable
     - Dropdown refreshes in real-time after every successful search
     - Added fade-in animation for the dropdown using opacity transitions (borrowed the pattern from the weather container animation)
     - Dropdown only appears when there's actual search history. If you haven't searched for anything yet, it stays hidden to keep the UI clean
   
   - **Challenges and Solutions**: 
     - *Challenge*: **Initialization Order Issues**. I didn't understand when to load the history data. I kept getting errors because I was trying to build UI components before the data even existed.
     - *Solution*: I moved `self.search_history = self.load_history()` before `self.build_ui()` in the `__init__` method. That way, the data is there when the dropdown gets created. Simple fix once I understood the flow.
     
     - *Challenge*: **Understanding Python OOP and `self`**. This one took me a while. I kept forgetting when to use `self` and why. Sometimes I'd call methods without it and wonder why Python couldn't find them.
     - *Solution*: I finally got it. The `self` keyword refers to the specific instance of the class. It's how you access methods and variables that belong to that instance. Without it, Python looks for standalone functions instead. Once that clicked, things made a lot more sense.
     
     - *Challenge*: **Event Handling and Callbacks**. I had no idea how to capture the city someone selected from the dropdown and actually trigger a search with it.
     - *Solution*: I created a separate method called `on_history_select(e)`. It grabs the selected value with `e.control.value`, updates the text input field, and then calls `self.on_search(None)` to start the search. Breaking it into steps helped me understand the event flow better.
     
     - *Challenge*: **Real-time UI Updates**. The dropdown wasn't refreshing. I'd search for a new city, and it wouldn't show up in the history until I restarted the entire app. That was frustrating.
     - *Solution*: After adding a city to history, I had to manually rebuild the dropdown's options: `self.history_dropdown.options = [ft.dropdown.Option(city) for city in self.search_history]` and then call `self.page.update()`. That forced the UI to refresh with the new data.
     
     - *Challenge*: **Function Parameter Mismatch**. My `on_search(self, e)` method expected an event parameter. That worked fine when someone clicked the search button, but when I tried to call it manually from the history selection, there was no event to pass. Python threw errors.
     - *Solution*: I made the parameter optional: `def on_search(self, e=None)`. Now it works whether it's called from a button click or programmatically. Problem solved.
     
     - *Challenge*: **Dropdown Options Data Type**. I thought I could just assign a list of city names directly to the dropdown. Nope. The dropdown wanted `ft.dropdown.Option` objects, not raw strings.
     - *Solution*: Used a list comprehension to convert properly: `[ft.dropdown.Option(city) for city in self.search_history]`. Once I did that, everything worked as expected.

2. **Current Location Weather with IP Geolocation**
   - **Description**: The app can automatically detect your location and show you the weather where you are right now. When you click the "Check My Weather" button, it uses your IP address to figure out your coordinates, then fetches the weather for that exact spot. No typing needed. Just one click and you get your local weather instantly. It works through the ipgeolocation.io API, which takes your IP and returns latitude and longitude coordinates. The app then passes those coordinates to OpenWeather's API to get the actual weather data.

   - **Why I chose this feature**: I wanted to make the app more convenient. Sometimes you just want to know what the weather's like right where you are without having to type in your city name. It felt like a natural addition since most weather apps do this. Plus, I was curious about how geolocation works and how different APIs communicate with each other. It seemed like a good challenge that would teach me something useful.

   - **Implementation Details**:
     - Integrated ipgeolocation.io API for IP-based location detection
     - Added new configuration variables in `Config` class for the geolocation API key and base URL
     - Created `get_weather_by_coordinates(lat, lon)` method in `WeatherService` to handle coordinate-based weather queries
     - Built `get_location_weather()` async method that fetches coordinates and retrieves weather data
     - Added a "Check My Weather" button with a location icon in the UI
     - Used the same loading and error handling pattern as the city search feature
     - Reused the existing `display_weather()` method to show results without duplicating code

   - **Challenges and Solutions**:
     - *Challenge*: **API Endpoint Confusion**. I kept getting responses that only contained my IP address, not my location coordinates. The API was returning `{"ip":"136.158.100.115"}` instead of the full location data I needed. I was stuck for a while trying to figure out what was wrong.
     - *Solution*: Turns out I was using the wrong endpoint. I was hitting `/getip` when I should've been using `/ipgeo`. The `/getip` endpoint only returns your IP, nothing else. Once I switched to `/ipgeo`, I got back all the location data including latitude and longitude. Lesson learned: always double-check the API documentation before assuming the endpoint is correct.

     - *Challenge*: **Missing API Key in Request**. Even after fixing the endpoint, the API kept rejecting my requests with a 401 error. The response said I needed to provide an API key, but I thought I had already set it up in my `.env` file. I was confused because it worked fine for the OpenWeather API.
     - *Solution*: The problem was in `config.py`. I was using `os.getenv("apiKey", "")` but my `.env` file had the variable named `GEOLOCATION_API_KEY`. The names didn't match, so Python couldn't find the key. I standardized everything by changing `config.py` to look for `GEOLOCATION_API_KEY` and making sure my `.env` file used the same name. Then I passed the key as a query parameter using `params={"apiKey": Config.GEOLOCATION_API_KEY}`. After that, the API accepted my requests.

     - *Challenge*: **Nested JSON Response Structure**. I tried to access `data['latitude']` and `data['longitude']` directly, but Python threw a KeyError. I printed out the response and saw that the coordinates weren't at the top level. They were nested inside a `location` object. That wasn't obvious from the API docs I skimmed.
     - *Solution*: Updated my code to access the nested structure properly: `lat, lon = data['location']['latitude'], data['location']['longitude']`. I also added print statements during testing to inspect the full JSON response. That helped me understand the structure before writing the final code.

     - *Challenge*: **Async Function Button Click Error**. When I first wired up the button, I got a weird error: `TypeError: 'coroutine' object is not callable`. The app crashed every time I clicked the location button. I had no idea what a "coroutine object" even was at that point.
     - *Solution*: The issue was how I set up the button's `on_click`. I wrote `on_click=self.get_location_weather()` with parentheses, which called the function immediately instead of passing it as a callback. Since `get_location_weather()` is async, it returned a coroutine object, and the button didn't know what to do with that. I fixed it by using a lambda: `on_click=lambda e: self.page.run_task(self.get_location_weather)`. That way, the function only runs when the button is actually clicked, and `run_task()` handles the async execution properly.


## Screenshots
[Add 3-5 screenshots showing different aspects of your app]

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/<username>/cccs106-projects.git
cd cccs106-projects/mod6_labs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your OpenWeatherMap API key to .env
```
