
import datetime as dt

from kayak_manager import KayakManager
from consts import DATE_FORMAT


def main():
    origin = "TLV"
    dest = "ROM"
    depart_date = "04/05/2023"
    return_date = "11/05/2023"
    class_ = "economy"
    num_of_passengers = 2

    manager = KayakManager(
        origin=origin,
        destination=dest,
        depart_date=dt.datetime.strptime(depart_date, DATE_FORMAT),
        return_date=dt.datetime.strptime(return_date, DATE_FORMAT),
        class_=class_,
        passengers=num_of_passengers
    )
    all_flights = manager.get_trips()
    print("\n".join([str(trip) for trip in all_flights]))


if __name__ == "__main__":
    main()