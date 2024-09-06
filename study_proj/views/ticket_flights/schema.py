import colander
from study_proj.views.tickets.validators import ticket_no_validator


class TicketFlightsPost(colander.MappingSchema):
    flight_id = colander.SchemaNode(colander.Integer())
    ticket_no = colander.SchemaNode(colander.String(), validator=ticket_no_validator)
    fare_conditions = colander.SchemaNode(colander.String(),
                                          validator=colander.OneOf(['Economy', 'Comfort', 'Business']))
    amount = colander.SchemaNode(colander.Decimal())


class TicketFlightsPut(colander.MappingSchema):
    amount = colander.SchemaNode(colander.Decimal(), missing=colander.required)
