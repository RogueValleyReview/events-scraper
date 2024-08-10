import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from flask import Flask, jsonify

app = Flask(__name__)

# List of websites to scrape
websites = [
    'https://www.mailtribune.com/events/',
    'https://www.travelmedford.org/events',
    'https://www.ashlandchamber.com/events',
    'https://www.eventbrite.com/d/or--rogue-valley/events/',
]

def scrape_mail_tribune(url):
    events = []
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        for event in soup.find_all('div', class_='event'):  # Example: more robust selector
            title = event.find('h3').text.strip()  # Example: flexible selector
            date = event.find('span', class_='event-date').text.strip()
            location = event.find('span', class_='event-location').text.strip()
            events.append({'title': title, 'date': date, 'location': location})
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
    return events

def scrape_travel_medford(url):
    events = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for event in soup.find_all(class_='event-item'):
            title = event.find(class_='title').text.strip()
            date = event.find(class_='date').text.strip()
            location = event.find(class_='location').text.strip()
            events.append({'title': title, 'date': date, 'location': location})
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
    return events

def scrape_ashland_chamber(url):
    events = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for event in soup.find_all(class_='chamber-event'):
            title = event.find(class_='chamber-title').text.strip()
            date = event.find(class_='chamber-date').text.strip()
            location = event.find(class_='chamber-location').text.strip()
            events.append({'title': title, 'date': date, 'location': location})
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
    return events

def scrape_eventbrite(url):
    events = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for event in soup.find_all(class_='search-event-card-wrapper'):
            title = event.find(class_='eds-event-card-content__primary-content').text.strip()
            date = event.find(class_='eds-event-card-content__sub-title').text.strip()
            location = event.find(class_='card-text--truncated__one').text.strip()
            events.append({'title': title, 'date': date, 'location': location})
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
    return events

@app.route('/events', methods=['GET'])
def get_events():
    all_events = []
    for url in websites:
        if 'mailtribune' in url:
            events = scrape_mail_tribune(url)
        elif 'travelmedford' in url:
            events = scrape_travel_medford(url)
        elif 'ashlandchamber' in url:
            events = scrape_ashland_chamber(url)
        elif 'eventbrite' in url:
            events = scrape_eventbrite(url)
        else:
            events = []
        all_events.extend(events)

    df = pd.DataFrame(all_events)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    events_json = df.to_json(orient='records')
    return jsonify(events=json.loads(events_json))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
