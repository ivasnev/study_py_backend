from study_proj.models import *
from study_proj.controllers.base_controller import BaseController
import json


class SeatController(BaseController):

    def get_single_seat(self, keys):
        """Получение одного места"""
        res = self.session.query(Seat.aircraft_code, Seat.seat_no, Seat.fare_conditions) \
            .filter(Seat.aircraft_code == keys['aircraft_code'], Seat.seat_no == keys['seat_no']).one()

        return dict(res)

    def get_all_seats(self):
        """Получение всех мест"""
        res = self.session.query(Seat.aircraft_code, Seat.seat_no).all()
        return [dict(row) for row in res]

    def post_seat(self, data):
        """Добавление места"""

        self.session.add(Seat(aircraft_code=data['aircraft_code'],
                              seat_no=data['seat_no'],
                              fare_conditions=data['fare_conditions'])
                         )
        self.session.flush()
        self.session.commit()
        return True

    def delete_seat(self, keys):
        """Удаление места"""
        deletable = self.session.query(Seat).get(keys)
        self.session.delete(deletable)
        self.session.commit()
        return True

    def put_seat(self, keys, data):
        """Обновление информации"""

        obj = self.session.query(Seat).filter_by(seat_no=keys['seat_no'], aircraft_code=keys['aircraft_code']).first()

        for key in data:
            obj.__setattr__(key, data[key])
        self.session.flush()
        self.session.commit()
        return True
