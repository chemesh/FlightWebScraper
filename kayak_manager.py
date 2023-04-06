import requests
import time
from bs4 import BeautifulSoup
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By

from consts import HEADERS
from datamodels import Flight, Trip


class KayakManager:
    URL_ROOT = 'https://www.kayak.com/flights'
    URL_SUFFIX = '?sort=bestflight_a' # &pid=deeplinks'
    _DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, origin: str, destination: str, depart_date: dt.datetime, return_date: dt.datetime,
                 class_: str = "economy", passengers: int = 1):
        self.origin = origin
        self.dest = destination
        self.depart_date = depart_date
        self.return_date = return_date
        self.class_ = class_
        self.num_of_passengers = passengers

        self.url = f'{self.URL_ROOT}/{origin}-{destination}/{depart_date.strftime(self._DATE_FORMAT)}/{return_date.strftime(self._DATE_FORMAT)}/{class_}/{passengers}adults{self.URL_SUFFIX} '
        # self.session = requests.session()
        # self.session.headers.update(HEADERS)

    def get_trips(self):
        res = []
        print(f'url: {self.url}')
        # response = self.session.get(url=self.url)
        # soup = BeautifulSoup(response.content, 'html.parser')

        browser = webdriver.Firefox()
        browser.get(url=self.url)
        time.sleep(3)
        blocks = browser.find_elements(By.CLASS_NAME, 'nrc6')
        _ = [block.click() for block in blocks]
        time.sleep(2)

        # print(f'browser.page_source: {browser.page_source}')
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        trips_html = soup.find_all('div', class_='nrc6')
        for raw_trip in trips_html:
            trip_data = Trip(
                depart_flights=[],
                return_flights=[],
                price=raw_trip.find('div', class_='f8F1-price-text').text,
                cabin=raw_trip.find('div', class_='aC3z-name').text,
                provider=raw_trip.find('div', class_='M_JD-provider-name').text,
                link=raw_trip.find('div', class_='oVHK').find('a').get('href'),
            )
            trip_info = raw_trip.find_all('div', class_='o-C7-leg-outer')
            for i, way in enumerate(trip_info):
                flights_info = way.find_all('div', class_='nAz5')
                for flight in flights_info:
                    flight_id = raw_trip.find('div', class_='nAz5-carrier-text').text
                    flight_data = Flight(
                        flight_id=flight_id,
                        origin=raw_trip.findNext('span', class_='g16k-station').text,
                        destination=raw_trip.findNext('span', class_='g16k-station').text,
                        date=way.find('span', class_='X3K_-header-text').text.split(' • ')[1],
                        departure=flight.findNext('span', class_='g16k-time').text,
                        arrival=flight.findNext('span', class_='g16k-time').text,
                        operator=flight_id[:flight_id.rfind(' ')],
                        warnings=[warn.text for warn in flight.find_all('span', class_='g16k-date-warning-badge')]
                    )
                    trip_data.depart_flights.append(flight_data) if i == 0 else \
                        trip_data.return_flights.append(flight_data)

            res.append(trip_data)
        browser.close()
        return res

