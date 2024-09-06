from study_proj.controllers.base_controller import BaseController
from study_proj.models import Flight, AirportsDatum
from collections import deque


class FlightController(BaseController):

    @staticmethod
    def bfs_paths_with_city(graph, start, goal, airport_to_city, max_transits=2):
        queue = deque([(start, [start], [airport_to_city[start]])])
        while queue:
            (vertex, path, cites) = queue.pop()
            for next in set(graph[vertex]) - set(path):
                if len(path) > max_transits:
                    continue
                if airport_to_city[next] in cites:
                    continue
                if next == goal:
                    yield path + [next]
                else:
                    queue.appendleft((next, path + [next], cites + [airport_to_city[next]]))

    def get_all_flights(self, page: int) -> list:
        page_size = 50
        flight_query = self.session.query(Flight.flight_id,
                                          Flight.flight_no,
                                          Flight.scheduled_departure,
                                          Flight.scheduled_arrival,
                                          Flight.departure_airport,
                                          Flight.arrival_airport,
                                          Flight.status,
                                          Flight.aircraft_code,
                                          Flight.actual_departure,
                                          Flight.actual_arrival
                                          ).limit(page_size).offset(page * page_size)
        flights = [x._asdict() for x in flight_query if x is not None]
        for flight in flights:
            for key in ('scheduled_departure', 'scheduled_arrival', 'actual_departure', 'actual_arrival'):
                if flight[key]:
                    flight[key] = str(flight[key])
        return flights

    def get_single_flight(self, key: int) -> dict:
        flight = self.session.query(Flight.flight_id,
                                    Flight.flight_no,
                                    Flight.scheduled_departure,
                                    Flight.scheduled_arrival,
                                    Flight.departure_airport,
                                    Flight.arrival_airport,
                                    Flight.status,
                                    Flight.aircraft_code,
                                    Flight.actual_departure,
                                    Flight.actual_arrival
                                    ).filter_by(
            flight_id=key).first()
        if flight:
            flight = flight._asdict()
            for param in ('scheduled_departure', 'scheduled_arrival', 'actual_departure', 'actual_arrival'):
                if flight[param]:
                    flight[param] = str(flight[param])
        return flight

    def get_routes_from_to(self, departure_airport, arrival_airport, max_transits):
        airports = self.session.query(AirportsDatum.airport_code, AirportsDatum.city).all()
        edges = self.session.query(Flight.departure_airport, Flight.arrival_airport).distinct().all()
        nodes = [x[0] for x in airports]
        airports = {x[0]: x[1]['en'] for x in airports}
        listed_graph = {key: [] for key in nodes}
        for edge in edges:
            listed_graph[edge[0]].append(edge[1])
        return list(self.bfs_paths_with_city(listed_graph, departure_airport, arrival_airport, airports, max_transits))

    def get_flights_from_to_(self, departure_date, departure_airport, arrival_airport, max_transits: int):
        routes = self.get_routes_from_to(departure_airport, arrival_airport, max_transits)
        res = []
        for route in routes:
            flights = []
            prev = route[0]
            for key in route[1:]:
                flight = self.session.query(Flight.flight_id,
                                            Flight.scheduled_departure,
                                            Flight.scheduled_arrival,
                                            Flight.flight_no,
                                            Flight.departure_airport,
                                            Flight.arrival_airport,
                                            Flight.aircraft_code
                                            ).filter(
                    Flight.scheduled_departure > departure_date, Flight.departure_airport == prev,
                    Flight.arrival_airport == key,
                    Flight.status == "Scheduled"
                ).order_by(Flight.scheduled_departure).first()
                prev = key
                if flight is None:
                    break
                flights.append(flight._asdict())
                departure_date = flights[-1]['scheduled_arrival']
                for param in ('scheduled_departure', 'scheduled_arrival'):
                    if flights[-1][param]:
                        flights[-1][param] = str(flights[-1][param])
            else:
                res.append(flights)
        return res

    def post_flight(self, data: dict) -> bool:
        self.session.add(Flight(flight_no=data['flight_no'],
                                scheduled_departure=data['scheduled_departure'],
                                scheduled_arrival=data['scheduled_arrival'],
                                departure_airport=data['departure_airport'],
                                arrival_airport=data['arrival_airport'],
                                status=data['status'],
                                aircraft_code=data['aircraft_code'],
                                actual_departure=data['actual_departure'],
                                actual_arrival=data['actual_arrival']
                                ))
        self.session.flush()
        self.session.commit()
        return True

    def delete_flight(self, key: str) -> bool:
        self.session.delete(self.session.query(Flight).get(key))
        return True

    def put_flight(self, _key: str, data: dict) -> bool:
        obj_to_update = self.session.query(Flight).filter_by(flight_id=_key).first()
        print(obj_to_update.__dict__.keys())
        for key, value in data.items():
            obj_to_update.__setattr__(key, value)
        self.session.flush()
        self.session.commit()
        return True

    @staticmethod
    def asa(self):
        pass