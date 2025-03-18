# Natural language processing course: `coccodrillo`


# Project Name

Welcome to the **[coccodrillo]** repository! This project is designed to [to do].

## Directory Structure

Below is an explanation of the key directories and files in this repository:

### `events/`

This directory contains scripts related to event searches.

- **`events.py`**: This script takes a start date, end date, a city name, and an event type as inputs. It searches for matching events on the website [Bandsintown](https://www.bandsintown.com/). The script collects information about the events, such as the event name, location, and time, and saves the data in a file.

  - **Start Date**: `"2025-03-17"`
  - **End Date**: `"2025-03-27"`
  - **City**: `"Rome"`

  It uses the `geckodriver` and the Firefox web driver to scrape the data with headless mode enabled.

### `foods/`

This directory contains scripts related to food and restaurant searches.

- **`restaurants.py`**: Given a city, this script searches for the best restaurants on [Yelp](https://www.yelp.com/). It collects restaurant names, reviews, and locations, and saves this information into a file.

### `geography/`

This directory contains a CSV file with city names, latitude, and longitude.

- **`get_geo.py`**: This script calculates the distance between two cities using the latitude and longitude data available in the CSV file. The output is the geographical distance between the two cities.

### `weather/`

This directory contains scripts related to weather forecasts.

- **`weather.py`**: This script fetches weather forecasts for a given city from [IlMeteo.it](https://www.ilmeteo.it/meteo/). It generates a file with the weather predictions for the next 15 days.

### `news/`

This directory contains scripts for retrieving news articles.

- **`get_news.py`**: This script fetches news articles for a specific city and news topic from [Bing News](https://www.bing.com/news/). The script takes a search query and the number of articles to retrieve as input, then returns a list of article links.


## How to Run the Project

1. Clone the repository:

  to do

