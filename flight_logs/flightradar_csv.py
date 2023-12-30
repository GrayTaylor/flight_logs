from geopy import Point
from geopy.distance import geodesic
from typing import List
import datetime as dt
import pandas as pd


class FlightLogRecord:
    def __init__(self, timestamp, UTC: dt.datetime, callsign,
                 lat, lon, altitude, speed, direction):
        self.timestamp = timestamp
        self.UTC = UTC
        self.callsign = callsign
        self.lat = lat
        self.lon = lon
        self.position = Point(lat, lon)
        self.point = Point(lat, lon, altitude)
        self.altitude = altitude
        self.speed = speed
        self.direction = direction

    def as_list(self):
        return [self.UTC.date(), self.UTC.time(), self.callsign,
                self.lat, self.lon, self.altitude, self.speed, self.direction]


class FlightLog:
    def __init__(self,
                 flight_log_records: List[FlightLogRecord]):
        self.records = flight_log_records
        self.records.sort(key=lambda r: r.UTC)

    def start_position(self):
        return self.records[0].position

    def end_position(self):
        return self.records[-1].position

    def gc_miles(self):
        return geodesic(self.start_position(), self.end_position()).miles

    def flown_miles(self):
        return sum([geodesic(record.position, self.records[idx].position).miles
                    for idx, record in enumerate(self.records[1:])])

    def max_altitude(self):
        return max([record.altitude for record in self.records])

    def max_speed(self):
        return max([record.speed for record in self.records])

    def as_df(self):
        col_names = ['date', 'time', 'callsign', 'lat', 'lon',
                     'altitude', 'speed', 'direction']
        dataset = [record.as_list() for record in self.records]

        return pd.DataFrame(dataset, columns=col_names)

    def __str__(self):
        rep = self.records[0]
        output = f'Flight {rep.callsign} on {rep.UTC.date()}'
        output += f' ({len(self.records)} records)'
        return output


def csv_row_to_record(row):
    lat, lon = tuple(row['Position'].split(','))
    UTC_datetime = dt.datetime.fromisoformat(row['UTC'])
    return FlightLogRecord(row['Timestamp'], UTC_datetime,
                           row['Callsign'], lat, lon,
                           row['Altitude'], row['Speed'],
                           row['Direction'])


def csv_to_flight_log(filename):
    df = pd.read_csv(filename)
    records = [csv_row_to_record(row) for _, row in df.iterrows()]
    return FlightLog(records)
