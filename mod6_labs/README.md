# Weather Application - Module 6 Lab

## Student Information
- **Name**: Jave Atanacio Bacsain
- **Student ID**: 231003016
- **Course**: CCCS 106
- **Section**: BSCS-3A

## Project Overview
This weather application is built with Python and the Flet framework. It provides real-time weather information for cities worldwide through the OpenWeatherMap API. The application displays current temperature, humidity levels, wind speed, and weather conditions in a clean, intuitive interface that follows Material Design principles. Users can search for any city by name or use their current location to get instant weather updates. The app also maintains a searchable history of previously viewed locations for quick access.

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
     - Added a "Check My Weather" button with a location icon in the UI (Instead of the instructed "My Location" button name since I thought it is better)
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

3. **5-Day Weather Forecast with Tabbed Interface**
   - **Description**: The app now shows a 5-day weather forecast for any city you search. After you look up a city's current weather, a green "Show 5-Day Forecast" button appears. Click it, and you get tabs for each day of the week. Each tab displays that day's high and low temperatures (color-coded red for highs, blue for lows), the weather condition, an icon, and averages for humidity and wind speed. The forecast data comes from OpenWeather's forecast API, which returns weather predictions in 3-hour intervals. The app groups these intervals by day, calculates the min/max temperatures, and picks the most common weather condition to represent each day. You can switch back to the current weather view anytime by clicking "Show Current Weather."

   - **Why I chose this feature**: I wanted to give the app more depth. Showing just the current weather felt incomplete. If you're planning your week, you need to see what's coming, not just what's happening right now. A 5-day forecast made the app more practical and realistic. It's the kind of feature you'd expect from any serious weather app. Plus, I was interested in learning how to work with tabbed interfaces in Flet and how to process more complex API data. It seemed like a good way to push myself beyond the basics.

   - **Implementation Details**:
     - Added `get_forecast(city)` method to `WeatherService` that hits OpenWeather's `/forecast` endpoint
     - Forecast API returns 40 data points (3-hour intervals over 5 days), so I needed to process and group them
     - Created `process_forecast_data(data)` method that:
       - Loops through all 40 forecast entries
       - Groups them by date using `datetime.strptime()` to parse the timestamp
       - Collects temperatures, conditions, icons, humidity, and wind speed for each day
       - Calculates daily min/max temps from all intervals in that day
       - Finds the most common weather condition and icon using Python's `max()` with `key=conditions.count`
       - Returns a clean list of 5 days with all the summary data
     - Built `display_forecast(data)` method that:
       - Creates a tab for each day using `ft.Tab`
       - Each tab shows date, weather icon, condition, high/low temps with arrow icons, and humidity/wind stats
       - Uses `ft.Tabs` component with 400px fixed height (originally tried `expand=True` but tabs wouldn't show)
       - Includes fade-in animation matching the pattern from weather display
     - Added forecast toggle button that switches between current weather and forecast views
     - Made page scrollable with `self.page.scroll = ft.ScrollMode.AUTO` to fit forecast content
     - Implemented smooth fade-out/fade-in transitions when toggling between views

   - **Challenges and Solutions**:
     - *Challenge*: **API Data Structure Confusion**. When I first hit the forecast endpoint, I got back this massive JSON response with 40 entries. I didn't understand what I was looking at. Each entry had timestamps, temperatures, weather conditions, and more. I couldn't figure out how to turn that into a simple 5-day forecast. It felt overwhelming.
     - *Solution*: I spent time reading through the API response carefully. I realized each entry represented a 3-hour window, and the `dt_txt` field had the date and time. That was my key to grouping the data. I wrote a loop that parsed each timestamp with `datetime.strptime()`, extracted just the date, and grouped all entries by that date. Once I had entries grouped by day, I could calculate min/max temps and pick the most common weather condition. Breaking the problem down into steps made it manageable.

     - *Challenge*: **Dictionary Grouping Logic**. I knew I needed to group forecast entries by day, but I didn't know how to structure it. I tried using a list at first, but that got messy fast. I couldn't easily check if a day already existed or append new data to it.
     - *Solution*: Switched to a dictionary where the date string was the key and the value was another dictionary containing lists for temps, conditions, icons, etc. That made everything cleaner. I could check `if date_key not in daily_forecasts` to initialize a new day, then just append data to the existing lists. Once all data was grouped, I sorted the dictionary keys and took the first 5 days. It worked perfectly.

     - *Challenge*: **Finding Most Common Weather Condition**. Each day had multiple weather conditions from different 3-hour intervals. Some days might be partly cloudy in the morning and rainy in the afternoon. I needed to pick one condition to represent the whole day, but I didn't know how.
     - *Solution*: Used Python's `max()` function with a custom key: `max(set(conditions), key=conditions.count)`. This finds the condition that appears most frequently in the list. If a day had "clear" six times and "cloudy" twice, it would pick "clear." It was elegant once I learned about the `key` parameter.

     - *Challenge*: **Tabs Not Displaying**. This one drove me crazy for a while. I built the entire forecast UI with tabs, but when I clicked "Show 5-Day Forecast," nothing appeared. The container was visible, the data was there, but the tabs were blank. Just empty space where the forecast should've been.
     - *Solution*: The problem was `expand=True` on the `ft.Tabs` component. I thought that would make the tabs fill the available space, but instead it broke them completely. I replaced it with `height=400` to give the tabs a fixed height, and suddenly everything worked. The tabs appeared with all the forecast data. Sometimes you just have to try different approaches until something clicks.

     - *Challenge*: **Opacity Reset Issue**. When I toggled from forecast back to current weather, nothing showed up. I checked the visibility flags, and they were correct. The container was supposed to be visible, but I couldn't see it. I was stuck trying to figure out what was hiding the weather display.
     - *Solution*: Turns out the weather container's opacity was still set to 0 from when I faded it out earlier. Setting `visible=True` doesn't reset opacity. I had to manually reset it: set `opacity=0`, make it visible, update the page, then fade it back to `opacity=1`. Once I understood that visibility and opacity are separate properties, the fix was simple. Just had to handle both.

     - *Challenge*: **Geolocation Not Showing Forecast Button**. When I used "Check My Weather" to get my location's weather, everything worked fine except the forecast button didn't appear. I could search for a city and the button would show up, but using geolocation left me without the option to view the forecast. That inconsistency was annoying.
     - *Solution*: I realized I forgot to add the forecast toggle button logic inside `get_location_weather()`. I was storing the city name properly with `self.current_city = weather.get('name', '')`, but I never set the button to visible or reset its state. I copied the same lines from `get_weather()`: show the toggle button, reset the forecast state, update the button text and icon. After that, both city search and geolocation triggered the forecast button consistently.

     - *Challenge*: **Loading Circle Overlap**. When I clicked "Show 5-Day Forecast," the loading circle would appear, which was fine. But the old weather container stayed visible behind it, creating this messy overlap. You'd see the current weather, the loading circle on top of it, and then the forecast would eventually replace everything. It looked unpolished.
     - *Solution*: Added fade-out animations before showing the loading indicator. When fetching the forecast, I now fade out both `weather_container` and `forecast_container`, wait 0.2 seconds, then hide them before showing the loading circle. Same pattern when fetching new weather data. That way, the loading circle appears on a clean background. Small detail, but it made the whole experience feel smoother and more professional.


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
