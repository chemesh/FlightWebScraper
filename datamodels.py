from dataclasses import dataclass


@dataclass
class Flight:
    flight_id: str
    origin: str
    destination: str
    date: str
    departure: str
    arrival: str
    operator: str
    warnings: list

    def __str__(self):
        return (f'Flight ID: {self.flight_id}, '
                f'Departure Airport: {self.origin}, '
                f'Arrival Airport: {self.destination}, '
                f'Date: {self.date}, '
                f'Departure Time: {self.departure}, '
                f'Arrival Time: {self.arrival}, '
                f'Operator: {self.operator}, '
                f'Important Notes: {", ".join(self.warnings)} '
        )

    def to_json(self):
        return vars(self)

    def to_csv(self, delimiter=','):
        headers = ""
        values = ""
        for header, value in self.to_json().items():
            headers += f'{str(header)}{delimiter}'
            values += f'{str(value)}{delimiter}'
        res = headers.rstrip(delimiter) + "\n"
        res += values.rstrip(delimiter)
        return res


@dataclass
class Trip:
    depart_flights: list[Flight]
    return_flights: list[Flight]
    price: str
    cabin: str
    provider: str
    link: str

    def __str__(self):
        departs = '\n'.join(['\t'+str(flight) for flight in self.depart_flights])
        arrivals = '\n'.join(['\t'+str(flight) for flight in self.return_flights])
        return (
            f'Departure Flights:\n{departs}\n'
            f'Return Flights:\n{arrivals}\n'
            f'Best Price: {self.price}, '
            f'Cabin Class: {self.cabin}, '
            f'Provider: {self.provider}, '
            f'Link: {self.link}'
        )

    def to_json(self):
        res = vars(self)
        res['depart_flights'] = [flight.to_json() for flight in self.depart_flights]
        res['return_flights'] = [flight.to_json() for flight in self.return_flights]
        return res





