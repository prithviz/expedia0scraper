__AUTHOR__ = "Tony"

"""
This module will scrap results of flights from Expedia.
very limited functionality
"""

import json
import requests
from lxml import html


def scrape(source, destination, date, adults, children):
    """
    :param source: From Where  String
    :param destination: to Where String
    :param date: date of journey d/m/y casted in string
    :param adults: integer (max 6 excluding others) casted in string
    :param children: int no[age] ex. 2[12,16] String
    :return: 
    """
    for i in range(5):
        try:
            url = "https://www.expedia.co.in/Flights-Search?trip=oneway&leg1=from:{0},to:{1},departure:" \
                  "{2}TANYT&passengers=adults:{3},children:{4},seniors:0," \
                  "infantinlap:Y&mode=search".format(source, destination, date, adults, children)
            response = requests.get(url)
            parser = html.fromstring(response.text)
            json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")
            print len(json_data_xpath), "XPATH"
            if len(json_data_xpath) == 1:
                raw_json = json.loads(json_data_xpath[0])
                flight_data = json.loads(raw_json["content"])
                lists = []
                for j in flight_data['legs'].keys():
                    total_distance = flight_data['legs'][j]['formattedDistance']
                    exact_price = flight_data['legs'][j]['price']['formattedTotalPrice']

                    departure_location_city = flight_data['legs'][j]['departureLocation']['airportCity']
                    departure_location_airport_code = flight_data['legs'][j]['departureLocation']['airportCode']

                    arrival_location_city = flight_data['legs'][j]['arrivalLocation']['airportCity']
                    arrival_location_airport_code = flight_data['legs'][j]['arrivalLocation']['airportCode']

                    airline_name = flight_data['legs'][j]['carrierSummary']['airlineName']

                    no_of_stops = flight_data['legs'][j]['stops']

                    flight_duration = flight_data['legs'][j]['duration']
                    flight_hour = flight_duration['hours']
                    flight_minutes = flight_duration['minutes']
                    flight_days = flight_duration['numOfDays']
                    adultCount = flight_data['summary']['searchOptions']['traveler']['adultCount']
                    childrenCount = flight_data['summary']['searchOptions']['traveler']['childCount']
                    if no_of_stops == 0:
                        stop = "Non-Stop"
                    else:
                        stop = str(no_of_stops) + ' Stops'

                    total_flight_duration = "{0} days {1} hours {2} minutes".format(flight_days, flight_hour,
                                                                                    flight_minutes)
                    departure = departure_location_city
                    arrival = arrival_location_city
                    carrier = flight_data['legs'][j]['timeline'][0]['carrier']
                    plane = carrier['plane']
                    plane_code = carrier['planeCode']
                    formatted_price = exact_price
                    if not airline_name:
                        airline_name = carrier['operatedBy']

                    timings = []
                    for timeline in flight_data['legs'][j]['timeline']:
                        if 'departureAirport' in timeline.keys():
                            departure_airport = timeline['departureAirport']['longName']
                            departure_time = timeline['departureTime']['time']
                            departure_date = timeline['departureTime']['date']
                            departure_date_longStr = timeline['departureTime']['dateLongStr']

                            arrival_airport = timeline['arrivalAirport']['longName']
                            arrival_time = timeline['arrivalTime']['time']
                            arrival_date = timeline['arrivalTime']['date']
                            arrival_date_longStr = timeline['arrivalTime']['dateLongStr']

                            flight_timing = {
                                'departure_airport': departure_airport,
                                'departure_date': departure_date,
                                'departure_date_longStr': departure_date_longStr,
                                'departure_time': departure_time,

                                'arrival_airport': arrival_airport,
                                'arrival_date': arrival_date,
                                'arrival_date_longStr': arrival_date_longStr,
                                'arrival_time': arrival_time
                            }
                            timings.append(flight_timing)

                    flight_info = {
                        'stops': stop,
                        'ticket_price': formatted_price,
                        'departure': departure,
                        'arrival': arrival,
                        'departure_location_airport_code': departure_location_airport_code,
                        'arrival_location_airport_code': arrival_location_airport_code,
                        'flight_duration': total_flight_duration,
                        'airline': airline_name,
                        'plane': plane,
                        'plane_code': plane_code,
                        'adultCount': adultCount,
                        'childCount': childrenCount,
                        'timings': timings,
                    }

                    lists.append(flight_info)
                sortedlist = sorted(lists, key=lambda k: k['ticket_price'], reverse=False)
                return sortedlist
            else:
                return ValueError
        except ValueError:
            print ValueError


class search_flight(object):
    @staticmethod
    def flights(param1, param2, param3, param4, param5):
        return scrape(param1, param2, param3, param4, param5)
