# coding: utf-8
import datetime

from study_proj.models import Flight
from cornice.resource import resource, view
import sqlalchemy as sa
from .schema import *
from cornice.validators import colander_body_validator
from study_proj.controllers.flights_controller import FlightController


@resource(name="flights", collection_path='/flights', path='/flights/{flight_id}')
class Flights(object):

    def __init__(self, request, context=None):
        self.request = request
        self.controller = FlightController(self.request.db)

    def collection_get(self) -> list:
        # return self.controller.get_all_flights(int(self.request.params.get('page', default=0)))
        return self.controller.get_flights_from_to_(
            departure_date=self.request.params.get('departure_date', default=datetime.datetime.now()),
            departure_airport=self.request.params.get('departure_airport', default='VKO'),
            arrival_airport=self.request.params.get('arrival_airport', default='VVO'),
            max_transits=int(self.request.params.get('max_transits', default=2)),
        )

    # def update_date(self, key: int):
    #     self.controller.get_single_flight(key)
    #     obj_to_update = self.request.db.query(Flight).filter_by(flight_id=key).first()
    #     obj_to_update.scheduled_departure += datetime.timedelta(days=365*6-119)
    #     obj_to_update.scheduled_arrival += datetime.timedelta(days=365*6-119)
    #
    # def update_status(self, key):
    #     obj_to_update = self.request.db.query(Flight).filter_by(flight_id=key).first()
    #     if obj_to_update.status not in ['Cancelled', 'Scheduled']
    #     obj_to_update.scheduled_departure += datetime.timedelta(days=365 * 6 - 119)
    #     obj_to_update.scheduled_arrival += datetime.timedelta(days=365 * 6 - 119)

    def get(self) -> dict:
        # for i in range(1, 65665):
        #     self.update_status(i)
        # self.request.db.commit()
        return self.controller.get_single_flight(self.request.matchdict['flight_id'])

    @view(schema=FlightsPost(), validators=(colander_body_validator,))
    def collection_post(self):
        data_to_ins = {}
        for key in self.request.params:
            if self.request.params[key] != 'null' and self.request.params[key]:
                data_to_ins[key] = self.request.params[key]
            else:
                data_to_ins[key] = None
        return self.controller.post_flight(data_to_ins)

    # TODO make cascade delete
    def delete(self):
        return self.controller.delete_flight(self.request.matchdict['flight_id'])

    @view(schema=FlightsPut(), validators=(colander_body_validator,))
    def put(self):
        data_to_update = {}
        keys = [
            'scheduled_departure',
            'departure_airport',
            'scheduled_arrival',
            'actual_departure',
            'arrival_airport',
            'actual_arrival',
            'aircraft_code',
            'flight_id',
            'flight_no',
            'status',
        ]
        for key in keys:
            if self.request.params.get(key, default=None):
                data_to_update[key] = self.request.params[key]
        return self.controller.put_flight(self.request.matchdict['flight_id'], data_to_update)
