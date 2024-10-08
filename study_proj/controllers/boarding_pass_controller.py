import json

from sqlalchemy import and_

from study_proj.controllers.base_controller import BaseController
from study_proj.models import Booking, Ticket, TicketFlight, BoardingPass


class BoardingPassController(BaseController):
    def get_all_boarding_passes(self):
        boarding_passes = self.session.query(
            BoardingPass.ticket_no, BoardingPass.flight_id, BoardingPass.boarding_no
        ).all()
        return [dict(row) for row in boarding_passes]

    def get_single_boarding_pass(self, data):
        boarding_pass = self.session.query(
            BoardingPass.ticket_no, BoardingPass.flight_id, BoardingPass.boarding_no, BoardingPass.seat_no
        ).filter(and_(BoardingPass.ticket_no == data['ticket_no'], BoardingPass.flight_id == data['flight_id'], )).one()

        return dict(boarding_pass)

    def post_boarding_pass(self, data):
        self.session.add(BoardingPass(
            ticket_no=data['ticket_no'],
            flight_id=data['flight_id'],
            boarding_no=data['boarding_no'],
            seat_no=data['seat_no'],
        ))
        self.session.commit()
        return True

    def delete_boarding_pass(self, data: dict):
        boarding_pass = self.session.query(
            BoardingPass
        ).filter(and_(BoardingPass.ticket_no == data['ticket_no'], BoardingPass.flight_id == data['flight_id'])).one()
        self.session.delete(boarding_pass)  # try/catch?
        self.session.commit()
        return True

    def put_ticket(self, data):  # TODO: Проверить, что работает
        boarding_pass = self.session.query(BoardingPass).filter(
            BoardingPass.ticket_no == data["ticket_no"],
            BoardingPass.flight_id == data["flight_id"],
        ).one()
        if data['ticket_no']:
            boarding_pass.ticket_no = data['ticket_no']
        if data['flight_id']:
            boarding_pass.flight_id = int(data['flight_id'])
        self.session.add(boarding_pass)
        self.session.flush()
        self.session.commit()
        return True
