import json

from study_proj.controllers.base_controller import BaseController
from study_proj.models import Booking, Ticket, TicketFlight, BoardingPass


class TicketController(BaseController):
    def get_all_ticket_by_book_ref(self, key):
        tickets = self.session.query(
            Ticket.ticket_no, Ticket.book_ref, Ticket.passenger_id, Ticket.passenger_name, Ticket.contact_data
        ).filter(
            Ticket.book_ref == key
        ).all()
        return [x._asdict() for x in tickets if x is not None]

    def get_all_tickets(self):
        tickets = self.session.query(
            Ticket.ticket_no, Ticket.book_ref, Ticket.passenger_name
        ).all()
        return [row._asdict() for row in tickets]

    def get_single_ticket(self, data):
        ticket = self.session.query(
            Ticket.ticket_no, Ticket.book_ref, Ticket.passenger_id, Ticket.passenger_name, Ticket.contact_data
        ).filter(
            Ticket.ticket_no == data['ticket_no'] and
            Ticket.book_ref == data['book_ref']
        ).one()

        return ticket._asdict()

    def post_ticket(self, data):
        self.session.add(Ticket(
            ticket_no=data['ticket_no'],
            book_ref=data['book_ref'],
            passenger_id=data['passenger_id'],
            passenger_name=data['passenger_name'],
            contact_data=json.loads(data["contact_data"]) if data.get('contact_data') else None,
        ))
        self.session.commit()
        return True

    def delete_ticket(self, data: dict):
        ticket = self.session.query(Ticket).filter(
            Ticket.ticket_no == data['ticket_no'] and
            Ticket.book_ref == data['book_ref']
        ).one()
        ticket_amount = 0
        ticket_flights = self.session.query(TicketFlight).filter(TicketFlight.ticket_no == ticket.ticket_no).all()
        boarding_passes = self.session.query(BoardingPass).filter(BoardingPass.ticket_no == ticket.ticket_no)
        for boarding_pass in boarding_passes:
            # Можно/нужно вызвать метод из BoardingPassController
            self.session.delete(boarding_pass)  # 1) Нужно ли делать flush()? 2) try/catch?
        self.session.flush()
        for ticket_flight in ticket_flights:
            ticket_amount += ticket_flight.amount
            self.session.delete(ticket_flight)  # 1) Нужно ли делать flush()? 2) try/catch?
        booking = self.session.query(Booking).get(ticket.book_ref)
        booking.total_amount -= ticket_amount
        self.session.add(booking)
        self.session.flush()
        self.session.delete(ticket)  # try/catch?
        self.session.commit()
        return True

    def put_ticket(self, data):  # TODO: Проверить, что работает
        obj_to_update = self.session.query(Ticket).get(data['ticket_no'])
        for key, value in data.items():
            obj_to_update.__setattr__(key, value)
        self.session.flush()
        self.session.commit()
        return True

