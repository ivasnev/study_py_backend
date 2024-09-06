# coding: utf-8

import json

from cornice.resource import resource, view
from sqlalchemy import update

from study_proj.controllers.aircraft_controller import AircraftController
from study_proj.models import AircraftsDatum
from study_proj.views.aircraft_data.validators import (id_validator,
                                                       request_validator)


@resource(collection_path="/aircrafts", path="/aircraft/{aircraft_code}")
class Aircraft(object):
    def __init__(self, request, context=None):
        self.request = request
        self.controller = AircraftController(self.request.db)

    def collection_get(self):
        return self.controller.get_all_aircrafts()

    @view(renderer="json", validators=id_validator)
    def get(self):
        return self.controller.get_single_aircraft(self.request.matchdict)

    @view(renderer="json", validators=request_validator("post_aircraft"))
    def collection_post(self):
        return self.controller.post_aircraft(self.request.POST)

    @view(renderer="json", validators=id_validator)
    def delete(self):
        return self.controller.delete_aircraft(self.request.matchdict)

    @view(renderer="json", validators=request_validator("put_aircraft"))
    def put(self):
        return self.controller.put_aircraft({**self.request.matchdict, **self.request.POST})
