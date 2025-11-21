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

4. **Weather Data Caching and Offline Mode**
   - **Description**: The app now saves weather data to your computer so you can still see the last result even when your internet cuts out. Every time you search for a city's weather or check the forecast, the app stores that information in a cache folder as JSON files. Each file includes a timestamp showing when the data was saved. If your internet connection drops or the API fails to respond, the app automatically pulls up the cached version instead of showing an error. You'll see an orange banner at the top that says "Offline Mode - Showing cached data" along with a message telling you when that data was last updated, like "5 minutes ago" or "2 hours ago." The cache expires after 30 minutes by default, but if you're offline, the app will still serve expired cache rather than leave you with nothing. It works for both current weather and the 5-day forecast, so you're covered either way.

   - **Why I chose this feature**: I got tired of seeing error messages every time my internet hiccuped. It felt wasteful. The app had already fetched the data once, so why throw it away and force another request? Real apps don't do that. They remember what you looked at. I wanted to make the app more resilient and realistic. Plus, I was curious about how caching actually works. I'd heard the term thrown around in class, but I'd never built it myself. This seemed like the perfect chance to learn file I/O, timestamp management, and graceful error handling all at once. It would also make the app feel more professional and polished, like something you'd actually want to use every day.

   - **Implementation Details**:
     - Created a new `cache.py` module with a `WeatherCache` class that handles all caching logic
     - Cache stores data in JSON files inside a `cache/` directory with filenames like `london.json` and `london_forecast.json`
     - Each cache file contains a dictionary with two keys: `timestamp` (Unix time from `time.time()`) and `data` (the actual weather or forecast response)
     - Set default cache expiry to 30 minutes (1800 seconds), but made it configurable through the constructor
     - Modified `weather_service.py` to integrate caching:
       - Added `self.cache = WeatherCache()` in `__init__` to initialize the cache manager
       - Added `self.is_offline = False` flag to track whether we're serving cached data
       - Updated `get_weather()` to check cache first with `cached_data = self.cache.get(city)` before making API calls
       - On successful API response, cache the data with `self.cache.set(city, data)` and set `is_offline = False`
       - Wrapped all API calls in try/except blocks to catch `httpx.TimeoutException`, `httpx.NetworkError`, and generic exceptions
       - If any exception occurs and cached data exists, set `is_offline = True` and return the cached data instead of raising an error
       - Applied same pattern to `get_forecast()` using separate `get_forecast()` and `set_forecast()` cache methods
       - For geolocation weather, created cache keys from coordinates like `coords_14.5995_120.9842` since there's no city name to use
     - Updated `main.py` to display cache information in the UI:
       - Added `format_last_updated(timestamp)` helper method that converts Unix timestamps to human-readable strings like "Just now," "5 minutes ago," "2 hours ago," or full date/time for older data
       - Modified `display_weather()` and `display_forecast()` to check `self.weather_service.is_offline` flag
       - Built component lists dynamically so I could conditionally add the offline banner and timestamp
       - Offline banner uses an orange background (`ft.Colors.ORANGE_50`) with a cloud-off icon and clear messaging
       - Timestamp appears in gray text below the banner, pulling data from `cache.get_timestamp()` or `cache.get_forecast_timestamp()`
       - Made sure the animations still work smoothly when showing cached vs fresh data
     - Added error handling for corrupted cache files:
       - Cache reads wrapped in try/except catching `json.JSONDecodeError` and `KeyError`
       - If a cache file is corrupted, delete it with `cache_file.unlink(missing_ok=True)` and return `None`
       - Cache writes fail silently with empty except blocks so the app keeps running even if it can't write to disk

   - **Challenges and Solutions**:
     - *Challenge*: **Cache Key for Geolocation Weather**. When you use the "Check My Weather" button, the app fetches weather by latitude and longitude, not by city name. I had no idea what to use as the cache filename. I tried using just the coordinates as the key, but then I realized the cache would never match when you searched for the same city by name later. The data was duplicated. A search for "Manila" and a geolocation search at Manila's coordinates would create two separate cache entries even though they represented the same place.
     - *Solution*: I split the problem into two parts. For the cache key, I used a formatted string with the coordinates like `coords_{lat}_{lon}`. That way, each unique location gets its own cache file even if you don't know the city name yet. But I also made sure to extract the city name from the API response after fetching the weather. The OpenWeather API includes a `name` field in every response, even for coordinate-based searches. I stored that in `self.current_city` so the rest of the app could use it properly. It's not a perfect solution since searching "Manila" and using geolocation still create separate caches, but it works well enough. The data doesn't get lost, and both searches function correctly offline.

     - *Challenge*: **Understanding When Cache Should Be Used**. At first, I thought the cache should only be used when it was still fresh, meaning less than 30 minutes old. So I wrote the logic to check the timestamp and only return cached data if it was recent. But then I realized that defeated the whole purpose of offline mode. If your internet went down and the cache was 35 minutes old, the app would just throw an error instead of showing you the slightly outdated data. That seemed silly. You'd rather see old weather than no weather at all.
     - *Solution*: I changed my approach. The cache expiry logic now works in two stages. When you have internet, the app checks if the cache is fresh. If it's less than 30 minutes old, it could theoretically serve that instead of making a new API call, though I decided to always fetch fresh data when online to keep things simple. But when the internet fails, the app ignores the expiry check completely. It looks for any cached data, even if it's hours or days old, and serves that with a clear offline indicator. That way, the user knows they're looking at old data, but at least they're looking at something. The timestamp message tells them exactly how old it is, so there's no confusion.

     - *Challenge*: **Forecast Caching Duplication**. The forecast API returns a different data structure than the current weather API. I initially tried to reuse the same cache methods for both, but it got messy. The timestamps didn't align properly, and I kept mixing up which data belonged to what. I'd save a forecast but then accidentally pull current weather data when trying to display the forecast later. It was confusing and fragile.
     - *Solution*: I created separate methods specifically for forecast caching: `get_forecast()`, `set_forecast()`, and `get_forecast_timestamp()`. They work exactly like their current weather counterparts, but they save files with a `_forecast.json` suffix instead. So if you search for London, you get two cache files: `london.json` for current weather and `london_forecast.json` for the 5-day forecast. That separation keeps everything clean and easy to manage. Each type of data has its own lifecycle, and there's no risk of accidentally serving the wrong cached data.

     - *Challenge*: **Dynamic UI Component Lists**. I wanted to show the offline banner and timestamp only when relevant, but I had already built the weather display as a single `ft.Column` with a fixed list of components. I couldn't easily inject conditional elements into the middle of that structure without rewriting everything. My first attempts involved a lot of if/else statements scattered throughout the display code, and it looked terrible. Hard to read, hard to maintain.
     - *Solution*: I switched to building the UI components as a Python list first, then passing that list to `ft.Column()` at the end. I started with the location text, then checked if we're offline. If yes, append the orange banner. Then check if there's a timestamp. If yes, append the timestamp text. After all the conditional stuff, I used `extend()` to add the rest of the weather data like the icon, temperature, humidity, and wind speed. Once the list was complete, I created the column: `ft.Column(weather_components, ...)`. This approach kept the code clean and made it easy to add or remove components without breaking the layout. I used the unpacking operator `*header_components` when building the forecast display, which felt even cleaner.

     - *Challenge*: **Timestamp Formatting Logic**. Unix timestamps are just big numbers. I needed to convert them into something human-readable like "5 minutes ago" or "2 hours ago." I'd never done time arithmetic in Python before, and I wasn't sure how to calculate the difference between two times or format it nicely. I started by just printing the raw timestamp, which looked awful in the UI.
     - *Solution*: I built a helper method called `format_last_updated()` that takes a timestamp and returns a string. First, I converted the Unix timestamp to a `datetime` object using `datetime.fromtimestamp()`. Then I got the current time with `datetime.now()` and subtracted the two to get a `timedelta` object. That gave me the difference in seconds. From there, I used simple if/else logic: if less than 60 seconds, return "Just now." If less than 3600 seconds, divide by 60 to get minutes. If less than 86400 seconds, divide by 3600 to get hours. Otherwise, format the full date and time with `strftime()`. I also added plural handling with a ternary operator like `minute{'s' if minutes != 1 else ''}` so it says "1 minute ago" instead of "1 minutes ago." Small touch, but it made the messages feel more natural.

     - *Challenge*: **Silent Cache Write Failures**. During testing, I noticed that sometimes the cache wouldn't save even though there were no visible errors. The app would fetch new weather data, display it correctly, but then if I went offline and searched again, there was no cached version available. I added print statements and realized the cache write was failing silently. Turns out the `cache/` directory didn't exist yet, and Python can't write to a folder that doesn't exist.
     - *Solution*: I added `self.cache_dir.mkdir(exist_ok=True)` in the `WeatherCache.__init__()` method. That creates the cache directory if it doesn't exist, and the `exist_ok=True` parameter prevents errors if the directory is already there. After that, cache writes worked consistently. I also wrapped all cache write operations in try/except blocks with empty except clauses. That way, if the write fails for any reason like disk full, permission error, or whatever, the app just continues without caching. It's not ideal, but it's better than crashing the entire application just because you couldn't save a cache file.

     - *Challenge*: **Offline Flag Not Resetting**. After testing offline mode, I noticed something weird. If I searched for a city while offline, the orange banner would appear. Good. But then if I searched again while online, the banner was still there even though I was clearly getting fresh data. The offline flag wasn't resetting properly between searches.
     - *Solution*: I added `self.is_offline = False` right after every successful API response in `weather_service.py`. When the API call succeeds and I cache the new data, I immediately reset the offline flag to False. That way, the next time the UI checks the flag, it knows we're back online. It's a simple fix, but I missed it at first because I was only thinking about setting the flag to True when errors occurred. I forgot to explicitly set it back to False when things went well. Now the banner only appears when it should, and it disappears as soon as we're online again.


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
