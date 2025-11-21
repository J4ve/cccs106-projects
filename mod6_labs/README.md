# Weather Application - Module 6 Lab

## Student Information
- **Name**: Jave Atanacio Bacsain
- **Student ID**: 231003016
- **Course**: CCCS 106
- **Section**: BSCS-3A

## Project Overview
This is a weather application I built using Python and the Flet framework. It pulls real-time weather data from cities around the world through the OpenWeatherMap API. The interface follows Material Design principles—clean, intuitive, and easy to navigate. Users can check current weather conditions like temperature, humidity, wind speed, and get a description of what's happening outside.

Building this taught me more than I expected. I got hands-on experience with asynchronous programming, learning how `async/await` works with `page.run_task()` to keep the UI responsive while fetching data. I integrated a real API for the first time, dealing with error handling and making sure the app doesn't break when things go wrong. I implemented persistent storage using JSON files, so user data sticks around between sessions. The UI work involved animations and real-time updates, which was challenging but rewarding. And throughout all of this, I got a much better grasp of object-oriented design—how to structure classes properly and keep concerns separated.

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
   - **Description**: The app automatically saves the last 10 cities you've searched in a JSON file called `search_history.json`. These show up in a dropdown menu, so you can click on any city you've searched before and get its weather instantly—no need to type it again. The history sticks around even after you close the app, and it updates in real-time as you search for new places.
   
   - **Why I chose this feature**: I wanted to make the app feel more practical for everyday use. If you're the kind of person who checks weather for the same few cities regularly, typing them over and over gets old fast. This feature just made sense. It reduces repetition and makes the whole experience smoother. Plus, it gave me a chance to work with file I/O and state management, which I knew I needed more practice with.
   
   - **Implementation Details**:
     - Used JSON for storage with Python's `pathlib` library to keep things cross-platform
     - Built a dropdown menu that populates automatically from the saved history
     - Added smart deduplication so the same city doesn't show up twice
     - Most recent searches appear at the top (last-in, first-out)
     - Limited history to 10 entries to keep things fast and manageable
     - Dropdown refreshes in real-time after every successful search
   
   - **Challenges and Solutions**: 
     - *Challenge*: **Initialization Order Issues** - I didn't understand when to load the history data. I kept getting errors because I was trying to build UI components before the data even existed.
     - *Solution*: I moved `self.search_history = self.load_history()` before `self.build_ui()` in the `__init__` method. That way, the data is there when the dropdown gets created. Simple fix once I understood the flow.
     
     - *Challenge*: **Understanding Python OOP and `self`** - This one took me a while. I kept forgetting when to use `self` and why. Sometimes I'd call methods without it and wonder why Python couldn't find them.
     - *Solution*: I finally got it—`self` refers to the specific instance of the class. It's how you access methods and variables that belong to that instance. Without it, Python looks for standalone functions instead. Once that clicked, things made a lot more sense.
     
     - *Challenge*: **Event Handling and Callbacks** - I had no idea how to capture the city someone selected from the dropdown and actually trigger a search with it.
     - *Solution*: I created a separate method called `on_history_select(e)`. It grabs the selected value with `e.control.value`, updates the text input field, and then calls `self.on_search(None)` to start the search. Breaking it into steps helped me understand the event flow better.
     
     - *Challenge*: **Real-time UI Updates** - The dropdown wasn't refreshing. I'd search for a new city, and it wouldn't show up in the history until I restarted the entire app. That was frustrating.
     - *Solution*: After adding a city to history, I had to manually rebuild the dropdown's options: `self.history_dropdown.options = [ft.dropdown.Option(city) for city in self.search_history]` and then call `self.page.update()`. That forced the UI to refresh with the new data.
     
     - *Challenge*: **Function Parameter Mismatch** - My `on_search(self, e)` method expected an event parameter. That worked fine when someone clicked the search button, but when I tried to call it manually from the history selection, there was no event to pass. Python threw errors.
     - *Solution*: I made the parameter optional: `def on_search(self, e=None)`. Now it works whether it's called from a button click or programmatically. Problem solved.
     
     - *Challenge*: **Dropdown Options Data Type** - I thought I could just assign a list of city names directly to the dropdown. Nope. The dropdown wanted `ft.dropdown.Option` objects, not raw strings.
     - *Solution*: Used a list comprehension to convert properly: `[ft.dropdown.Option(city) for city in self.search_history]`. Once I did that, everything worked as expected.

   



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
