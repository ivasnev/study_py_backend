import colander



class FlightsPost(colander.MappingSchema):
    flight_id = colander.SchemaNode(colander.Integer())
    scheduled_departure = colander.SchemaNode(colander.DateTime())
    scheduled_arrival = colander.SchemaNode(colander.DateTime())
    departure_airport = colander.SchemaNode(colander.String(), validator=colander.Length(3))
    arrival_airport = colander.SchemaNode(colander.String(), validator=colander.Length(3))
    status = colander.SchemaNode(colander.String(), validator=colander.Length(max=20))
    aircraft_code = colander.SchemaNode(colander.String(), validator=colander.Length(3))
    actual_departure = colander.SchemaNode(colander.DateTime(), missing=None)
    actual_arrival = colander.SchemaNode(colander.DateTime(), missing=None)


class FlightsPut(colander.MappingSchema):
    flight_id = colander.SchemaNode(colander.Integer(), missing=colander.drop)
    scheduled_departure = colander.SchemaNode(colander.DateTime(), missing=colander.drop)
    scheduled_arrival = colander.SchemaNode(colander.DateTime(), missing=colander.drop)
    departure_airport = colander.SchemaNode(colander.String(), validator=colander.Length(3), missing=colander.drop)
    arrival_airport = colander.SchemaNode(colander.String(), validator=colander.Length(3), missing=colander.drop)
    status = colander.SchemaNode(colander.String(), validator=colander.Length(max=20), missing=colander.drop)
    aircraft_code = colander.SchemaNode(colander.String(), validator=colander.Length(3), missing=colander.drop)
    actual_departure = colander.SchemaNode(colander.DateTime(), missing=None)
    actual_arrival = colander.SchemaNode(colander.DateTime(), missing=None)
