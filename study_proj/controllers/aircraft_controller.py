import json

from study_proj.controllers.base_controller import BaseController
from study_proj.models import AircraftsDatum, Flight, Seat, Booking, Ticket, TicketFlight, BoardingPass


class AircraftController(BaseController):
    def get_all_aircrafts(self):
        aircrafts = self.session.query(
            AircraftsDatum.aircraft_code, AircraftsDatum.model, AircraftsDatum.range
        ).all()
        return [row._asdict() for row in aircrafts]

    def get_single_aircraft(self, data):
        aircraft = (
            self.session.query(
                AircraftsDatum.aircraft_code, AircraftsDatum.model, AircraftsDatum.range
            )
            .filter(
                AircraftsDatum.aircraft_code == data["aircraft_code"]
            )
            .one()
        )
        return aircraft._asdict()

    def post_aircraft(self, data):
        self.session.add(AircraftsDatum(
            aircraft_code=data["aircraft_code"],
            model=json.loads(data["model"]),
            range=int(data["range"]),
        ))
        self.session.flush()
        self.session.commit()
        return True

    def delete_aircraft(self, data):
        # При удалении самолета произойдет конфликт со значениями в таблице рейсов
        aircraft = self.session.query(AircraftsDatum).get(
            data['aircraft_code']
        )
        flights = self.session.query(Flight).filter(Flight.aircraft_code == aircraft.aircraft_code).all()
        for flight in flights:
            flight.status = 'Cancelled'
            self.session.add(flight)
            self.session.flush()
        # seats = self.session.query(Seat).filter(Seat.aircraft_code == aircraft.aircraft_code).one()
        # self.session.delete(seats)
        # self.session.commit()
        return True

    def put_aircraft(self, data):
        aircraft = self.session.query(AircraftsDatum).filter(
            AircraftsDatum.aircraft_code == data["aircraft_code"]
        ).one()
        if data.get('range'):
            aircraft.range = int(data['range'])
        if data.get('model'):
            aircraft.model = json.loads(data['model'])
        self.session.add(aircraft)
        self.session.flush()
        self.session.commit()
        return True
